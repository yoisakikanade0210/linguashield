


import csv
import os

SRC = "自建测试集·农业国际合作(2026-10-09)"
SRC_LEGACY = "自建测试集(2026-10-01)"



LEGACY_MAX_ID = 134



CONTROL_KEEP = {

    "S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008",

    "S011", "S012", "S013", "S014",

    "S023", "S024", "S025", "S026", "S027", "S028",

    "S033", "S034", "S035", "S036",

    "S101", "S102",

    "S041", "S042", "S043", "S044", "S045", "S046", "S047", "S048",

    "S071", "S072", "S073", "S074", "S075", "S076", "S077", "S078",


    "S086",
}





EN_PHISH = [

    ("农业BEC·账户变更", 1,
     "Dear Mr. Lin, regarding proforma invoice PI-FJ-2261 for 60 MT of urea, "
     "please be advised that our bank mandates were rearranged after this year's "
     "annual review. Kindly remit the 30 percent deposit to the revised beneficiary "
     "below and update your records accordingly. Please keep this confidential until "
     "our internal audit is closed."),

    ("农业BEC·账户变更", 1,
     "Notice to all partners: following our group restructuring, payments for "
     "agricultural machinery spare parts are now routed through our newly designated "
     "account. Earlier instructions are void with immediate effect and should be "
     "discarded."),

    ("农业BEC·账户变更", 1,
     "Dear team, our receiving bank finished a platform migration on Monday, so the "
     "remittance coordinates for the tea shipment have been updated. Use the details "
     "below to settle the outstanding amount. Kindly confirm once done and keep this "
     "confidential until the migration is announced."),


    ("农业BEC·预付保证金", 1,
     "Dear supplier, we are glad to confirm a bulk order of 2,400 cartons of frozen "
     "tilapia for Dakar. To lock the production slot, an advance payment to our "
     "designated agent account is required within 24 hours. Failure to pay today will "
     "release the slot to the next bidder."),

    ("农业BEC·预付保证金", 1,
     "Urgent: the Turkish buyer has accepted your citrus quotation, but customs "
     "bonding requires a refundable security deposit to be cleared today. Wire USD "
     "3,200 to our clearance agent account and forward the slip. Do not discuss this "
     "with other departments until reviewed."),


    ("农业BEC·冒充高管", 1,
     "Chen, this is Wang Sicheng speaking. I am in transit for the fertilizer joint "
     "venture signing and cannot be reached by phone. Please arrange a confidential "
     "transfer of RMB 480,000 to this account for the government liaison payment. "
     "Keep strictly confidential, nobody else has been informed."),

    ("农业BEC·冒充高管", 1,
     "I am writing on behalf of the director during his overseas inspection tour. He "
     "has authorised a time-sensitive payment concerning the grain procurement "
     "contract. Please process it quietly today; do not inform the finance department "
     "since this falls outside standard approval."),


    ("农业BEC·物流改道", 1,
     "Routing notice: the discharge port for your cassava shipment has been amended "
     "to Port Klang upon the buyer's instruction. Alongside this, freight and balance "
     "payments must now be settled through the agent account enclosed. Act today to "
     "avoid demurrage."),

    ("农业BEC·物流改道", 1,
     "Dear logistics desk, the consignee and receiving address have been replaced as "
     "of today. Kindly release payment for the re-routing charges to the third-party "
     "account below before 16:00; the container will otherwise remain on the terminal."),


    ("农业BEC·单据陷阱", 1,
     "Dear partner, attached is the revised commercial invoice. Kindly note that due "
     "to a discrepancy raised by the issuing bank, payment under the credit is no "
     "longer available and settlement must be made by telegraphic transfer directly "
     "to our account today. Confirm upon remittance."),

    ("农业BEC·单据陷阱", 1,
     "Important: your bill of lading draft contains errors. Download the corrected "
     "copy from our portal and re-confirm your banking credentials so the documents "
     "can be released: http://agri-docs-verify.top/bl"),


    ("农业BEC·冒充机构", 1,
     "Office of Agricultural Development Grants: we are pleased to inform you that "
     "your cross-border demonstration farm project has been pre-approved. To finalise "
     "disbursement, a one-time administrative charge of USD 780 should be paid through "
     "our appointed processing agent. Today is the last day."),

    ("农业BEC·冒充机构", 1,
     "International Agri Expo committee: your booth application is confirmed, however "
     "the space allocation fee has to be settled today to the account below. We cannot "
     "accept payment on site. Do not share this with your sales manager yet."),

    ("农业BEC·冒充机构", 1,
     "Hi, this is Kevin from purchasing, writing from my personal mailbox because the "
     "office server is down. We need to place an order for 12 tonnes of mushrooms "
     "before tonight's cutoff. The agent asks for 40 percent upfront. Please confirm "
     "receipt and keep this arrangement private."),


    ("农业BEC·费用索取", 1,
     "Re: crop insurance claim CLI-2026-339. Your hail damage claim has been assessed "
     "and approved. A release fee of USD 1,150 is payable to the adjusters' account "
     "before funds can be transmitted. Please pay promptly, the file closes tomorrow."),

    ("农业BEC·保证金索取", 1,
     "Performance bond refund notice: to unlock the security deposit from our joint "
     "bid, a verification amount must be remitted to the trustee account. It is fully "
     "reimbursable upon completion. Keep this confidential to protect our commercial "
     "position."),


    ("农业BEC·账户变更", 1,
     "Following the complaints about the contaminated fertilizer batch, we have "
     "authorised a full refund. Please note our account details have changed; provide "
     "your account information and the refund will be released once the administrative "
     "handling charge is settled."),


    ("农业BEC·账户恐吓", 1,
     "Your payment for the poultry feed consignment is overdue. If settlement is not "
     "received within six hours your company will be reported to the export blacklist "
     "and legal action follows. Settle immediately through our updated payment "
     "channel: http://agri-settle-now.xyz"),


    ("农业BEC·账户变更", 1,
     "Morning all, quick correction to the wiring instructions circulated earlier this "
     "week: our principal account is under review, so please redirect today's "
     "settlement to the interim account listed below. Ignore any earlier details."),


    ("农业BEC·物流改道", 1,
     "URGENT: container MSKU-7742190 holding your grain shipment is accruing demurrage "
     "at the discharge port. Pay the outstanding amount to the terminal agent account "
     "within twelve hours or the cargo will be auctioned. No further notice."),


    ("农业BEC·费用索取", 1,
     "Your phytosanitary certificate could not be issued because the inspection fee "
     "has not been received. Until payment reaches our designated office account the "
     "consignment stays bonded at origin. Remit today and send proof."),


    ("农业BEC·账户恐吓", 1,
     "Security alert: unusual activity detected on your export settlement account. "
     "Your trading account has been locked. Verify your account and re-submit your "
     "payment details to retain access: http://agri-bank-verify.tk/login"),


    ("农业BEC·费用索取", 1,
     "Regarding the import licence for your crop protection products, renewal requires "
     "immediate settlement of the registration levy through the consulting firm "
     "handling our file. Kindly remit to the nominated account and forward the slip "
     "today before close of business."),


    ("农业BEC·账户变更", 1,
     "Dear finance desk, effective this week our receivable cycles are handled by the "
     "group treasury; consequently the remittance path has been changed. Outstanding "
     "balances should clear to the coordinates below. We ask you to keep this "
     "confidential until the migration is complete."),


    ("农业BEC·预付保证金", 1,
     "Last call: the Jakarta buyer's edible fungus allocation closes tonight at "
     "midnight. Secure your share by paying the reservation amount to our holding "
     "account now. This arrangement is not for general circulation; reply only to me."),
]


