


import re
from rules import (
    EN_PHRASES, ZH_PHRASES, COMBO_RULES, WEIGHTS, GROUP_BASE,
    SHORTENERS, SUSPICIOUS_TLDS, BRAND_KEYWORDS, TRUSTED_DOMAINS,

    AGRI_TRUSTED_DOMAINS, SECOND_CHANNEL_TRIGGERS,
    EMAIL_AUTH_CHECKS, AGRI_VERIFY_CHECKLIST, HOMOGLYPH_MAP,
)






ZERO_WIDTH_CHARS = ["\u200b", "\u200c", "\u200d", "\ufeff"]


def normalize(text):
    

    for ch in ZERO_WIDTH_CHARS:
        text = text.replace(ch, "")


    result = ""
    for ch in text:
        code = ord(ch)
        if 0xFF01 <= code <= 0xFF5E:
            result += chr(code - 0xFEE0)
        else:
            result += ch







    result = re.sub(r"\s+", " ", result)
    return result



def detect_language(text):
    
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    total_count = len(text.strip())
    if total_count == 0:
        return "en"

    return "zh" if chinese_count / total_count > 0.10 else "en"



URL_PATTERN = re.compile(r"https?://[^\s<>\"'）)]+|www\.[^\s<>\"'）)]+")


def check_urls(text):
    
    urls = URL_PATTERN.findall(text)
    if not urls:
        return 0, [], []

    score = 0
    reasons = []

    for url in urls:
        low = url.lower()



        if any(trusted in low for trusted in TRUSTED_DOMAINS):
            continue
        if any(trusted in low for trusted in AGRI_TRUSTED_DOMAINS):
            continue





        host_match = re.search(r"https?://([^/\s]+)", low)
        if host_match:
            host = host_match.group(1).split(":")[0]
        else:
            host = low.split("/")[0]


        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
            score += 30
            reasons.append(f"URL 直接使用 IP 地址：{url}")


        if any(short in host for short in SHORTENERS):
            score += 25
            reasons.append(f"使用短链接（隐藏真实地址）：{url}")



        hit_tld = [t for t in SUSPICIOUS_TLDS if host.endswith(t)]
        if hit_tld:
            score += 20
            reasons.append(f"高风险域名后缀 {hit_tld[0]}：{url}")



        for brand in BRAND_KEYWORDS:
            if brand in host:
                score += 30
                reasons.append(f"URL 疑似仿冒品牌「{brand}」：{url}")
                break



    return score, reasons, urls



def match_phrases(text, lang):
    

    phrase_dict = ZH_PHRASES if lang == "zh" else EN_PHRASES
    low = text.lower()

    score = 0
    reasons = []
    matched_groups = set()

    for group_name, phrases in phrase_dict.items():

        base = GROUP_BASE.get(group_name, 10)
        for phrase in phrases:

            target = phrase.lower() if lang == "en" else phrase
            if target in low:
                score += base
                matched_groups.add(group_name)
                reasons.append(f'命中{group_name}话术：「{phrase}」(+{base})')
                break

    return score, reasons, matched_groups



def match_combos(matched_groups):
    
    score = 0
    reasons = []

    for need_groups, add_score, desc in COMBO_RULES:

        if all(g in matched_groups for g in need_groups):
            score += add_score
            reasons.append(f"组合告警：{desc}")

    return score, reasons








def extract_domain(url):
    
    m = re.search(r"https?://([^/\s:]+)", url.lower())
    if m:
        return m.group(1)
    return url.lower().split("/")[0].split(":")[0]


def domain_looks_spoofed(host):
    

    known = [
        "microsoft", "paypal", "apple", "google", "amazon",
        "alibaba", "sinosure", "fao", "usda", "customs",
    ]

    deobf = host
    for fake, real in HOMOGLYPH_MAP.items():
        deobf = deobf.replace(fake, real)

    if deobf == host:
        return False, ""

    for name in known:
        if name in deobf and name not in host:
            detail = "、".join(f"{k}→{v}" for k, v in HOMOGLYPH_MAP.items() if k in host)
            return True, f"域名 {host} 疑似用形近字替换冒充「{name}」（{detail}）"
    return False, ""


def verify_checklist(text, clean, urls, matched_groups, score):
    
    low = clean.lower()
    tips = []
    domains = []


    hit_trigger = [t for t in SECOND_CHANNEL_TRIGGERS
                   if (t.lower() in low)]
    if hit_trigger:
        tips.append(
            "【账户变更·必须第二渠道核实】本邮件出现账户/汇款相关表述"
            f"（{'、'.join(hit_trigger[:3])}）。"
            "任何收款账户变更，都必须用**合同上原留存的**电话或当面核实，"
            "绝不要使用本邮件里提供的新号码/新联系人。"
        )
        tips.extend(EMAIL_AUTH_CHECKS)


    for url in urls:
        host = extract_domain(url)
        domains.append(host)
        spoofed, detail = domain_looks_spoofed(host)
        if spoofed:
            tips.append(f"【域名疑似仿冒】{detail}")
        else:
            tips.append(
                f"【域名比对】链接真实域名是「{host}」，"
                "请与对方公司官网公布的域名逐字比对（注意 0/o、1/l、rn/m 之类替换）。"
            )


    agri_groups = {
        "商务异常（BEC Core）", "农业外贸场景（Agri Trade）",
        "外贸金融异常（Trade Finance Anomaly）",
        "涉农场景（中性词）", "外贸结算（Trade Settlement）",
        "账户变更（Account Change）",
    }
    if matched_groups & agri_groups:
        tips.append("【农业国际合作场景·标准核验清单】")
        tips.extend(AGRI_VERIFY_CHECKLIST)


    seen = set()
    uniq = []
    for t in tips:
        if t not in seen:
            seen.add(t)
            uniq.append(t)

    return uniq, domains



def analyze(text):
    

    clean = normalize(text)


    lang = detect_language(clean)


    url_score, url_reasons, urls = check_urls(clean)
    phrase_score, phrase_reasons, matched = match_phrases(clean, lang)
    combo_score, combo_reasons = match_combos(matched)


    weighted = (
        phrase_score * WEIGHTS["phrase"] +
        combo_score  * WEIGHTS["combo"] +
        url_score    * WEIGHTS["url"]
    )
    score = min(int(weighted), 100)


    verify, domains = verify_checklist(text, clean, urls, matched, score)

    return {
        "lang": lang,
        "raw_score": int(phrase_score + combo_score + url_score),
        "score": score,
        "level": level_text(score),
        "reasons": phrase_reasons + combo_reasons + url_reasons,
        "urls": urls,
        "verify": verify,
        "domains": domains,
    }


def level_text(score):
    
    if score >= 70:
        return "高危（强烈疑似钓鱼）"
    elif score >= 40:
        return "可疑（建议谨慎核实）"
    elif score >= 15:
        return "低风险（存在个别可疑信号）"
    else:
        return "基本安全"



if __name__ == "__main__":
    print("=" * 55)
    print("  语盾·农信 LinguaShield Agri —— 双语风险识别与核验辅助")
    print("=" * 55)
    while True:
        user_input = input("\n请输入待检测邮件正文（输入 q 退出）：\n> ")
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
        if result["verify"]:
            print("核验建议：")
            for v in result["verify"]:
                print(f"  → {v}")
        print("-" * 55)
