# -*- coding: utf-8 -*-
"""
rules.py —— 语盾(LinguaShield) 规则库
==========================================
这是整个项目的**核心资产**，也是你作为英语专业学生的独占价值所在。

设计来源说明（合规声明）：
本文件的**设计思想**参考了开源项目 SecuriSMS（MIT 协议）的"规则分层 + 语言路由"
思路，以及 phishing-detector-advanced 的"多层加权"思路。
但所有词条为你自行收集整理、代码实现为你自行编写，**未复制任何开源仓库的代码**。

规则分层思想（借鉴自 SecuriSMS）：
  R 层  → 基础规则：单条话术命中（如"verify your account"）
  C 层  → 组合规则：多类话术同时出现才高度可疑（如"冒充身份 + 索要密码"）
  URL 层 → URL 信誉规则：短链、可疑 TLD、仿冒域名、IP 直连

重要设计：GROUP_BASE 分组基础分
---------------------------------
不同话术组的"可疑程度"不同，不能一律给同样分数：
  · "辅导员""教务处"这类中性词，出现在校园通知里很正常 → 只给 3 分（几乎不报警）
  · "验证码""activate fee""manuscript processing charge" → 强信号，给 12~15 分
中性词必须配合其他信号（组合规则）才会拉高风险，这样才能**降低误报**。
"""

# ============================================================
# 一、英文话术库（你的英语优势区）
# ============================================================

EN_PHRASES = {
    "凭证索取（Credential Harvesting）": [
        "verify your account", "verify your identity",
        "confirm your password", "update your payment",
        "re-enter your credentials", "login to continue",
        "reset your password",           # 新增：诱导重置密码
        "enter your login",              # 新增
    ],
    "账户异常恐吓（Account Threat）": [
        # ↑ 注意：这里补全了真实邮件常见的变体。
        # 初版只写了 "account suspended"，但真实邮件常写
        # "your account IS suspended" / "has been suspended"，中间多一个词就匹配失败了。
        "account suspended", "account is suspended",
        "account has been suspended", "account has been locked",
        "account will be closed", "account will be permanently closed",
        "unusual activity", "unusual sign-in",      # 新增
        "we noticed suspicious",                    # 新增
    ],
    "紧急施压（Urgency）": [
        "immediately", "within 24 hours", "within 12 hours",
        "urgent", "urgent action required",   # 新增单独的 "urgent"
        "act now", "expires today", "final notice",
        "limited time",                       # 新增
    ],
    "冒充机构（Impersonation）": [
        "security team", "it department", "it support",      # 新增 it support
        "on behalf of", "official notification",
        "dear customer", "dear user", "dear account holder", 
        "new device"# 新增
    ],
    "金钱诱导（Financial Lure）": [
        "processing fee", "fee required", "charge required",
        "advance payment", "prize", "refund",
        "wire transfer", "bank transfer",      # 新增 bank transfer
        "gift card", "invoice attached",       # 新增
    ],
    "费用索取（Fee Demand）": [
        # ★ 新增这一组：配合学术诈骗做组合判断，专治掠夺性期刊/会议
        "pay the fee", "payment of",
        "usd", "$", "credit card",
        "non-refundable",                      # 典型掠夺性会议话术
    ],
    "学术·会议诈骗（Academic Scam）": [
        # ===== 你的差异化卖点：学术场景诈骗 =====
        # 英语专业学生/教师常收到，国产安全工具几乎不覆盖。
        # ⚠️ 这一组只放"强信号"：一出现本身就说明有问题。
        "manuscript processing charge", "article processing charge",  # 新增 APC
        "conference registration fee", "registration fee",
        "indexing fee",
        "impact factor guaranteed",
        "keynote speaker invitation",
    ],
    "学术场景（中性词）": [
        # ★2026-09-29 修正：下面这些词，真实的学术邮件里一样会出现。
        #   初版把它们和"版面费"放在同一组（15分），导致正常的会议通知
        #   只要写了 "review committee" 就被判 15 分 → 误报。
        #   现在单独成组只给 3 分，必须"配合收费话术"才会拉高风险。
        "call for papers", "submit your manuscript",
        "review committee", "submit your paper",
        "academic committee", "editorial board",
    ],
}

# ============================================================
# 二、中文话术库（校园场景，贴近大学生受害案例）
# ============================================================

