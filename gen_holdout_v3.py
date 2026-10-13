


import csv
import os

SRC = "自建留出集v3(2026-10-09)"


ROWS = [

    ("en", "留出v3·英文·农业BEC", 1,
     "Subject: factoring arrangement change. Please note our factoring bank has "
     "replaced the collection mandate for palm oil shipments since Monday. All "
     "unpaid invoices must clear to the substituted payee shown underneath. Confine "
     "this information to yourself until we circulate Friday."),

    ("en", "留出v3·英文·农业BEC", 1,
     "Hello Gao, further to the rubber contract negotiations. For the advance to be "
     "released this quarter, remit sixty percent to our Shenzhen office account "
     "straight away. Shenzhen handles the export clearing on our behalf now. Please "
     "handle discreetly, the compliance sign-off is still pending."),

    ("en", "留出v3·英文·农业BEC", 1,
     "Cotton Programme update: the issuing bank has refused presentation of our "
     "documents. Rather than delay the vessel we ask that you pay the balance through "
     "our recovery agent into their nominated holding account. Treat this as urgent "
     "and confidential vis-a-vis your procurement colleagues."),

    ("en", "留出v3·英文·农业BEC", 1,
     "Hi there, we spoke at the aquaculture expo in Xiamen. I am following up from my "
     "private address because our domain is being migrated. We can secure your order "
     "of shrimp starter feed at last year's price if the confirmation amount reaches "
     "today. Contact me on WeChat only please, not through the office."),

    ("en", "留出v3·英文·农业BEC", 1,
     "Selection notice: you have been shortlisted for the South-South cooperation "
     "training programme on forage crops. Before the invitation letter can be issued "
     "the facilitation charge is payable in advance to the programme's handling "
     "account. Slots are released to the waiting list tomorrow evening."),


    ("en", "留出v3·英文·正常农业", 0,
     "Thank you for your enquiry regarding crude palm oil. We can offer 500 MT for "
     "December shipment at competitive terms; please indicate your required "
     "specification for free fatty acid content and we will prepare a full quotation."),

    ("en", "留出v3·英文·正常农业", 0,
     "The rubber inspection report issued by the designated surveyor shows the shipment "
     "meets TSR20 specifications. Original certificates have been sent by courier to "
     "your office and payment will proceed under the existing letter of credit."),

    ("en", "留出v3·英文·正常农业", 0,
     "Shipping advice for your cotton order: loading completed at the port yesterday "
     "and the mate's receipt has been collected. We will forward the full set of "
     "documents once issued by the carrier, estimated within three working days."),

    ("en", "留出v3·英文·正常农业", 0,
     "Congratulations, your nomination to the forage crop training programme has been "
     "accepted by the host institute. Tuition, lodging and local transport are covered "
     "by the programme; participants are not asked to pay any fee to secure a place."),

    ("en", "留出v3·英文·正常农业", 0,
     "Minutes of the demonstration farm steering meeting are attached, covering trial "
     "plot allocation and the irrigation schedule for the coming season. Comments on "
     "the draft work plan are welcome before the steering committee reconvenes."),


    ("zh", "留出v3·中文·农业BEC", 1,
     "陈总您好，关于棕榈油尾款：我司保理银行已于本周一接手收款事宜，"
     "原账户不再使用，未结发票请支付至下方替补收款人。此项调整在周五正式发文前"
     "请仅限于您本人知晓。"),

    ("zh", "留出v3·中文·农业BEC", 1,
     "您好，橡胶合同履行在即，为使预付款本季度得以释放，请即刻支付百分之六十"
     "至我司深圳办事处账户，目前报关由深圳方面代为办理。此事请谨慎处理，"
     "合规批复尚未下达，不宜对外。"),

    ("zh", "留出v3·中文·农业BEC", 1,
     "棉花项下通知：开证行已退回我方交单，为避免船期延误，请通过我方催收代理"
     "将余款汇入其指定代管账户。时间紧迫，此事请勿与贵司采购同事提及。"),

    ("zh", "留出v3·中文·农业BEC", 1,
     "关于南南合作饲草培训班的入选通知：您已进入遴选名单，"
     "邀请函签发前需先向项目承办账户支付资料服务费，名额将於明晚释放至候补名单。"),

    ("zh", "留出v3·中文·农业BEC", 1,
     "王工你好，厦门水产展会上我们见过。公司域名正在迁移，先用私人邮箱联系你。"
     "虾苗开口料订单可按去年价格锁定，今天是最后的确认窗口，"
     "请通过微信单独回复我，不要走公司邮箱。"),


    ("zh", "留出v3·中文·正常农业", 0,
     "感谢贵司对毛棕榈油的询盘。我司可供应十二月船期五百吨，"
     "请告知所需游离脂肪酸含量指标，以便我方出具完整报价方案。"),

    ("zh", "留出v3·中文·正常农业", 0,
     "本批橡胶经第三方检验机构检测符合 TSR20 标准，"
     "正本证书已快递寄往贵司办公室，货款将按既有信用证项下支付。"),

    ("zh", "留出v3·中文·正常农业", 0,
     "棉花装运通知：昨日已完成装船并取回大副收据，"
     "全套单据将在承运人签发后转发贵司，预计三个工作日内提供。"),

    ("zh", "留出v3·中文·正常农业", 0,
     "祝贺贵单位人员入选本期援外饲草技术培训班。学费、住宿与当地交通"
     "均由项目承担，主办方不会以任何名义要求参训人员先行缴费。"),

    ("zh", "留出v3·中文·正常农业", 0,
     "现将示范农场指导委员会会议纪要附上，内容涵盖试验小区划分与"
     "下一季灌溉安排，请在工作计划草案定稿前反馈修改意见。"),
]


def main():
    os.makedirs("holdout", exist_ok=True)
    path = os.path.join("holdout", "holdout_v3.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "lang", "scene", "is_phish", "text", "source", "note"])
        for i, (lang, scene, is_phish, text) in enumerate(ROWS, start=1):
            w.writerow([f"H3{i:02d}", lang, scene, str(is_phish), text, SRC, ""])

    phish = sum(1 for r in ROWS if r[2] == 1)
    en = sum(1 for r in ROWS if r[0] == "en")
    print(f"已生成留出集 v3：{len(ROWS)} 条 -> {path}")
    print(f"  钓鱼 {phish} 条 / 正常 {len(ROWS) - phish} 条　"
          f"英文 {en} 条 / 中文 {len(ROWS) - en} 条")
    print()
    print("★ 纪律提醒：v3 只用于检验。跑完之后请勿用它回头调规则，")
    print("  否则它需要被 v4 替代。")


if __name__ == "__main__":
    main()