EN_NORM = [
    ("正常农业·询盘报价", 0,
     "Dear Ms. Zhang, thank you for your enquiry on hybrid vegetable seeds. We quote "
     "USD 46.00 per kilogram FOB Xiamen for the 200 kg trial lot. This quotation stays "
     "valid for fifteen days and a formal invoice will follow upon your confirmation."),

    ("正常农业·单证结算", 0,
     "Attached please find the proforma invoice for 40 MT of compound fertilizer NPK "
     "15-15-15 together with our bank particulars. Payment is to be effected by an "
     "irrevocable letter of credit at sight. Please advise your issuing bank upon "
     "receipt."),

    ("正常农业·单证结算", 0,
     "The phytosanitary certificate for the pomelo consignment is being processed by "
     "the local inspection office. Issuance is expected next Tuesday and the original "
     "will travel together with the certificate of origin. No action is required from "
     "your side meanwhile."),

    ("正常农业·单证结算", 0,
     "Please review the draft certificate of origin. The consignee should read "
     "AL-MAYA TRADING LLC exactly as registered on their import licence. Kindly "
     "confirm so we can finalise before the vessel sails."),

    ("正常农业·单证结算", 0,
     "The bill of lading draft for MV Cape Harbour v.126 is enclosed. Please check the "
     "notify party and the description of goods; once confirmed we will instruct the "
     "carrier to release originals against payment under the credit."),

    ("正常农业·物流履约", 0,
     "Shipment advice: booking is confirmed with the carrier, ETA Rotterdam 14 "
     "November. We will share tracking references and the packing list once the "
     "container is gated in at origin."),

    ("正常农业·物流履约", 0,
     "Quality control results for the mung bean lot show moisture at 12.4 percent and "
     "purity at 99.1 percent, both within contract specification. The inspection "
     "certificate is attached for your records."),

    ("正常农业·询盘报价", 0,
     "Regarding the draft contract we propose payment by transferable letter of credit "
     "payable sixty days after bill of lading date. Please let us know whether this "
     "aligns with your credit policy before we finalise the wording."),

    ("正常农业·合作交流", 0,
     "Dear colleague, further to our discussion on juncao cultivation, our delegation "
     "will visit Fujian in December. Attached is a draft programme; please suggest "
     "any additions that would suit your research team."),

    ("正常农业·合作交流", 0,
     "The international symposium on tropical agriculture will convene in Nanning next "
     "March. The organising committee invites submissions through the official "
     "website; no submission fee applies to selected papers."),

    ("正常农业·会展通知", 0,
     "You are cordially invited to the Fujian Agricultural Trade Fair. Partner booths "
     "are arranged through the provincial trade office, and registration is completed "
     "at the official portal. No payment is ever requested by email."),

    ("正常农业·询盘报价", 0,
     "We acknowledge receipt of purchase order PO-2026-1188 for 500 units of "
     "irrigation fittings. Production is scheduled for next month and we will advise "
     "the ex-factory date in due course."),

    ("正常农业·物流履约", 0,
     "Two kilograms of the camellia seed sample will leave our warehouse by courier "
     "tomorrow. The airway bill number will follow once booked; please arrange the "
     "import permit at your end ahead of arrival."),

    ("正常农业·物流履约", 0,
     "Cold chain arrangements for the citrus are in place: the reefer is set at four "
     "degrees with controlled atmosphere. We will monitor temperature throughout the "
     "voyage and share the log upon arrival."),

    ("正常农业·合作交流", 0,
     "We would be glad to receive your technical team for a factory visit in early "
     "December, including a tour of the processing line and a tasting session of our "
     "new dried products."),

    ("正常农业·单证结算", 0,
     "Attached is the annual reconciliation statement covering all shipments settled "
     "this season. Kindly review the figures and confirm by return; any discrepancy "
     "will be checked against our shipping documents."),


    ("正常农业·单证结算", 0,
     "Notice from our bank: documents presented under your letter of credit have been "
     "received and are under examination. We will notify you should any discrepancy "
     "arise. Our beneficiary details remain unchanged this season."),

    ("正常农业·会展通知", 0,
     "The provincial agriculture bureau has published the list of enterprises eligible "
     "for machinery purchase subsidies. Disbursement will be made to the accounts "
     "already on file with the bureau; no application fee is charged at any stage."),

    ("正常农业·物流履约", 0,
     "Customs clearance: please upload the supplementary documents through your "
     "broker's official portal. The consignment was selected for routine inspection "
     "only and no additional charges have been assessed."),

    ("正常农业·合作交流", 0,
     "Regarding pesticide registration, the dossier requires toxicology reports and "
     "residue data from two growing seasons. We shall prepare the materials and submit "
     "them once the local trials conclude."),

    ("正常农业·单证结算", 0,
     "Your seed export permit application is under quarantine review, decision expected "
     "within ten working days. We will forward the approval notice as soon as it is "
     "released by the authority."),

    ("正常农业·合作交流", 0,
     "Enclosed is the draft supply agreement between our cooperative and your company, "
     "covering volumes, quality standards and delivery windows. Comments are welcome "
     "before the next round of negotiation."),

    ("正常农业·合作交流", 0,
     "We acknowledge your request for soil analysis. The quotation covers macronutrient "
     "testing and heavy metal screening for twenty-four samples; the report will be "
     "issued within two weeks of receipt."),

    ("正常农业·询盘报价", 0,
     "Please quote spare parts for the combine harvester model 4LZ-6.0, specifically "
     "the cutter bar and the threshing drum. Serial numbers are listed in the attached "
     "table for reference."),


    ("正常农业·单证结算", 0,
     "Following your request we confirm our banking particulars for this contract: "
     "account name Fujian Greenfield Agri-Export Co., Ltd, SWIFT BKCHCNBJ720. These "
     "coordinates have been used for every shipment this season and remain valid; "
     "nothing has been revised."),
]


