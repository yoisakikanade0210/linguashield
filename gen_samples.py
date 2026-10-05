# -*- coding: utf-8 -*-
"""
gen_samples.py —— 生成 100 条测试集 samples.csv
=================================================
用途：把语盾的测试集从 3 条示例扩充到 100 条真实样本。
      覆盖「账号盗取 / 学术诈骗 / 校园冒充 / 版面费诈骗 / 客服理赔」等钓鱼场景，
      以及「奖学金公示 / 正常学术通知 / 个人邮件」等正常场景。

设计要点（配合模块 A 学习）：
  · 钓鱼约 40 条、正常约 60 条 —— 故意制造「类别不平衡」，
    这样跑出来的指标才能演示"准确率会骗人、必须看 FPR"。
  · 正常样本里刻意放"奖学金公示""正常 CFP"等易误报文本，用来压低误报率。

运行：python gen_samples.py  → 生成同目录 samples.csv（UTF-8 BOM，Excel 可直接打开）
"""
import csv

# 每条样本：(场景 scene, 是否钓鱼 is_phish, 文本 text, 来源 source)
# lang 由引擎自动判定，这里不填，留空；但 CSV 里保留 lang 列方便人工核对。

rows = []
SRC = "自建测试集(2026-10-01)"

# ============ 钓鱼样本 is_phish=1（约 40 条）============

# ---- 英文·账号盗取（10）----
rows += [
    ("en", "英文·账号盗取", 1, "Dear Customer, we noticed suspicious activity on your PayPal account. Your account has been suspended. Please verify your account within 24 hours: https://bit.ly/3xK9pQz", SRC),
    ("en", "英文·账号盗取", 1, "Microsoft account security: unusual sign-in detected. Your account will be locked. Re-enter your credentials to keep access: http://micr0soft-secure.tk/login", SRC),
    ("en", "英文·账号盗取", 1, "Your Apple ID has been disabled. Account is suspended due to unusual activity. Confirm your password immediately to restore it.", SRC),
    ("en", "英文·账号盗取", 1, "IT department notice: we detected unusual activity on your bank login. Please reset your password now to secure the account.", SRC),
    ("en", "英文·账号盗取", 1, "Amazon: your order is on hold. Verify your identity and update your payment within 24 hours or the order will be cancelled.", SRC),
    ("en", "英文·账号盗取", 1, "Google Security: a new device signed in. If this was not you, login to continue and confirm your password to protect your account.", SRC),
    ("en", "英文·账号盗取", 1, "Netflix: your account has been suspended for unusual activity. Enter your login to reactivate your subscription today.", SRC),
    ("en", "英文·账号盗取", 1, "Urgent: your bank detected fraud. Wire transfer to the secured account within 12 hours or your card will be frozen.", SRC),
    ("en", "英文·账号盗取", 1, "IT support: your password expires today. Reset your password via the link to avoid account closure: http://paypa1-verify.gq/", SRC),
    ("en", "英文·账号盗取", 1, "Microsoft 365: final notice. Your account will be permanently closed. Re-enter your credentials within 24 hours to keep your mailbox.", SRC),
]

# ---- 英文·学术诈骗（8）----
rows += [
    ("en", "英文·学术诈骗", 1, "Congratulations! Your manuscript is accepted. Please pay the manuscript processing charge of 350 USD to proceed with publication.", SRC),
    ("en", "英文·学术诈骗", 1, "You are invited to submit to ICMAST 2027. Conference registration fee applies. Indexing fee required. Payment of 400 USD via credit card.", SRC),
    ("en", "英文·学术诈骗", 1, "Special issue with impact factor guaranteed. Keynote speaker invitation. Non-refundable article processing charge of 500 USD.", SRC),
    ("en", "英文·学术诈骗", 1, "Your paper needs an article processing charge of $280. Please make the payment of the fee via the link before the deadline.", SRC),
    ("en", "英文·学术诈骗", 1, "You won a prize refund of $120. Gift card required to claim. Act now, expires today.", SRC),
    ("en", "英文·学术诈骗", 1, "Invoice attached. Urgent: pay the fee required to publish your paper. Wire transfer accepted.", SRC),
    ("en", "英文·学术诈骗", 1, "Call for papers — but registration fee of 250 USD is non-refundable and must be paid to confirm your submission.", SRC),
    ("en", "英文·学术诈骗", 1, "Limited time: pay the fee to index your paper. USD payment via credit card. Final notice.", SRC),
]

