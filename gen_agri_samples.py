# -*- coding: utf-8 -*-
"""
gen_agri_samples.py —— 「语盾·农信」农业国际合作邮件样本生成脚本
======================================================================
用途：把农业国际合作场景的测试样本（S105 起）**追加**到 samples.csv，
      不改动 S001~S104 的任何内容。

为什么单独写一个脚本，而不是改 gen_samples.py？
  · gen_samples.py 是"基础 100 条"的生成器，末尾有 assert len(rows) == 100，
    它的职责是"造出 100 条基线"。往它里面塞农业样本会破坏它的自洽性。
  · 农业样本是**增量**，且带独立的来源标注（FBI AA22-340A 场景），
    单独成脚本更清晰，也能反复重跑而不影响基线。

运行：python gen_agri_samples.py
输出：samples.csv（追加 S105~S1xx）

设计依据：
  FBI / FDA-OIC / USDA 联合公告 AA22-340A（2022-12）
  点名"农业与食品供应链"为 BEC（商务邮件诈骗）高发领域。
  四大典型 TTP：
    ① 变更收款账户（Change of bank account）
    ② 伪造紧急大额订单（Urgent large order）
    ③ 修改收货地址/物流改道（Reroute shipment）
    ④ 冒充高管/合作方要求保密（Executive impersonation + secrecy）
"""

import csv

SRC = "自建测试集·农业国际合作(2026-10-02)"