ZH_PHISH = [

    ("农业BEC·账户变更", 1,
     "陈经理您好，关于杂交水稻种子订单（合同号 HT-2026-0817）的尾款，"
     "因公司银行账户年检，收款账户已变更，请按以下新收款账户汇款并更新银行信息。"
     "此事请保密，等内部流程走完再统一通知。"),

    ("农业BEC·账户变更", 1,
     "通知：我集团完成账户体系升级，茶叶出口业务货款的收款账户已调整，"
     "之前提供的银行信息作废，请以后按本邮件的新账户打款，收到后回复确认。"),

    ("农业BEC·账户变更", 1,
     "您好，我行系统正在维护，为不影响如期发货，请先将本批化肥款打入指定第三方账户，"
     "账户变更后我们再补手续。请尽快办理，此项勿向他人透露。"),


    ("农业BEC·预付保证金", 1,
     "我方现有一笔有机肥大额订单，数量有限，需先支付订金锁定产能，"
     "请于二十四小时内汇至指定账户，逾期名额将被其他供应商占用，抓紧时间。"),

    ("农业BEC·预付保证金", 1,
     "您好，现有一批冷冻水产出口订单需要紧急排产，请先预付百分之四十到指定账户，"
     "今天必须到账，名额有限，过期作废，不要声张。"),


    ("农业BEC·冒充高管", 1,
     "小刘，我是王董，正在外地考察不方便电话。现有一笔政府关系的款项需要今天处理，"
     "金额四十八万元，请转到这个账户，此事务必保密，公司其他人都不知道。"),

    ("农业BEC·冒充高管", 1,
     "董事长在外考察期间由我代为传达：农产品采购合同有一笔款项已批准，"
     "请财务今天下午悄悄办理，不要告知财务经理，此事属于特殊审批，抓紧转账。"),


    ("农业BEC·物流改道", 1,
     "您好，应客户要求，本批木薯干的卸货港改至巴生港，同时货代费用由指定代理账户代收，"
     "请按变更后的账户在今天四点前完成付款，否则货柜将继续滞留在码头。"),

    ("农业BEC·物流改道", 1,
     "最新通知：收货地址已变更，尾端派送费用需先支付至指定账户才能安排送货，"
     "请尽快汇款并回传水单，备注不打连云港二字。"),


    ("农业BEC·单据陷阱", 1,
     "您好，信用证出现不符点已被开证行拒付，现改为电汇结算，"
     "请直接汇款至以下账户完成结清，今天补齐即可放单，请马上安排。"),

    ("农业BEC·单据陷阱", 1,
     "重要通知：您的提单确认件存在信息错误，请在二十六日前登录我们的平台核对，"
     "并重新确认您的银行资料以便放单：http://agri-bl-check.top/verify"),


    ("农业BEC·冒充机构", 1,
     "农业农村部项目评审办公室：贵单位跨境示范农场项目已通过初审，"
     "为完成资金拨付，需先缴纳一次性手续费七百八十元至指定代办账户，"
     "今天是最后一天，逾期视为放弃。"),

    ("农业BEC·冒充机构", 1,
     "中国国际农博会组委会：贵司展位已确认，但需在今日缴纳摊位费至以下账户，"
     "现场不接受缴费，请尽快处理，此事暂不要告知贵司销售负责人。"),


    ("农业BEC·冒充机构", 1,
     "你好，我是采购部李经理，公司邮箱有问题用这个私人号联系你。"
     "今晚十二点前有一批食用菌订单要下，需先转代理费到指定账户，"
     "请收到后立刻办理并保持低调。"),


    ("农业BEC·费用索取", 1,
     "关于您的农业保险理赔（理赔号 LP-2026-339）：赔款已核定，"
     "但需先支付公估费一千二百元才能放款，请将费用汇入指定账户，"
     "本周不处理案件即将关闭。"),

    ("农业BEC·保证金索取", 1,
     "关于履约保证金退还：为解冻这笔款项，需先向监管专户汇入一笔验证金，"
     "验证完成后全额退回，请今日内办理，此事务必保密以免影响我司商业安排。"),


    ("农业BEC·账户变更", 1,
     "关于化肥批次质量问题的退款已批准，但因我司账户变更，"
     "请提供您的收款账户并先支付手续费，我们将连同退款一并打给您，请抓紧。"),


    ("农业BEC·账户恐吓", 1,
     "您有一笔饲料货款已逾期，六小时内未处理将上报出口黑名单并启动法律程序，"
     "请立即通过以下付款通道结清：http://agri-settle-now.xyz"),


    ("农业BEC·账户变更", 1,
     "各位好，更正本周早些时候发过的收款信息：我司主账户正在审计，"
     "今天的货款请改打至以下临时账户，之前那条请勿再使用。"),


    ("农业BEC·物流改道", 1,
     "紧急：您名下柜号 MSCU-7742190 的粮食货柜已在目的港产生滞港费，"
     "十二小时内未付清将被拍卖，请尽快汇至码头代理账户，不再另行通知。"),


    ("农业BEC·费用索取", 1,
     "您的植物检疫证书因检疫费未到账而被扣，请今日汇款至指定账户，"
     "否则整批货将继续封存在起运地仓库，由此产生的损失由贵司承担。"),


    ("农业BEC·账户恐吓", 1,
     "安全提醒：监测到您的出口结算账户存在异常登录，为保障资金安全，"
     "账户将于今日被冻结，请立即验证您的账户并重新提交资料："
     "http://agri-bank-verify.tk/login"),


    ("农业BEC·费用索取", 1,
     "关于您农药经营许可证的年审：需通过我方代办机构缴纳年审费，"
     "请汇至以下账户并在今日下班前回传凭据，否则证书将无法如期换发。"),


    ("农业BEC·账户变更", 1,
     "财务你好，本周起我司应收账款由集团资金中心统一归集，收款路径已调整，"
     "未结余额请汇入以下账户，此项调整在正式公告前请勿外传。"),


    ("农业BEC·预付保证金", 1,
     "最后通知：雅加达客户的食用菌名额今晚十二点截止，"
     "请立即支付预留金至我司监管账户锁定配额，此事不宜公开讨论，请单独回复我。"),
]