# ---- 英文·财务/中奖诈骗（4）----
rows += [
    ("en", "英文·财务诈骗", 1, "You received a gift card reward. Urgent action required: claim your prize within 24 hours using the link.", SRC),
    ("en", "英文·财务诈骗", 1, "Bank transfer needed. Limited time offer. Act now or the refund expires today.", SRC),
    ("en", "英文·财务诈骗", 1, "Wire transfer of your inheritance. Final notice: confirm your bank transfer details immediately.", SRC),
    ("en", "英文·财务诈骗", 1, "Credit card refund pending. Expires today. Enter your login to receive the refund now.", SRC),
]

# ---- 中文·冒充辅导员/校内身份（10）----
rows += [
    ("zh", "中文·冒充辅导员", 1, "同学你好，我是辅导员李老师。你的助学金申请已通过，请立即点击链接填写身份证号和银行卡号，验证码稍后发送。名额有限，抓紧时间办理，不要告诉他人。", SRC),
    ("zh", "中文·冒充辅导员", 1, "教务处通知：请于今日转账学费至指定账户，立即办理，逾期将影响选课。账户信息见链接。", SRC),
    ("zh", "中文·冒充辅导员", 1, "同学，我是班主任。请提供学号和身份证号用于学籍核对，点击填写链接，此事需保密，不要声张。", SRC),
    ("zh", "中文·冒充辅导员", 1, "学长提醒：校园贷额度已批，需先交押金激活，转账后速办，名额有限。", SRC),
    ("zh", "中文·冒充辅导员", 1, "后勤处通知：请缴纳宿舍水电费，汇款至下方账户，立即办理。", SRC),
    ("zh", "中文·冒充辅导员", 1, "同学你好，奖学金已到账，需先交激活费才能发放，请提供银行卡号和验证码，不要告诉他人。", SRC),
    ("zh", "中文·冒充辅导员", 1, "教务处紧急通知：你的登录密码已过期，请抓紧时间重置，点击链接填写。", SRC),
    ("zh", "中文·冒充辅导员", 1, "班主任通知：请提交个人信息并转账办理助学手续，速办，过期作废。", SRC),
    ("zh", "中文·冒充辅导员", 1, "同学，助学金名额将满，需交保证金锁定名额，抓紧时间，私下联系我办理。", SRC),
    ("zh", "中文·冒充辅导员", 1, "学长说：领奖学金要先填验证码和银行卡，私下联系，不要告诉辅导员。", SRC),
]

# ---- 中文·学术版面费诈骗（8）----
rows += [
    ("zh", "中文·版面费诈骗", 1, "您的论文录用通知已发，请缴纳版面费并汇款，快速发表，此事需保密处理。", SRC),
    ("zh", "中文·版面费诈骗", 1, "本刊可代发、包录用、包发表核心期刊，需交审稿费，转账办理，速办。", SRC),
    ("zh", "中文·版面费诈骗", 1, "论文版面费请汇款至指定账户，过期作废，立即办理。", SRC),
    ("zh", "中文·版面费诈骗", 1, "期刊征稿，包发表需缴纳费用，立即办理，名额有限。", SRC),
    ("zh", "中文·版面费诈骗", 1, "录用通知：请于今日交审稿费，速办，勿外传。", SRC),
    ("zh", "中文·版面费诈骗", 1, "核心期刊代发，转账并保密，速办，错过不再有。", SRC),
    ("zh", "中文·版面费诈骗", 1, "版面费快速发表通道开放，不要声张，立即缴纳。", SRC),
    ("zh", "中文·版面费诈骗", 1, "征稿启事：版面费缴纳后包录用，名额有限，抓紧时间。", SRC),
]

# ============ 正常样本 is_phish=0（约 60 条）============

