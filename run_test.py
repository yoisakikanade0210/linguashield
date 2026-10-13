


from engine import analyze



CASES = [

    ("A1", "\u3010农业BEC\u3011冒充采购商改收款账户 + 要求保密（AA22-340A 头号手法）",
     "Dear Partner, following our agricultural cooperation agreement, we have changed "
     "our bank account. Please remit the balance payment to the new beneficiary account "
     "below and keep this confidential. Urgent transfer required.", "\u9ad8\u5371"),

    ("A2", "\u3010农业BEC\u3011冒充高管在外考察，要求保密转账",
     "Chen, this is Wang Sicheng speaking. I am in transit for the fertilizer joint "
     "venture signing and cannot be reached by phone. Please arrange a confidential "
     "transfer of RMB 480,000 to this account for the government liaison payment. "
     "Keep strictly confidential, nobody else has been informed.", "\u53ef\u7591"),

    ("A3", "\u3010农业BEC\u3011以\u201c检疫费未到账\u201d扣住证书索取费用",
     "Your phytosanitary certificate could not be issued because the inspection fee "
     "has not been received. Until payment reaches our designated office account the "
     "consignment stays bonded at origin. Remit today and send proof.", "\u53ef\u7591"),

    ("A4", "\u3010农业BEC\u3011逾期恐吓 + 引导到陌生支付通道",
     "Your payment for the poultry feed consignment is overdue. If settlement is not "
     "received within six hours your company will be reported to the export blacklist "
     "and legal action follows. Settle immediately through our updated payment "
     "channel: http://agri-settle-now.xyz", "\u53ef\u7591"),

    ("A5", "\u3010中文·农业BEC\u3011技术合作掩护下的资金归集改路径",
     "\u8d22\u52a1\u4f60\u597d\uff0c\u672c\u5468\u8d77\u6211\u53f8\u5e94\u6536\u8d26\u6b3e\u7531\u96c6\u56e2\u8d44\u91d1\u4e2d\u5fc3\u7edf\u4e00\u5f52\u96c6\uff0c\u6536\u6b3e\u8def\u5f84\u5df2\u8c03\u6574\uff0c"
     "\u672a\u7ed3\u4f59\u989d\u8bf7\u6c47\u5165\u4ee5\u4e0b\u8d26\u6237\uff0c\u6b64\u9879\u8c03\u6574\u5728\u6b63\u5f0f\u516c\u544a\u524d\u8bf7\u52ff\u5916\u4f20\u3002", "\u53ef\u7591"),

    ("A8", "\u3010农业BEC\u3011单据陷阱：提单有错 \u2192 索取银行凭证",
     "Important: your bill of lading draft contains errors. Download the corrected "
     "copy from our portal and re-confirm your banking credentials so the documents "
     "can be released: http://agri-docs-verify.top/bl", "\u53ef\u7591"),


    ("C1", "\u3010中文·农业BEC\u3011变更收款账户 + 要求保密（AA22-340A 头号手法）",
     "\u5f20\u603b\u60a8\u597d\uff0c\u6211\u65b9\u519c\u4e1a\u5408\u4f5c\u8ba2\u5355\u5df2\u786e\u8ba4\u3002\u56e0\u516c\u53f8\u8d26\u6237\u8c03\u6574\uff0c\u73b0\u53d8\u66f4\u6536\u6b3e\u8d26\u6237\uff0c"
     "\u8bf7\u5c06\u5c3e\u6b3e\u6253\u6b3e\u5230\u4ee5\u4e0b\u8d26\u6237\uff0c\u6b64\u4e8b\u52a1\u5fc5\u4fdd\u5bc6\uff0c\u6293\u7d27\u65f6\u95f4\u529e\u7406\u3002", "\u9ad8\u5371"),

    ("C2", "\u3010中文·农业BEC\u3011预付保证金 + 紧急施压",
     "\u6211\u65b9\u73b0\u6709\u4e00\u7b14\u6709\u673a\u80da\u5927\u989d\u8ba2\u5355\uff0c\u6570\u91cf\u6709\u9650\uff0c\u9700\u5148\u652f\u4ed8\u8ba2\u91d1\u9501\u5b9a\u4ea7\u80fd\uff0c"
     "\u8bf7\u4e8e\u4e8c\u5341\u56db\u5c0f\u65f6\u5185\u6c47\u81f3\u6307\u5b9a\u8d26\u6237\uff0c\u903e\u671f\u540d\u989d\u5c06\u88ab\u5176\u4ed6\u4f9b\u5e94\u5546\u5360\u7528\uff0c\u6293\u7d27\u65f6\u95f4\u3002", "\u53ef\u7591"),


    ("A6", "\u3010正常农业\u3011真实单证往来 —— 应当放行：同样提到形式发票/信用证/银行信息，但没有\u201c变更\u201d语义",
     "\u73b0\u5c06\u56db\u5341\u5428\u590d\u5408\u80a5\u7684\u5f62\u5f0f\u53d1\u7968\u4e0e\u6211\u53f8\u94f6\u884c\u4fe1\u606f\u4e00\u5e76\u9644\u4e0a\uff0c"
     "\u8bf7\u6309\u5408\u540c\u7ea6\u5b9a\u901a\u8fc7\u4e0d\u53ef\u64a4\u9500\u5373\u671f\u4fe1\u7528\u8bc1\u7ed3\u7b97\uff0c\u786e\u5b9a\u5f00\u8bc1\u884c\u540e\u8bf7\u544a\u77e5\uff0c\u8c22\u8c22\u3002", "\u57fa\u672c\u5b89\u5168"),

    ("A7", "\u3010正常农业\u3011银行到单通知 —— 明确写\u201c账户未变更\u201d，应放行",
     "\u6211\u884c\u901a\u77e5\uff1a\u8d35\u53f8\u4fe1\u7528\u8bc1\u9879\u4e0b\u5355\u636e\u5df2\u6536\u59df\uff0c\u6b63\u5728\u5ba1\u5355\u3002\u5982\u53d1\u73b0\u4e0d\u7b26\u70b9\u5c06\u53e6\u884c\u544a\u77e5\u3002"
     "\u6211\u53f8\u6536\u6b3e\u8d26\u6237\u672c\u5b63\u5ea6\u672a\u6709\u53d8\u66f4\uff0c\u8bf7\u60a8\u653e\u5fc3\u3002", "\u57fa\u672c\u5b89\u5168"),

    ("E4", "\u3010正常农业\u3011英文合作交流邮件（应放行）",
     "Dear colleague, further to our discussion on juncao cultivation, our delegation "
     "will visit Fujian in December. Attached is a draft programme; please suggest any "
     "additions that would suit your research team.", "\u57fa\u672c\u5b89\u5168"),

    ("C3", "\u3010正常农业\u3011中文询盘报价（应放行）",
     "\u5f20\u5973\u58eb\u60a8\u597d\uff0c\u611f\u8c22\u6765\u51fd\u8be2\u95ee\u6cb9\u8336\u79cd\u5b50\u3002\u73b0\u62a5\u4ef7 FOB \u53a6\u95e8\u6bcf\u516c\u65a4\u56db\u5341\u516d\u5143\uff0c"
     "\u8d77\u8ba2\u4e8c\u767e\u516c\u65a4\uff0c\u62a5\u4ef7\u6709\u6548\u671f\u5341\u4e94\u5929\uff0c\u786e\u8ba4\u540e\u6211\u65b9\u51fa\u5177\u6b63\u5f0f\u53d1\u7968\u3002", "\u57fa\u672c\u5b89\u5168"),


    ("E3", "\u3010农业BEC\u00b7规避手法\u3011零宽字符 + 全角空格伪装账户变更",
     "Dear Partner, we noticed unusual activity on your agri\u200b-export trading account. "
     "Your account\u3000has\u3000been\u3000changed. Please re\u200b-confirm your banking "
     "credentials and update your payment immediately: http://micr0soft-agri-secure.tk/login", "\u9ad8\u5371"),
]



def run():
    lines = []
    ok = 0

    def out(s=""):
        print(s)
        lines.append(s)

    out("=" * 68)
    out("  语盾·农信 LinguaShield Agri 原型 · 现场演示样本验证报告")
    out(f"  （共 {len(CASES)} 条：纯农业国际合作场景演示）")
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

        if r.get("verify"):
            out("  核验建议：")
            for v in r["verify"]:
                out(f"    → {v}")

    out("")
    out("=" * 68)
    out(f"  结果：{ok}/{len(CASES)} 条符合预期")
    out("=" * 68)

    with open("测试报告.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n>>> 已生成 测试报告.txt")


if __name__ == "__main__":
    run()