ZH_PHRASES = {
    "冒充身份（Impersonation）": [
        # ⚠️ 这一组词是"中性词"：校园正常通知里也会出现（辅导员发通知很常见）
        #    所以基础分只给 3 分，必须配合"金钱/套取/掩饰"才判定高危。
        "辅导员", "教务处", "班主任", "学长", "后勤处","学姐",
    ],
    "金钱相关（Financial）": [
        # ★2026-09-29 修正："奖学金"从这里移走了。
        #   真实校园通知里"奖学金公示"极其常见，给它 12 分会导致
        #   "教务处通知奖学金已公示"这种正常通知被判 52 分 → 严重误报。
        #   奖学金本身不是危险信号，危险的是"申领奖学金要先交激活费"。
        "助学金", "激活费", "保证金",
        "银行卡", "验证码", "转账", "校园贷",
        "手续费", "押金", "缴纳", "汇款",  "跑分", "跑带", "校园跑分",  # 新增 缴纳/汇款
    ],
    "校园事务（中性词）": [
        # ★2026-09-29 新增：校园正常事务词，只给 2 分。
        #   它们单独出现完全正常，只有配合"收钱/套信息/要保密"才可疑。
        "奖学金", "选课", "学分", "学籍", "公示", "评优",
    ],
    "学术·版面费诈骗（Academic Scam CN）": [
        # ★2026-09-29 新增：中文库原本完全没有学术诈骗词条，
        #   导致"缴纳版面费、快速发表、保密处理"这种典型掠夺性期刊
        #   催收邮件只判 20 分（漏报）。而这恰恰是本项目主打场景之一。
        "版面费", "快速发表", "录用通知", "审稿费",
        "代发", "包发表", "包录用", "核心期刊",
    ],
     "校园代务诈骗（Campus Proxy Scam）": [
        # ★2026-10-02 新增：校园代务/虚假活动类诈骗暗语
        #   综测加分/代课/cos/交换人生/英语口语班/口语角 都是"听起来像校内事务"
        #   但实际本校并不存在(或需付费)的话术，给中等分(10)，
        #   须配合"交钱"才判高危，避免误伤正常校内通知。
        "综测加分", "代课", "cos", "交换人生", "有偿代课",
        "英语口语班", "英语口语角",
    ],
    "紧急施压（Urgency）": [
        "抓紧时间", "最后一天", "过期作废", "立即办理", "名额有限",
        "速办",               # 新增
    ],
    "信息套取（Info Harvesting）": [
        "身份证号", "学号", "个人信息", "银行卡号", "填写链接",
        "登录密码",           # 新增
    ],
    "话术掩饰（Secrecy）": [
        # 让你不要跟别人商量 —— 这是诈骗的强信号
        "保密", "不要声张", "私下联系",
        "不要告诉",           # 新增
    ],

    # ---- ★2026-10-02 新增：保卫处预警诈骗类型（福建农林大学武装部/保卫处 开学第一课）----
    "刷单返利（Brush Order Scam）": [
        # 保卫处点名校园最高发：刷单返利。这些词正常语境绝不会出现 → 强信号。
        "刷单", "点赞任务", "任务冻结", "连单", "垫付", "返利", "日结高薪",
    ],
    "游戏交易诈骗（Game Trade Scam）": [
        "游戏交易", "账号冻结", "充值解冻", "装备交易", "游戏账号",
    ],
    "冒充客服（Fake CS）": [
        # 含 FAU 真实案例：冒充"校妆网"客服进宿舍卖假化妆品
        "理赔退款", "包裹丢失", "屏幕共享", "校妆网", "快递客服",
        "注销学生账户", "安全账户",
    ],
    "考证升学诈骗（Cert Scam）": [
        "保过", "内部名额", "代写论文", "改分数", "花钱改分",
    ],
}

# ============================================================
# 三、分组基础分（★核心设计：解决误报问题）
# ============================================================
# 借鉴 phishing-detector-advanced 的"分层加权"思想：
# 不同信号的可信度不同，给不同权重，而不是一律 10 分。

