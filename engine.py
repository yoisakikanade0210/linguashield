# -*- coding: utf-8 -*-
"""
engine.py —— 语盾(LinguaShield) 检测引擎
================================================
把 rules.py 里的规则"跑起来"，输出：
    风险总分 / 风险等级 / 可读的判定理由(reasons) / 命中的 URL

设计思想来源（合规声明）：
  · 语言路由 + 规则分层 + 可读理由  ← 借鉴 SecuriSMS（MIT）
  · 多层加权评分                      ← 借鉴 phishing-detector-advanced
以上仅为**设计思路**的借鉴；本文件全部代码为自行编写，未复制任何仓库源码。

核心流程：
  1. normalize()        归一化：处理钓鱼者常用的规避字符
  2. detect_language()  语言路由：判断中文/英文，决定用哪套话术库
  3. check_urls()       URL 信誉：短链/可疑TLD/仿冒域名/IP直连/白名单
  4. match_phrases()    话术匹配：单条规则命中
  5. match_combos()     组合规则：多类话术同现（C 层）
  6. analyze()          汇总加权，输出可读结论
"""

import re
from rules import (
    EN_PHRASES, ZH_PHRASES, COMBO_RULES, WEIGHTS, GROUP_BASE,
    SHORTENERS, SUSPICIOUS_TLDS, BRAND_KEYWORDS, TRUSTED_DOMAINS,
)

# ------------------------------------------------------------
# 1. 归一化：处理规避手段（借鉴 SecuriSMS 的 evasion 应对）
# ------------------------------------------------------------
# 钓鱼者常用这些手段绕过关键词检测：
#   · 零宽字符：paypal → pay\u200bpal（肉眼看不出区别）
#   · 全角字符：ｐａｙｐａｌ（用全角字母）
#   · 插入符号：p-a-y-p-a-l
ZERO_WIDTH_CHARS = ["\u200b", "\u200c", "\u200d", "\ufeff"]  # 各类零宽字符


def normalize(text):
    """把文本'洗干净'，让钓鱼者的小花招失效"""
    # 去掉零宽字符（它们看不见，但会让关键词匹配失败）
    for ch in ZERO_WIDTH_CHARS:
        text = text.replace(ch, "")
    # 全角字符转半角：全角Ａ(0xFF21) → 半角A(0x41)
    # 技巧：全角字母和半角字母的编码差固定为 0xFEE0
    result = ""
    for ch in text:
        code = ord(ch)
        if 0xFF01 <= code <= 0xFF5E:          # 全角字符区间
            result += chr(code - 0xFEE0)      # 转成半角
        else:
            result += ch

    # ★修复：把所有空白字符统一成单个半角空格
    # 全角空格是全角字符吗？不是！全角空格是 U+3000，不在 0xFF01~0xFF5E 区间里，
    # 上面的转换漏掉了它。于是钓鱼者这样写就能绕过：
    #     "account　is　suspended"   ← 用的是全角空格
    # 而我们的规则写的是 "account is suspended"（半角空格），匹配失败 → 漏报。
    # 用 \s+ 统一所有空白（含全角空格、制表符、换行）为单个半角空格即可。
    result = re.sub(r"\s+", " ", result)
    return result


# ------------------------------------------------------------
# 2. 语言路由：判断中文还是英文（借鉴 SecuriSMS 的 language routing）
# ------------------------------------------------------------
def detect_language(text):
    """
    统计中文字符占比来判断语言。
    返回 "zh"（中文）或 "en"（英文）。
    为什么要判断？→ 中文邮件用中文话术库，英文邮件用英文话术库，
    避免"用英文库查中文邮件"导致的漏报，也避免误报。
    """
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))  # 统计汉字个数
    total_count = len(text.strip())
    if total_count == 0:
        return "en"
    # 汉字占比超过 10% 就认为是中文文本
    return "zh" if chinese_count / total_count > 0.10 else "en"


# ------------------------------------------------------------
# 3. URL 信誉检查（借鉴 SecuriSMS 的 URL reputation）
# ------------------------------------------------------------
URL_PATTERN = re.compile(r"https?://[^\s<>\"'）)]+|www\.[^\s<>\"'）)]+")


def check_urls(text):
    """检查文本里的所有 URL，返回 (总分, 理由列表, URL列表)"""
    urls = URL_PATTERN.findall(text)
    if not urls:
        return 0, [], []

    score = 0
    reasons = []

    for url in urls:
        low = url.lower()

        # (1) 白名单：可信域名直接放行，避免误伤（比如学校官网链接）
        if any(trusted in low for trusted in TRUSTED_DOMAINS):
            continue

        # ★关键修复：先提取"主机名(host)"再做判断
        # 初版直接对整个 URL 做 endswith(".tk")，但真实 URL 长这样：
        #   http://paypa1-secure.tk/login    ← 结尾是 "/login"，不是 ".tk"
        # 所以 .tk 根本检测不到。必须先把 host 单独取出来再判断后缀。
        host_match = re.search(r"https?://([^/\s]+)", low)
        if host_match:
            host = host_match.group(1).split(":")[0]   # split 去掉可能的端口号
        else:
            host = low.split("/")[0]

        # (2) IP 直连：正常网站几乎不会用 http://192.168.1.1 这种形式
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
            score += 30
            reasons.append(f"URL 直接使用 IP 地址：{url}")

        # (3) 短链接：隐藏真实去向，钓鱼常用
        if any(short in host for short in SHORTENERS):
            score += 25
            reasons.append(f"使用短链接（隐藏真实地址）：{url}")

        # (4) 可疑顶级域名：免费/低成本域名滥用率高
        #     现在用 host 判断，http://paypa1-secure.tk/login 能正确识别
        hit_tld = [t for t in SUSPICIOUS_TLDS if host.endswith(t)]
        if hit_tld:
            score += 20
            reasons.append(f"高风险域名后缀 {hit_tld[0]}：{url}")

        # (5) 仿冒/近似域名：host 里含品牌名，但域名并非官方域名
        #     典型：paypal.com.verify-account.tk —— 用 paypal 迷惑你，真实域名是后者
        for brand in BRAND_KEYWORDS:
            if brand in host:
                score += 30
                reasons.append(f"URL 疑似仿冒品牌「{brand}」：{url}")
                break

        # 注意：以上各项**可以累加**（没有 continue）。
        # 一个恶意 URL 常常同时踩中多条：既仿冒品牌、又用 .tk 后缀。
    return score, reasons, urls