# ---- 英文·正常学术/通知（30）----
rows += [
    ("en", "英文·正常学术", 0, "The review committee has finished evaluating submissions. Authors will be notified by email next week. Thank you for your patience.", SRC),
    ("en", "英文·正常学术", 0, "Call for papers: the 2027 Linguistics Conference invites submissions on corpus methods. Please submit your manuscript through the portal.", SRC),
    ("en", "英文·正常学术", 0, "Dear colleague, the editorial board meeting is scheduled for Friday. Agenda and minutes are attached for your reference.", SRC),
    ("en", "英文·正常学术", 0, "Reminder: your library books are due tomorrow. Please return or renew them via the library website. No action needed otherwise.", SRC),
    ("en", "英文·正常学术", 0, "We are pleased to invite you to the department seminar on Friday at 3pm. Light refreshments will be served.", SRC),
    ("en", "英文·正常学术", 0, "Your submission to the journal has been received. The peer review process typically takes 8 weeks. We will contact you with updates.", SRC),
    ("en", "英文·正常学术", 0, "The conference registration is now open. Early bird rate ends in three weeks. Visit the official site to register.", SRC),
    ("en", "英文·正常学术", 0, "Dear user, your newsletter subscription is confirmed. You may unsubscribe at any time using the link below.", SRC),
    ("en", "英文·正常学术", 0, "IT department will perform scheduled maintenance on Sunday 2am-4am. Services may be briefly unavailable. No password change required.", SRC),
    ("en", "英文·正常学术", 0, "Congratulations on your acceptance to the program. Please complete the enrollment form and upload your documents by the deadline.", SRC),
    ("en", "英文·正常学术", 0, "The scholarship committee has published the list of recipients on the university portal. Congratulations to all awardees.", SRC),
    ("en", "英文·正常学术", 0, "Your course registration is confirmed. The syllabus and reading list are available on the course page.", SRC),
    ("en", "英文·正常学术", 0, "Reminder: tuition payment for the semester is due at the end of the month. Pay through the student finance portal.", SRC),
    ("en", "英文·正常学术", 0, "Dear student, the writing center offers free tutoring this term. Book a session online at your convenience.", SRC),
    ("en", "英文·正常学术", 0, "The annual research symposium abstract book is now available. Thank you to all who submitted abstracts.", SRC),
    ("en", "英文·正常学术", 0, "We have received your application. Our team will review it and respond within 10 business days. No further action is needed now.", SRC),
    ("en", "英文·正常学术", 0, "The library will be closed for the holiday. Regular hours resume the following Monday. Enjoy the break.", SRC),
    ("en", "英文·正常学术", 0, "Dear colleague, please find attached the meeting notes from yesterday's discussion. Let me know if you have questions.", SRC),
    ("en", "英文·正常学术", 0, "Your journal access has been renewed for another year. You may continue downloading articles as usual.", SRC),
    ("en", "英文·正常学术", 0, "The campus career fair is next Tuesday in the main hall. Bring your resume and talk to recruiters.", SRC),
    ("en", "英文·正常学术", 0, "Reminder: the final exam schedule is posted. Please check your student portal for date and room assignments.", SRC),
    ("en", "英文·正常学术", 0, "Thank you for volunteering at the outreach event. A certificate of participation will be emailed to you shortly.", SRC),
    ("en", "英文·正常学术", 0, "The writing workshop series begins next week. Sessions are free for enrolled students. Register on the linguistics department site.", SRC),
    ("en", "英文·正常学术", 0, "Your requested interlibrary loan has arrived. Pick it up at the circulation desk with your student ID.", SRC),
    ("en", "英文·正常学术", 0, "Dear applicant, we have received your fee waiver request and are reviewing it. You will hear from us soon.", SRC),
    ("en", "英文·正常学术", 0, "The department picnic is this Saturday at the lakeside park. Family and friends welcome. Bring your own picnic blanket.", SRC),
    ("en", "英文·正常学术", 0, "Your transcript request has been processed. The official PDF will be sent to the address you provided.", SRC),
    ("en", "英文·正常学术", 0, "Reminder: the thesis submission deadline is the last day of the month. Submit through the graduate school portal.", SRC),
    ("en", "英文·正常学术", 0, "We enjoyed your guest lecture and would like to invite you to speak again next semester. Please let us know your availability.", SRC),
    ("en", "英文·正常学术", 0, "The student health center extended its hours during finals week. Walk-ins are welcome without an appointment.", SRC),
]