GROUP_BASE = {
    # ---- 英文 ----
    "凭证索取（Credential Harvesting）":   12,   # 强信号
    "账户异常恐吓（Account Threat）":      12,   # 强信号
    "紧急施压（Urgency）":                  8,   # 中等（正常邮件也可能催)
    "冒充机构（Impersonation）":            5,   # 偏中性（群发特征）
    "金钱诱导（Financial Lure）":          12,   # 强信号
    "费用索取（Fee Demand）":              10,   # 强
    "学术·会议诈骗（Academic Scam）":      15,   # ★最高：你的差异化场景要能报出来
    "学术场景（中性词）":                   3,   # ★2026-09-29 新增：避免正常学术邮件误报
    # ---- 中文 ----
    "冒充身份（Impersonation）":            3,   # ★中性词，只给 3 分避免误报
    "金钱相关（Financial）":               12,
    "紧急施压（Urgency）":                  8,
    "信息套取（Info Harvesting）":         12,
    "话术掩饰（Secrecy）":                 12,
    "校园事务（中性词）":                   2,   # ★2026-09-29 新增
    "学术·版面费诈骗（Academic Scam CN）": 15,   # ★2026-09-29 新增：补上中文学术诈骗漏报
    "校园代务诈骗（Campus Proxy Scam）":   10,   # 中等：暗语，配合交钱才高危
    # ---- 保卫处高危类型：正常语境绝不会出现，单命中即判可疑(>=40) ----
    "刷单返利（Brush Order Scam）":       40,   # 强信号：刷单返利（保卫处预警）
    "游戏交易诈骗（Game Trade Scam）":     40,   # 强信号：游戏账号解冻诈骗
    "冒充客服（Fake CS）":                 40,   # 强信号：理赔退款/校妆网等
    "考证升学诈骗（Cert Scam）":           40,   # 强信号：保过/代写论文
}

# ============================================================
# 四、URL 信誉规则（借鉴 SecuriSMS 的 URL 检查思路）
# ============================================================

SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "is.gd", "buff.ly", "shorte.st", "cutt.ly",
]

SUSPICIOUS_TLDS = [
    ".tk", ".ml", ".ga", ".cf", ".gq",
    ".xyz", ".top", ".loan", ".work", ".click", ".link",
]

BRAND_KEYWORDS = [
    "paypal", "paypa1", "microsoft", "micr0soft",
    "apple", "app1e", "google", "g00gle",
    "amazon", "amaz0n", "alipay", "al1pay",
    "wechat", "w3chat",
]

# 白名单：可信域名直接放行，避免误伤（借鉴 SecuriSMS 的 allowlist）
TRUSTED_DOMAINS = [
    "fafu.edu.cn", "edu.cn", "gov.cn", "cnki.net",
]

# ============================================================
# 五、组合规则（C 层）—— 借鉴 SecuriSMS 的"组合规则"思想
# ============================================================
# 单条话术可能是巧合，但组合出现几乎必然是钓鱼。
# 格式：(需要同时命中的话术组列表, 加分值, 判定说明)