ZH_NORM = [
    ("正常农业·询盘报价", 0,
     "张女士您好，感谢来函询问油茶种子。现报价 FOB 厦门每公斤四十六元，"
     "起订二百公斤，报价有效期十五天，确认后我方出具正式发票。"),

    ("正常农业·单证结算", 0,
     "现将四十吨复合肥的形式发票与我司银行信息一并附上，"
     "请按合同约定通过不可撤销即期信用证结算，确定开证行后请告知，谢谢。"),

    ("正常农业·单证结算", 0,
     "关于柚子的植物检疫证书，当地检疫机构正在受理，预计下周二出证，"
     "届时连同原产地证一并寄送。此阶段贵方无需任何操作，也不产生费用。"),

    ("正常农业·单证结算", 0,
     "现将原产地证草稿发您核对，收货人名称须与其进口许可证完全一致，"
     "请确认后回复，以便我们在船期前完成出证。"),

    ("正常农业·单证结算", 0,
     "提单确认件已附上，请核对通知人与货物描述，"
     "确认无误后我方将通知船公司在信用证项下放单。"),

    ("正常农业·物流履约", 0,
     "装运通知：舱位已向船公司订妥，预计十一月十四日抵达鹿特丹，"
     "集装箱进场后会即刻提供跟踪号与装箱单。"),

    ("正常农业·物流履约", 0,
     "本批绿豆质检结果：水分百分之十二点四，纯度百分之九十九点一，"
     "均在合同约定范围内，质检证书附后供存档。"),

    ("正常农业·询盘报价", 0,
     "关于合同草稿，我方建议采用提单日后六十天付款的信用证方式结算，"
     "请贵司确认是否符合贵方信贷政策，我们再定最终措辞。"),

    ("正常农业·合作交流", 0,
     "继上次关于菌草栽培的交流，我院代表团拟于十二月访问福建，"
     "现将行程草案附上，欢迎结合贵单位研究安排提出补充建议。"),

    ("正常农业·合作交流", 0,
     "热带农业国际研讨会将于明年三月在南宁召开，"
     "组委会接受通过官网提交的论文，入选论文不收取任何版面费用。"),

    ("正常农业·会展通知", 0,
     "诚邀贵单位参加福建农产品贸易洽谈会。"
     "合作展位由省外贸中心统一安排，报名在官方平台完成，"
     "全程不会通过邮件向您收取任何费用。"),

    ("正常农业·询盘报价", 0,
     "采购订单 PO-2026-1188（灌溉配件五百套）已收悉，"
     "生产安排在次月，出厂日期确定后会第一时间通知贵方。"),

    ("正常农业·物流履约", 0,
     "油茶种子样品两公斤将于明日发出，运单一经预约即发送给您，"
     "请贵方提前办理进口许可以免影响清关。"),

    ("正常农业·物流履约", 0,
     "柑橘冷链方案已确定：冷藏箱设定四摄氏度并采用气调，"
     "全程监控温度，到港后提供完整温控记录。"),

    ("正常农业·合作交流", 0,
     "欢迎贵司技术团队于十二月初来厂参观，"
     "行程包括加工生产线考察以及我司新出干货产品的品鉴。"),

    ("正常农业·单证结算", 0,
     "附上本季度全部已结算货款的年度对账单，请核对数据后回复确认，"
     "如有出入我们将对照全套货运单据逐笔核查。"),


    ("正常农业·单证结算", 0,
     "我行通知：贵司信用证项下单据已收妥，正在审单。"
     "如发现不符点将另行告知。我司收款账户本季度未有变更，请您放心。"),

    ("正常农业·会展通知", 0,
     "省农业农村厅已公示农机购置补贴企业名单，"
     "补助资金将拨付至各企业在厅里备案的既有账户，申报全程不收取费用。"),

    ("正常农业·物流履约", 0,
     "关于报关事宜：请通过贵司报关行的官方平台上传补充单证。"
     "本批货物仅为常规查验，未产生任何额外费用。"),

    ("正常农业·合作交流", 0,
     "关于农药登记事宜，申报材料需提供毒理学报告与两季残留数据，"
     "我方将在本地试验结束后整理上报。"),

    ("正常农业·单证结算", 0,
     "贵司种子出口审批申请已在检疫审查流程中，预计十个工作日内出结果，"
     "批复一经下达我们立即转发给您。"),

    ("正常农业·合作交流", 0,
     "附上我司合作社与贵方的供货协议草稿，涵盖数量、质量标准与交货期，"
     "欢迎在下一轮磋商前提出修改意见。"),

    ("正常农业·合作交流", 0,
     "土壤检测委托已受理。报价覆盖大量元素测定与二十四个样本的重金属筛查，"
     "报告将于收样后两周内出具。"),

    ("正常农业·询盘报价", 0,
     "请对联合收割机 4LZ-6.0 型配件报价，主要为割台与脱粒滚筒，"
     "所需机型编号见附表，请据此核价。"),


    ("正常农业·单证结算", 0,
     "应贵方要求确认本合同的银行信息：户名福建绿野农产品出口有限公司，"
     "开户行中国银行福州分行，该账户为本季历次出货所用，信息未做变更，"
     "请照此开票。"),
]