# (lang, scene, is_phish, text)
AGRI_ROWS = [
    # ============================================================
    # 一、英文钓鱼：农业国际合作 BEC（仿 AA22-340A 四大 TTP）
    # ============================================================
    ("en", "英文·农业BEC", 1,
     "Dear Partner, following our agricultural cooperation agreement, we have changed "
     "our bank account. Please remit the balance payment to the new beneficiary account "
     "below and keep this confidential. Urgent transfer required."),

    ("en", "英文·农业BEC", 1,
     "Dear Sir, this is the CEO of the trading company. We are closing a bulk order of "
     "fresh produce this week. Our new bank account details are attached. Do not inform "
     "the sales team, this is confidential. Act now to avoid delay."),

    ("en", "英文·农业BEC", 1,
     "We need to update our payment details for the agricultural products order. "
     "Please use the offshore account below for the advance payment. This must be "
     "done within 24 hours. Contact me on my new number, not the office."),

    ("en", "英文·农业BEC", 1,
     "Notification of change of beneficiary: our remittance account has been updated. "
     "Send the wire transfer to the third-party account provided. Keep this confidential "
     "and confirm immediately."),

    ("en", "英文·农业BEC", 1,
     "Dear supplier, we have revised payment details for the cold chain shipment. "
     "Please pay the deposit to the account below. This is urgent and must be kept "
     "confidential until the contract is signed."),

    ("en", "英文·农业BEC", 1,
     "Change of shipping address: the final destination port has been changed. "
     "Also note our updated bank details for the letter of credit amendment. "
     "Process the payment today. http://agri-trade-secure.xyz/payment"),

    ("en", "英文·农业BEC", 1,
     "Dear Manager, urgent: the agricultural cooperation fund has been approved. "
     "Pay the processing fee of USD 1,200 to our offshore account to release the bulk "
     "order. Expires today. Do not discuss with colleagues."),

    ("en", "英文·农业BEC", 1,
     "This is to inform you that our company has changed our bank account for all "
     "future agricultural transactions. Kindly update your records and send the payment "
     "for the trial order to the intermediary bank account listed."),

    ("en", "英文·农业BEC", 1,
     "Dear Customer, we noticed unusual activity on your agri-export trading account. "
     "Your account has been suspended. Verify your account and update your payment "
     "information within 12 hours: http://micr0soft-agri-secure.tk/login"),

    ("en", "英文·农业BEC", 1,
     "We are a large agricultural importer and wish to place a bulk order. However, "
     "before shipment we require an advance payment to our new agent account to cover "
     "customs clearance. Keep this confidential. Please act immediately."),

    # ============================================================
    # 二、英文正常：真实的农业国际合作往来邮件（应放行）
    #    这些是最容易误报的一类 —— 它们必然含大量农业术语，
    #    所以专门造出来验证"压不压低基础分"这个设计是对的。
    # ============================================================
    ("en", "英文·正常农业", 0,
     "Dear Partner, please find attached the proforma invoice and bill of lading for "
     "our bulk order of fresh produce. Payment will be settled by letter of credit at "
     "sight as per the contract. Let us know if the documents are in order."),

    ("en", "英文·正常农业", 0,
     "Thank you for your interest in our agricultural cooperation program. We have "
     "received your inquiry about cold chain logistics for agricultural products. "
     "Our export team will reply with a formal quotation within three working days."),

    ("en", "英文·正常农业", 0,
     "The phytosanitary certificate and customs clearance documents for the shipment "
     "are being prepared. We will forward them once issued by the inspection authority. "
     "No payment action is required from your side at this stage."),

    ("en", "英文·正常农业", 0,
     "We confirm receipt of your trial order for agricultural products. The goods will "
     "be shipped from the port of destination next month. Please review the attached "
     "contract terms at your convenience."),

    ("en", "英文·正常农业", 0,
     "Dear colleague, our delegation will visit your institute next month to discuss "
     "agricultural cooperation on crop breeding. We would be glad to arrange a meeting "
     "at your convenience. Attached is the draft agenda."),

    ("en", "英文·正常农业", 0,
     "The 2027 international symposium on agricultural trade will be held in Fuzhou. "
     "Researchers and exporters are welcome to submit abstracts. No registration fee is "
     "required for invited speakers."),

    ("en", "英文·正常农业", 0,
     "Regarding the agricultural products shipment, our quality inspection report shows "
     "all items meet the contract standard. The bank will release the payment upon "
     "receipt of the shipping documents under the letter of credit."),

    ("en", "英文·正常农业", 0,
     "We appreciate your long-standing cooperation on agricultural trade. The summary "
     "of last season's orders is attached for your reference. Please advise if any "
     "adjustment is needed for the coming season."),

    # ============================================================
    # 三、中文钓鱼：冒充采购商/合作方（中文侧 BEC）
    # ============================================================
    ("zh", "中文·农业BEC", 1,
     "张总您好，我方农业合作订单已确认。因公司账户调整，现变更收款账户，"
     "请将尾款打款到以下账户，此事务必保密，抓紧时间办理。"),

    ("zh", "中文·农业BEC", 1,
     "您好，我们是大宗农产品采购方，现有一批冷链订单需要紧急下单。"
     "请先支付订金到我们新开通的离岸账户，名额有限，过期作废，不要声张。"),

    ("zh", "中文·农业BEC", 1,
     "关于供货合同：我方收款账户变更，请把预付货款汇款至以下新的收款账户。"
     "原账户已停用，请立即更新银行信息，耽误发货责任自负。"),

    ("zh", "中文·农业BEC", 1,
     "李经理你好，我是对方公司财务。农产品出口的信用证需要修改，"
     "请把保证金转到指定第三方账户，此事保密处理，抓紧时间转账。"),

    ("zh", "中文·农业BEC", 1,
     "紧急通知：农业合作项目款已批，需先缴纳手续费才能放行大宗订单。"
     "请汇款至以下账户，今天最后一天，请勿告知其他同事。"),

    ("zh", "中文·农业BEC", 1,
     "您好，我方采购农产品样品，需先支付样品费并更换收款人。"
     "请按新账户打款到这个账户，尽快办理，名额有限。"),

    # ============================================================
    # 四、中文正常：真实涉农业务往来（应放行）
    # ============================================================
    ("zh", "中文·正常农业", 0,
     "您好，本批农产品出口所需的形式发票与提单已发送，请按即期信用证结算，"
     "如有疑问请与我司外贸部联系，谢谢。"),

    ("zh", "中文·正常农业", 0,
     "关于农业合作事宜：我方合作社的种植基地本季产量稳定，可保障订单农业供货。"
     "详情见附件合同，欢迎来函洽谈。"),

    ("zh", "中文·正常农业", 0,
     "感谢贵司长期以来的农产品采购合作。现将上一季度订单结算明细发送给您，"
     "请核对后回复确认，若有异议请及时告知。"),

    ("zh", "中文·正常农业", 0,
     "通知：冷链物流车辆安排已确认，本批农产品将于下周抵达目的港。"
     "报关与清关文件由我司负责准备，无需贵方额外出资。"),

    ("zh", "中文·正常农业", 0,
     "我院拟于下月举办农业国际合作交流会，围绕农产品出口与冷链技术展开研讨。"
     "诚邀贵单位派员参加，会议不收取任何费用。"),

    ("zh", "中文·正常农业", 0,
     "关于供货商资质审核：请贵司提供营业执照与产品质检报告复印件，"
     "用于我方内部备案，谢谢配合。"),
]

# ============ 追加写入 CSV（不改动已有行）============
rows = []
with open("samples.csv", "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    for r in reader:
        if r and r[0].strip():     # 跳过空行
            rows.append(r)

start = len(rows) + 1              # 新编号从 S105 开始
added = 0
for lang, scene, is_phish, text in AGRI_ROWS:
    rows.append([f"S{start + added:03d}", lang, scene, str(is_phish), text, SRC, ""])
    added += 1

with open("samples.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

phish = sum(1 for r in rows if r[3] == "1")
en = sum(1 for r in rows if r[1] == "en")
print(f"已追加 {added} 条农业样本到 samples.csv（编号 S{start:03d}~S{start + added - 1:03d}）")
print(f"  当前总计 {len(rows)} 条：钓鱼 {phish} 条 / 正常 {len(rows) - phish} 条")
print(f"  英文 {en} 条 / 中文 {len(rows) - en} 条")