# ---- 中文·正常通知（30）----
rows += [
    ("zh", "中文·正常通知", 0, "各位同学：本学期奖学金评定结果已在教务处官网公示，请自行登录教务系统查看，公示期五个工作日。", SRC),
    ("zh", "中文·正常通知", 0, "选课通知：下学期选课通道将于周一开放，请同学们提前在教务系统查看培养方案与学分要求。", SRC),
    ("zh", "中文·正常通知", 0, "关于学籍核对的通知：请于本周内登录系统确认本人学籍信息，如有误及时联系班主任更正。", SRC),
    ("zh", "中文·正常通知", 0, "教务处公告：全国大学英语四六级考试报名开始，请符合条件的同学及时报名并缴费。", SRC),
    ("zh", "中文·正常通知", 0, "评优结果公示：本学年三好学生及优秀学生干部名单已张贴于学院公告栏，欢迎监督。", SRC),
    ("zh", "中文·正常通知", 0, "辅导员通知：下周班会时间为周三下午，地点在教室 301，请准时参加，无需带材料。", SRC),
    ("zh", "中文·正常通知", 0, "图书馆通知：假期开放时间调整为上午九点至晚上九点，还书请到一楼自助机办理。", SRC),
    ("zh", "中文·正常通知", 0, "校医院提醒：流感疫苗接种本周进行，请同学们携带学生证到体育馆有序接种。", SRC),
    ("zh", "中文·正常通知", 0, "后勤处通知：宿舍热水系统将于周日检修，届时暂停供应，请同学们提前做好准备。", SRC),
    ("zh", "中文·正常通知", 0, "关于奖学金发放：财务处将于本月统一打入学子卡，请注意查收，无需任何激活操作。", SRC),
    ("zh", "中文·正常通知", 0, "学长学姐经验分享会本周五晚在报告厅举行，欢迎大一同学参加，现场可提问交流。", SRC),
    ("zh", "中文·正常通知", 0, "班主任通知：综合素质测评材料请于周五前在系统提交，逾期系统将自动关闭。", SRC),
    ("zh", "中文·正常通知", 0, "教务处：期中教学检查启动，同学们可通过教务系统对课程进行评价，评价匿名。", SRC),
    ("zh", "中文·正常通知", 0, "关于助学金：学校资助名单已公示，请相关同学登录系统确认银行卡号无误以便发放。", SRC),
    ("zh", "中文·正常通知", 0, "校园活动：秋季运动会报名开始，有意参加的同学到体育部填写报名表，截止本周五。", SRC),
    ("zh", "中文·正常通知", 0, "心理咨询中心开放预约：同学们可通过官网预约面谈，服务免费且严格保密。", SRC),
    ("zh", "中文·正常通知", 0, "学院通知：学术讲座《语料库语言学入门》定于周四晚，欢迎各年级同学旁听。", SRC),
    ("zh", "中文·正常通知", 0, "关于学费：请同学们通过学校财务平台按时缴纳，缴费成功后可自行下载电子票据。", SRC),
    ("zh", "中文·正常通知", 0, "就业指导中心：校园招聘会下周举行，请同学们准备好简历，着正装参加。", SRC),
    ("zh", "中文·正常通知", 0, "教务处公告：期末考试安排已发布，请同学登录系统查询具体时间与考场。", SRC),
    ("zh", "中文·正常通知", 0, "志愿者招募：图书馆助学岗招新，每周值班四小时，可加综合素质学分，详情见通知。", SRC),
    ("zh", "中文·正常通知", 0, "关于宿舍调整：需调寝的同学请在系统提交申请，由班主任审核后统一安排。", SRC),
    ("zh", "中文·正常通知", 0, "学生会通知：迎新晚会节目征集开始，有特长的同学可到文艺部报名。", SRC),
    ("zh", "中文·正常通知", 0, "教务处：英语角每周三晚在外国语学院大厅举行，外教现场指导，欢迎参加。", SRC),
    ("zh", "中文·正常通知", 0, "关于医保：大学生医保续保缴费通道已开，请同学们在截止日前完成缴费。", SRC),
    ("zh", "中文·正常通知", 0, "实习基地宣讲：某教育集团下周来校宣讲，地点阶梯教室，感兴趣的同学可自行前往。", SRC),
    ("zh", "中文·正常通知", 0, "学院公示：国家奖学金拟推荐人选已在官网发布，公示期内接受异议反馈。", SRC),
    ("zh", "中文·正常通知", 0, "后勤处：食堂一楼翻新完毕，正常营业，欢迎同学们就餐并反馈意见。", SRC),
    ("zh", "中文·正常通知", 0, "班主任：班级春游报名接龙开始，费用AA，自愿参加，请在本群接龙。", SRC),
    ("zh", "中文·正常通知", 0, "图书馆：到期图书可线上续借一次，无需到馆，续借成功会短信通知。", SRC),
]

# ============ 写入 CSV ============
assert len(rows) == 100, f"样本数应为 100，实际 {len(rows)}"

header = ["id", "lang", "scene", "is_phish", "text", "source", "note"]
out_path = "samples.csv"
with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    for i, (lang, scene, is_phish, text, source) in enumerate(rows, start=1):
        w.writerow([f"S{i:03d}", lang, scene, is_phish, text, source, ""])

# 统计打印
phish = sum(1 for r in rows if r[2] == 1)
normal = 100 - phish
en = sum(1 for r in rows if r[0] == "en")
zh = 100 - en
print(f"已写入 {out_path}：共 100 条")
print(f"  钓鱼 {phish} 条 / 正常 {normal} 条")
print(f"  英文 {en} 条 / 中文 {zh} 条")
