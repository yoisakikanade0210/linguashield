# -*- coding: utf-8 -*-
"""
run_test.py —— 语盾原型 8 样本验证
=====================================
用途：给指导老师看"原型确实能跑通"。
运行：python run_test.py
输出：控制台逐条打印 + 同目录生成 测试报告.txt
"""

from engine import analyze

# (编号, 场景名, 文本, 期望等级关键词)
# 期望只写 "高危" / "可疑" / "低风险" / "基本安全" 四档之一
CASES = [
    # ---------- 英文 4 条 ----------
    ("E1", "英文·账号盗取（仿冒 PayPal + 短链）",
     "Dear Customer, we noticed suspicious activity on your PayPal account. "
     "Your account has been suspended. Please verify your account within 24 hours: "
     "https://bit.ly/3xK9pQz", "高危"),

    ("E2", "英文·学术诈骗（掠夺性会议征稿）",
     "Dear Scholar, Your paper has been selected by the review committee. "
     "Call for Papers: submit your manuscript and pay the fee of USD 450 "
     "(non-refundable) to confirm the keynote speaker invitation. "
     "Impact factor guaranteed. http://int-conf-edu.xyz/submit", "高危"),

    ("E3", "英文·规避手法（零宽字符 + 全角空格）",
     "Your acc​ount　is　suspended. Verify your identity immediately at "
     "http://paypa1-secure.tk/login", "高危"),

    ("E4", "英文·正常邮件（真实学术会议通知，应放行）",
     "Dear Professor, thank you for your submission to the 2026 International "
     "Conference on Applied Linguistics. The review committee has completed the "
     "evaluation. Please find the attached review comments.", "基本安全"),

    # ---------- 中文 4 条 ----------
    ("C1", "中文·冒充辅导员 + 助学金套取",
     "同学你好，我是辅导员李老师。你的助学金申请已通过，请立即点击链接填写"
     "身份证号和银行卡号，验证码稍后发送。名额有限，抓紧时间办理，不要告诉他人。", "高危"),

    ("C2", "中文·校园贷 + 紧急施压",
     "教务处通知：为保障学籍，需缴纳保证金。校园贷额度已开放，名额有限，"
     "请在最后一天前完成转账。", "高危"),

    ("C3", "中文·正常通知（真实奖学金公示，应放行）",
     "各位同学：本学期奖学金评定结果已在教务处官网公示，请自行登录教务系统查看。", "基本安全"),

    ("C4", "中文·学术诈骗（版面费催收）",
     "您的论文已被录用，请缴纳版面费 800 元至指定账户，过期作废。"
     "快速发表，保密处理。", "高危"),
]


def run():
    lines = []
    ok = 0

    def out(s=""):
        print(s)
        lines.append(s)

    out("=" * 68)
    out("  语盾 LinguaShield 原型 · 8 样本验证报告")
    out("=" * 68)

    for cid, name, text, expect in CASES:
        r = analyze(text)
        hit = r["level"].startswith(expect)
        ok += 1 if hit else 0
        out("")
        out(f"[{cid}] {name}")
        out(f"  判定语言：{r['lang']}    风险分：{r['score']}/100")
        out(f"  判定等级：{r['level']}    期望：{expect}    {'✓ 通过' if hit else '✗ 未通过'}")
        if r["urls"]:
            out(f"  提取 URL：{r['urls']}")
        out("  判定理由：")
        if r["reasons"]:
            for x in r["reasons"]:
                out(f"    · {x}")
        else:
            out("    （无异常信号）")

    out("")
    out("=" * 68)
    out(f"  结果：{ok}/{len(CASES)} 条符合预期")
    out("=" * 68)

    with open("测试报告.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n>>> 已生成 测试报告.txt")


if __name__ == "__main__":
    run()