# ------------------------------------------------------------
# 4. 话术匹配（R 层：单条规则）
# ------------------------------------------------------------
def match_phrases(text, lang):
    """
    按语言选择话术库，返回 (总分, 理由列表, 命中的分组集合)
    matched_groups 用于后面做"组合规则"判断。
    """
    # 语言路由：选对应的话术库
    phrase_dict = ZH_PHRASES if lang == "zh" else EN_PHRASES
    low = text.lower()

    score = 0
    reasons = []
    matched_groups = set()

    for group_name, phrases in phrase_dict.items():
        # 从 GROUP_BASE 取这一组的基础分（不同组权重不同）
        base = GROUP_BASE.get(group_name, 10)
        for phrase in phrases:
            # 英文按小写匹配；中文直接子串匹配
            target = phrase.lower() if lang == "en" else phrase
            if target in low:
                score += base                  # ★用分组基础分，而不是固定 10 分
                matched_groups.add(group_name)
                reasons.append(f'命中{group_name}话术：「{phrase}」(+{base})')
                break                          # 同一组命中一条即可，避免重复加分

    return score, reasons, matched_groups


# ------------------------------------------------------------
# 5. 组合规则（C 层：多类话术同现 → 高度可疑）
# ------------------------------------------------------------
def match_combos(matched_groups):
    """
    借鉴 SecuriSMS 的"组合规则"：单条话术可能是巧合，
    但"冒充身份 + 索要密码"同时出现，几乎必然是钓鱼。
    """
    score = 0
    reasons = []

    for need_groups, add_score, desc in COMBO_RULES:
        # all() 判断所需的话术组是否全部命中
        if all(g in matched_groups for g in need_groups):
            score += add_score
            reasons.append(f"组合告警：{desc}")

    return score, reasons


# ------------------------------------------------------------
# 6. 主函数：汇总加权，输出可读结论
# ------------------------------------------------------------
def analyze(text):
    """
    对外主接口。输入一段邮件/短信文本，返回结构化结果。

    返回字典：
      lang          检测到的语言(zh/en)
      raw_score     加权前总分
      score         加权后总分（封顶 100）
      level         风险等级文字
      reasons       可读的判定理由列表（可解释）
      urls          文本中提取到的所有 URL
    """
    # Step 1: 归一化（处理规避字符）
    clean = normalize(text)

    # Step 2: 语言路由
    lang = detect_language(clean)

    # Step 3: 三个层面分别检测
    url_score, url_reasons, urls = check_urls(clean)               # URL 层
    phrase_score, phrase_reasons, matched = match_phrases(clean, lang)  # 话术层
    combo_score, combo_reasons = match_combos(matched)             # 组合层

    # Step 4: 多层加权合并（借鉴 phishing-detector-advanced 的加权思想）
    weighted = (
        phrase_score * WEIGHTS["phrase"] +
        combo_score  * WEIGHTS["combo"] +
        url_score    * WEIGHTS["url"]
    )
    score = min(int(weighted), 100)   # 封顶 100 分

    return {
        "lang": lang,
        "raw_score": int(phrase_score + combo_score + url_score),
        "score": score,
        "level": level_text(score),
        "reasons": phrase_reasons + combo_reasons + url_reasons,
        "urls": urls,
    }


def level_text(score):
    """把分数转成人类可读的风险等级"""
    if score >= 70:
        return "高危（强烈疑似钓鱼）"
    elif score >= 40:
        return "可疑（建议谨慎核实）"
    elif score >= 15:
        return "低风险（存在个别可疑信号）"
    else:
        return "基本安全"


# ------------------------------------------------------------
# 直接运行本文件时，做一次命令行交互演示
# ------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 55)
    print("  语盾 LinguaShield —— 中英双语钓鱼检测（命令行版）")
    print("=" * 55)
    while True:
        user_input = input("\n请输入待检测文本（输入 q 退出）：\n> ")
        if user_input.lower() == "q":
            print("再见！")
            break
        result = analyze(user_input)
        print("\n" + "-" * 55)
        print(f"检测语言：{result['lang']}")
        print(f"风险总分：{result['score']} / 100")
        print(f"风险等级：{result['level']}")
        if result["urls"]:
            print(f"发现 URL：{result['urls']}")
        print("判定理由：")
        for r in result["reasons"]:
            print(f"  · {r}")
        print("-" * 55)