COMBO_RULES = [
    # ---- 英文：经典账号盗取 ----
    (["冒充机构（Impersonation）", "凭证索取（Credential Harvesting）"], 25,
     "冒充机构并索要凭证，高度疑似钓鱼"),
    (["账户异常恐吓（Account Threat）", "凭证索取（Credential Harvesting）"], 25,
     "账户恐吓配合索要凭证，典型账号盗取"),
    (["账户异常恐吓（Account Threat）", "紧急施压（Urgency）"], 20,
     "账户恐吓配合紧急施压，制造恐慌诱导点击"),
    (["凭证索取（Credential Harvesting）", "紧急施压（Urgency）"], 22,
     "索要凭证配合紧急时限，典型钓鱼话术"),

    # ★2026-10-01 模块 D 实战：新增两条英文组合，专治"金钱诱导+紧急施压"漏报
    #   为什么加：原规则库只有 [冒充机构,凭证索取]、[账户恐吓,凭证索取] 等，
    #   但"财务/中奖类诈骗"常见形态是 金钱话术 + 紧急时限 同现、却没冒充机构，
    #   于是单条加分不够(20~30分)、判不到 40 分"可疑"线 → 漏报了 S008/S015/S016/S019/S020/S021。
    #   为什么安全：组合要求"两组同时命中"。正常英文邮件既不会写 wire transfer/gift card，
    #   也不会写 urgent/within 24 hours，所以正常样本几乎不可能同时命中两组 → 不会新增误报。
    (["金钱诱导（Financial Lure）", "紧急施压（Urgency）"], 22,
     "金钱诱导配合紧急时限，典型财务/中奖类钓鱼"),
    (["费用索取（Fee Demand）", "紧急施压（Urgency）"], 24,
     "费用索取配合紧急催促，疑似掠夺性收费/中奖诈骗(补抓 S018)"),

    # ---- ★学术诈骗专项（你的差异化卖点）----
    (["学术·会议诈骗（Academic Scam）", "费用索取（Fee Demand）"], 30,
     "学术/会议话术配合费用索取，疑似掠夺性期刊或虚假会议诈骗"),
    (["学术·会议诈骗（Academic Scam）", "金钱诱导（Financial Lure）"], 28,
     "学术/会议话术涉及金钱交易，疑似学术诈骗"),
    (["学术·会议诈骗（Academic Scam）", "紧急施压（Urgency）"], 22,
     "学术场景配合紧急催促，疑似虚假征稿/会议通知"),
    # ★2026-09-29 新增：中性学术词本身不报警，但一旦同时出现收费话术，
    #   说明"披着学术外衣要钱"，这才是掠夺性期刊的典型形态。
    (["学术场景（中性词）", "费用索取（Fee Demand）"], 20,
     "学术征稿话术配合费用索取，疑似掠夺性期刊/虚假会议"),
    (["学术场景（中性词）", "金钱诱导（Financial Lure）"], 18,
     "学术征稿话术涉及金钱交易，建议核实主办方资质"),

    # ---- 中文：校园诈骗典型组合 ----
    (["冒充身份（Impersonation）", "金钱相关（Financial）"], 25,
     "冒充校内身份并涉及金钱，高度疑似诈骗"),
    # ★2026-09-29 新增：真实的校内通知不会给你"最后一天"的死线。
    #   只有"冒充身份 + 时间压力"同现，几乎不可能是正常通知。
    (["冒充身份（Impersonation）", "紧急施压（Urgency）"], 20,
     "冒充校内身份并施加时间压力，疑似诈骗"),
    (["冒充身份（Impersonation）", "信息套取（Info Harvesting）"], 22,
     "冒充校内身份并套取个人信息，疑似信息窃取"),
    (["金钱相关（Financial）", "话术掩饰（Secrecy）"], 25,
     "涉及金钱且要求保密，典型诈骗话术"),
    (["紧急施压（Urgency）", "信息套取（Info Harvesting）"], 20,
     "紧急催促配合套取个人信息，疑似信息窃取"),
    (["信息套取（Info Harvesting）", "金钱相关（Financial）"], 25,
     "套取个人信息并涉及金钱，疑似盗刷风险"),

    # ---- ★2026-09-29 新增：中文学术诈骗（补上原规则库的漏报）----
    (["学术·版面费诈骗（Academic Scam CN）", "话术掩饰（Secrecy）"], 25,
     "论文/期刊话术要求保密处理，疑似掠夺性期刊或代发诈骗"),
    (["学术·版面费诈骗（Academic Scam CN）", "金钱相关（Financial）"], 25,
     "论文/期刊话术配合缴费要求，疑似版面费诈骗"),
    (["学术·版面费诈骗（Academic Scam CN）", "紧急施压（Urgency）"], 20,
     "论文/期刊话术配合限时催促，疑似虚假录用通知"),
    # ---- ★2026-10-02 新增：校园代务 + 保卫处预警组合规则 ----
    (["校园代务诈骗（Campus Proxy Scam）", "金钱相关（Financial）"], 25,
     "校园代务暗语(综测加分/代课/cos)配合交钱，疑似校园诈骗"),
    (["刷单返利（Brush Order Scam）", "金钱相关（Financial）"], 25,
     "刷单返利配合金钱交易，高危诈骗"),
    (["刷单返利（Brush Order Scam）", "紧急施压（Urgency）"], 22,
     "刷单话术配合限时催促，典型刷单诈骗"),
    (["游戏交易诈骗（Game Trade Scam）", "金钱相关（Financial）"], 25,
     "游戏交易配合金钱，疑似账号解冻/装备交易诈骗"),
    (["冒充客服（Fake CS）", "信息套取（Info Harvesting）"], 25,
     "冒充客服配合索要信息(验证码/屏幕共享)，高危"),
    (["冒充客服（Fake CS）", "金钱相关（Financial）"], 25,
     "冒充客服(校妆网/快递)配合交钱，疑似诈骗"),
    (["考证升学诈骗（Cert Scam）", "金钱相关（Financial）"], 25,
     "考证升学(保过/代写)配合交钱，疑似诈骗"),
]

# ============================================================
# 六、评分权重（多层加权，借鉴 phishing-detector-advanced）
# ============================================================
WEIGHTS = {
    "phrase": 1.0,   # 话术命中
    "combo":  1.5,   # 组合命中：比单条更可信
    "url":    1.2,   # URL 异常：客观证据，可信度最高
}