def build_rows():
    
    rows = []
    for block, lang, scene_prefix in (
        (EN_PHISH, "en", "英文"),
        (EN_NORM, "en", "英文"),
        (ZH_PHISH, "zh", "中文"),
        (ZH_NORM, "zh", "中文"),
    ):
        for idx, (scene, is_phish, text) in enumerate(block, start=1):

            to_holdout = idx >= 20
            rows.append({
                "lang": lang,
                "scene": f"{scene_prefix}·{scene}",
                "is_phish": is_phish,
                "text": text.strip(),
                "holdout": to_holdout,
            })
    return rows


def main():
    new_rows = build_rows()
    main_rows = [r for r in new_rows if not r["holdout"]]
    holdout_rows = [r for r in new_rows if r["holdout"]]


    old = list(csv.DictReader(open("samples.csv", encoding="utf-8-sig", newline="")))
    fieldnames = ["id", "lang", "scene", "is_phish", "text", "source", "note"]




    ids = [int(r["id"][1:]) for r in old
           if r["id"].startswith("S") and r["id"][1:].isdigit()]
    max_id = max(ids) if ids else 0
    if max_id > LEGACY_MAX_ID:
        raise SystemExit(
            f"samples.csv 里已经含有新样本（最大编号 S{max_id:03d}），"
            f"重复运行会让样本翻倍。\n"
            f"如需重跑，请先还原原始样本：  git checkout -- samples.csv"
        )


    kept, archived = [], []
    for r in old:
        if not r.get("text") or not r["text"].strip():
            continue
        sid = r["id"]
        is_old_agri = sid.startswith("S") and sid[1:].isdigit() and int(sid[1:]) >= 105
        if sid in CONTROL_KEEP or is_old_agri:
            kept.append(r)
        else:
            archived.append(r)


    os.makedirs("legacy", exist_ok=True)
    with open("legacy/legacy_generic_samples.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in archived:
            w.writerow({k: r.get(k, "") for k in fieldnames})


    start = LEGACY_MAX_ID + 1

    out_rows = []
    for r in kept:
        out_rows.append({k: r.get(k, "") for k in fieldnames})
    for i, r in enumerate(main_rows):
        out_rows.append({
            "id": f"S{start + i:03d}",
            "lang": r["lang"],
            "scene": r["scene"],
            "is_phish": str(r["is_phish"]),
            "text": r["text"],
            "source": SRC,
            "note": "",
        })

    with open("samples.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)


    os.makedirs("holdout", exist_ok=True)
    with open("holdout/holdout_agri_v2.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(fieldnames)
        for i, r in enumerate(holdout_rows, start=1):
            w.writerow([f"H2{i:02d}", r["lang"], "留出v2·" + r["scene"],
                        str(r["is_phish"]), r["text"], SRC, ""])
    print(f"已写入留出集 v2：{len(holdout_rows)} 条 -> holdout/holdout_agri_v2.csv")


    total = len(out_rows)
    phish = sum(1 for r in out_rows if r["is_phish"] == "1")
    en = sum(1 for r in out_rows if r["lang"] == "en")
    print()
    print("=" * 64)
    print("  主测试集重建完成")
    print("=" * 64)
    print(f"  总计 {total} 条：钓鱼 {phish} / 正常 {total - phish}"
          f"　英文 {en} / 中文 {total - en}")
    print(f"  其中农业国际合作 {sum(1 for r in out_rows if '农业' in r['scene'] or '农' in r['scene'])} 条")
    print(f"  新增 {len(main_rows)} 条（编号 S{start:03d}~S{start + len(main_rows) - 1:03d}）")
    print(f"  归档通用样本 {len(archived)} 条 -> legacy/legacy_generic_samples.csv")
    print()


if __name__ == "__main__":
    main()
