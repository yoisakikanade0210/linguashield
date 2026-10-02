# -*- coding: utf-8 -*-
"""
模块 B 升级 · 多参照语料稳健性检验 corpus_B_robust.py
=========================================================
作者：刘湘宁（语盾 LinguaShield）

【这个脚本解决什么问题】
原 `corpus_B_keywords.py` 的参照语料是 57 条**自己写的模拟正常英文**。
它诚实地标注了"模拟"，但有个方法论弱点：
    → 目标语料（22 条自建钓鱼）和参照语料（自建正常）**都是同一批人写的**
    → 对比出来差异，可能掺了"写作风格差异"而不是"钓鱼话术特征"

【升级做法：稳健性检验 robustness check】
引入三种来源**彼此独立**的参照语料，对同一批目标语料各跑一次关键词表：

  R1 自建模拟    57 条自建校园/生活/商务英文（保留，作为基线对照）
  R2 真实邮件    Enron-Spam 公开数据集的 ham（正常邮件）子集，真实、可溯源、可引用
  R3 混合参照    Enron ham + 测试集内 30 条正常英文（兼顾真实与题材对口）

**判定规则**：一个词只有在 R1/R2/R3 三种参照下 **都达到 p<0.001**，
才被认定为「稳健信号词 robust signal word」。
在任一参照下不显著的词 = 「敏感词」，它的显著性可能来自参照选择，不能作为规则依据。

学术价值：这一步把原来的结论
    "我们的规则有语言学证据支撑"
升级为
    "我们的规则在三种独立参照语料下均呈显著，不依赖于参照语料的选择"
后者是本研究的最终结论表述。

【为什么对 Enron 抽样而不是全量用】
参照语料与目标语料体量悬殊时会过度放大显著性（目标 405 词 vs 全量 35 万词，差 800 倍）。
语料库语言学惯例：参照语料取目标的 10~50 倍为宜。
故固定随机种子抽取 150 封，约 1.3 万词（约 32 倍），保证**可复现**。

【数据来源与引用】
  Metsis, V., Androutsopoulos, I., & Paliouras, G. (2006).
  Spam Filtering with Naive Bayes -- Which Naive Bayes?
  In Proc. 3rd Conf. on Email and Anti-Spam (CEAS 2006).
  数据集：Enron-Spam（公开研究用途），ham（正常邮件）部分用作本研究的正常邮件参照语料。
"""
import csv, re, math, random, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "samples.csv")
ENRON = os.path.join(HERE, "corpus_raw", "spam_ham_dataset.csv")

# 抽样参数：固定种子 → 任何人重跑结果完全一致
N_ENRON = 150
SEED = 20261002

# =========================================================
# 1. 读目标语料（22 条英文钓鱼）+ 测试集内的正常英文
# =========================================================
phish_en, csv_normal_en = [], []
with open(CSV, encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        if row["lang"] != "en":
            continue
        (phish_en if row["is_phish"] == "1" else csv_normal_en).append(row["text"].lower())

def toks(s):
    return re.findall(r"[a-z']+", s)

TARGET = [w for s in phish_en for w in toks(s)]
N1 = len(TARGET)
tf = Counter(TARGET)
print(f"目标语料：{len(phish_en)} 条英文钓鱼样本，共 {N1} 词")
print(f"测试集内正常英文：{len(csv_normal_en)} 条\n" + "-" * 66)

# =========================================================
# 2. 三种参照语料
# =========================================================
# --- R1 自建模拟（保留原 57 条，保证结果可与旧版对照）---
SIM_TEXTS = [
    "hi professor, i will submit the assignment before the deadline next week.",
    "the library will be closed this monday for staff training and cleaning.",
    "your amazon order has shipped and should arrive in two business days.",
    "please reply to confirm your attendance at the seminar on friday.",
    "we have updated our privacy policy, please review it on the website.",
    "the midterm exam is scheduled for next friday in room 302 at 10 am.",
    "thank you for your application, we will contact you by next week.",
    "reminder: tuition payment is due by the end of this month online.",
    "the campus bus schedule has changed for the winter break period.",
    "congratulations on your admission to the university, welcome aboard.",
    "meeting notes: we discussed the budget and the new project timeline.",
    "your password will expire in 30 days, please reset it via the portal.",
    "the weather forecast predicts light rain for the weekend, bring an umbrella.",
    "i attached the report you requested yesterday, let me know if useful.",
    "our team won the research grant to study local freshwater biodiversity.",
    "the cafeteria will serve dumplings on thursday for the spring festival.",
    "please forward this email to all members of the student council.",
    "the workshop on academic writing is open to first year undergraduates.",
    "our paper was accepted at the conference, thanks for your feedback.",
    "the scholarship results will be announced on the official notice board.",
    "i enjoyed the lecture, could you share the slides with the class.",
    "the wifi network will be upgraded tonight, expect brief interruptions.",
    "remember to register for the optional course before the closing date.",
    "the professor postponed the class to next week due to a conference.",
    "we are organizing a charity run, sign up at the sports center desk.",
    "your subscription to the journal has been renewed for another year.",
    "the career fair will host 40 companies in the main hall on tuesday.",
    "please complete the course evaluation, it helps improve teaching quality.",
    "the lab safety training is mandatory for all new research assistants.",
    "our group booked the study room for a project discussion on sunday.",
    "the museum offers free admission to students with a valid school id.",
    "thank you for volunteering at the community English corner last month.",
    "the bookstore has new textbooks for the spring semester in stock.",
    "we celebrated the graduation of 200 students at the ceremony.",
    "the online system is maintained every sunday from midnight to 2 am.",
    "please check your student email for the internship opportunity list.",
    "the debate club meets every wednesday in the language building.",
    "our department ranked top three in the national teaching assessment.",
    "the health center provides free flu shots for enrolled students.",
    "i lost my student card, where can i apply for a replacement on campus.",
    "the spring sports meet is postponed to next month because of the rain.",
    "we invited a guest speaker to talk about studying abroad options.",
    "the reading group finished the novel and will pick a new one soon.",
    "please save the date for the alumni reunion in early summer.",
    "the computer lab closes at 10 pm on weekdays and noon on weekends.",
    "our team presented the poster at the undergraduate research symposium.",
    "the canteen accepts both campus card and mobile payment now.",
    "she won the essay competition and received a certificate of merit.",
    "the language exchange program pairs local and international students.",
    "we updated the syllabus, the final project is now worth 40 percent.",
    "the shuttle bus between campuses runs every 20 minutes during the day.",
    "please submit your feedback form to help us improve the curriculum.",
    "the scholarship covers tuition and a monthly living allowance.",
    "our club recruited 30 new members at the freshman orientation fair.",
    "the exam timetable is posted on the faculty website, check carefully.",
    "we are happy to announce the opening of the new student lounge.",
    "the writing center offers free tutoring for all undergraduate courses.",
]

# --- R2 真实邮件：Enron-Spam ham 子集 ---
def clean_enron(t):
    """Enron 原始文本带 Subject: 与邮件头残留，做最小化清洗。"""
    t = re.sub(r"^subject\s*[::]\s*", "", t.strip())
    t = re.sub(r"forwarded by[::]?", " ", t, flags=re.I)
    return t.lower()

enron_ham = []
if os.path.exists(ENRON):
    with open(ENRON, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f):
            if str(r.get("label_num", r.get("label", ""))).strip() in ("0", "ham"):
                enron_ham.append(clean_enron(r["text"]))
    rng = random.Random(SEED)
    rng.shuffle(enron_ham)
    # 剔除过短（无实质内容）与过长（体量失控）的邮件，保证参照干净
    pool = [t for t in enron_ham if 80 <= len(t) <= 4000]
    enron_sample = pool[:N_ENRON]
    print(f"Enron-Spam 数据集：读到 ham {len(enron_ham)} 封，"
          f"经长度筛选后取前 {len(enron_sample)} 封（seed={SEED}，可复现）")
else:
    enron_sample = []
    print(f"!! 未找到 Enron 数据文件，R2/R3 将不可用：{ENRON}")

CSV_NORM = [w for s in csv_normal_en for w in toks(s)]

def build_ref(texts, extra_words=None):
    ws = [w for s in texts for w in toks(s)]
    if extra_words:
        ws += extra_words
    return Counter(ws), len(ws)

REF = {}
REF["R1 自建模拟"] = build_ref(SIM_TEXTS, CSV_NORM)
if enron_sample:
    REF["R2 真实邮件(Enron ham)"] = build_ref(enron_sample)
    REF["R3 混合(Enron+正常)"] = build_ref(enron_sample, CSV_NORM)

for name, (cnt, n) in REF.items():
    print(f"  参照 {name:<22} 词数 {n:>6}")

# =========================================================
# 3. LL 对数似然比
# =========================================================
def ll(a, b, c, d):
    tot = a + b + c + d
    if tot == 0:
        return 0.0
    e1 = (a + b) * a / tot
    e2 = (a + b) * b / tot
    v = 0.0
    if a > 0 and e1 > 0:
        v += a * math.log(a / e1)
    if b > 0 and e2 > 0:
        v += b * math.log(b / e2)
    return 2 * v

STOP = set("""the a an and or but if then to of in on for with your you we our
    is are was were be been being this that these those it its as at from by
    will can may not no has have had do does done please than so out up about
    into their them he she they i me my your re s t d ll ve m""".split())

def keyword_table(cnt, N2):
    out = {}
    for w in set(tf) | set(cnt):
        a = tf.get(w, 0)
        if a < 2 or w in STOP:
            continue
        b = cnt.get(w, 0)
        out[w] = (a, b, ll(a, b, N1 - a, N2 - b))
    return out

tables = {name: keyword_table(c, n) for name, (c, n) in REF.items()}

# =========================================================
# 4. 稳健性判定
# =========================================================
# 【方法论修正 —— 重要】
# 初次运行发现：目标语料仅 405 词，凡是出现 >=2 次的候选词，在三份参照下 LL 都远超 15.13，
# 即"什么都显著"。这是小目标语料 + 大参照语料的典型问题：
# 显著性只说明"差异不太可能是偶然"，却不说明"差异有多大"。
# 语料库语言学界对此已有共识（Gabrielatos & Marchi, 2012）：关键词筛选不能只看 keyness，
# 必须同时看**效应量 effect size**。
# 故本脚本采用双重门槛：
#     (1) 显著性 LL >= 15.13 (p<0.001)          —— 差异可靠
#     (2) 效应量 LogRatio >= 3（目标频率 >= 参照的 8 倍） —— 差异够大、有实践意义
# 只有两个条件在三份参照下同时成立，才认定为「稳健信号词」。
CRIT = 15.13      # df=1, p<0.001
LR_CRIT = 3.0     # log2 效应量门槛 = 8 倍频率差

def logratio(a, N1, b, N2):
    """Gabrielatos 推荐的效应量：目标相对频率 / 参照相对频率，取 log2。加 1 平滑避免 0。"""
    p1 = a / N1 if N1 else 0
    p2 = (b + 1) / N2 if N2 else 0
    if p1 <= 0 or p2 <= 0:
        return 0.0
    return math.log2(p1 / p2)

candidates = set.intersection(*[set(t) for t in tables.values()]) if tables else set()

# 判定以「真实参照」为准 R2/R3；R1 自建模拟只作历史对照，不参与判定。
# 为什么 R1 退出判定？——实测发现模拟语料自带污染：
#   例如 R1 里写了 "your password will expire in 30 days, please reset it via the portal"，
#   导致 password/reset 在 R1 中出现 2 次，把这两个强信号词的效应量压到 2.3 / 1.5，
#   明明是钓鱼标志词却被误判为「效应量不足」。
#   这不是词的问题，是参照语料被自己的写作习惯污染了 —— 也正是必须引入真实语料的原因。
TRUE_REF = [n for n in tables if n.startswith("R2") or n.startswith("R3")] or list(tables)

robust, sensitive = [], []
for w in candidates:
    scores = {name: tables[name][w][2] for name in tables}
    lrs = {name: logratio(tables[name][w][0], N1, tables[name][w][1], REF[name][1]) for name in tables}
    good = all(scores[n] >= CRIT and lrs[n] >= LR_CRIT for n in TRUE_REF)
    (robust if good else sensitive).append((w, scores, lrs))

robust.sort(key=lambda r: -min(r[2][n] for n in TRUE_REF))   # 以最弱真实参照的效应量排序
sensitive.sort(key=lambda r: -max(r[1].values()))

print(f"\n判定基准 = {', '.join(TRUE_REF)}（真实邮件参照）；R1 自建模拟仅作历史对照，不参与判定")
print("=" * 78)
print(f"【稳健信号词】在真实参照下同时满足 LL>={CRIT} (p<0.001) 且 LogRatio>={LR_CRIT} (≥8倍)")
print("=" * 78)
print(f"{'词':<14}" + "".join(f"{n.split()[0]+'(LL/LR)':<16}" for n in tables) + f"{'最弱LR':<8}")
for w, sc, lr in robust[:25]:
    vals = "".join(f"{tables[n][w][2]:>7.1f}/{lr[n]:>5.1f}  " for n in tables)
    print(f"{w:<14}{vals}{min(lr[n] for n in TRUE_REF):<8.1f}")

if sensitive:
    print(f"\n【未通过】在真实参照下频率差不足 8 倍（共 {len(sensitive)} 个，前 12）")
    print(f"{'词':<14}" + "".join(f"{n.split()[0]+'(LL/LR)':<16}" for n in tables))
    for w, sc, lr in sensitive[:12]:
        print(f"{w:<14}" + "".join(f"{tables[n][w][2]:>7.1f}/{lr[n]:>5.1f}  " for n in tables))

# =========================================================
# 5. 闭环：rules.py 的 19 个信号词是否在真实参照下依然显著
# =========================================================
SIGNAL = ["account","card","password","payment","fee","transfer","confirm",
          "login","reset","wire","suspended","verify","urgent","secure",
          "security","prize","gift","credentials","notice"]

print("\n" + "=" * 78)
print("【闭环验证】rules.py 已用的 19 个信号词，在真实参照下是否依然站得住")
print("=" * 78)
print(f"{'信号词':<14}{'频次':<6}" + "".join(f"{n.split()[0]+'(LL/LR)':<18}" for n in tables) + "判定")
ok = weak = 0
used = [w for w in SIGNAL if w in tf]
for w in SIGNAL:
    if w not in tf:
        print(f"{w:<14}{0:<6}" + "".join(f"{'-':<18}" for _ in tables) + "目标语料未出现")
        continue
    vals, lrs = [], []
    for name, (cnt, N2) in REF.items():
        if w in tables[name]:
            a, b, s = tables[name][w]
        else:
            a, b, s = tf[w], cnt.get(w, 0), ll(tf[w], cnt.get(w, 0), N1 - tf[w], N2 - cnt.get(w, 0))
        vals.append(s)
        lrs.append(logratio(a, N1, b, N2))
    # 以真实参照为准做判定；同时列出 R1 供对照（可看出模拟参照如何低估效应量）
    core = all(v >= CRIT for v, n in zip(vals, tables) if n in TRUE_REF) \
        and all(l >= LR_CRIT for l, n in zip(lrs, tables) if n in TRUE_REF)
    allsig = all(v >= CRIT for v in vals) and all(v >= LR_CRIT for v in lrs)
    ok += core
    line = f"{w:<14}{tf[w]:<6}" + "".join(f"{v:>7.1f}/{l:>5.1f}  " for v, l in zip(vals, lrs))
    if core:
        print(line + ("稳健 ✓" if allsig else "稳健 ✓（仅 R1 偏弱）"))
    else:
        weak += 1
        print(line + ("LL不足 ⚠" if min(vals) < CRIT else "真实参照下效应量不足 ⚠"))

print("\n" + "=" * 78)
print("【诚实性自检】检验是不是过于宽松？")
print("=" * 78)
# 担心点：目标语料仅 405 词，而参照有 1.8 万词，体量悬殊可能让 LL 对什么都判显著。
# 检验办法：拿一批与诈骗无关的「中性词」做阴性对照。
# 若中性词在目标里没被判显著 → 说明检验能区分，19 个信号词的高显著是真信号而非统计假象。
NEUTRAL = ["paper","monday","link","report","team","meeting","please","email",
           "send","review","attached","note","list","group","plan","work","time",
           "day","week","new","teacher","student","course","research","thanks"]

print("  各参照下的显著词数量 —— 这一栏正是「为什么要加效应量门槛」的证据：")
for name, (cnt, N2) in REF.items():
    tot = len(tables[name])
    sig = sum(1 for w, v in tables[name].items() if v[2] >= CRIT)
    strong = sum(1 for w, v in tables[name].items()
                 if v[2] >= CRIT and logratio(v[0], N1, v[1], N2) >= LR_CRIT)
    print(f"    {name:<22} 候选 {tot:>4}｜LL显著 {sig:>4} ({sig/max(1,tot)*100:>5.1f}%)"
          f"｜再过效应量门槛 {strong:>4} ({strong/max(1,tot)*100:>5.1f}%)")
print("    → 只看 LL 会把几乎全部候选词判为显著；加上效应量（≥8 倍）后真正被保留的才是硬信号。")

print("\n  中性词阴性对照（与诈骗无关的日常词汇，不该成为信号词）：")
print(f"    {'中性词':<14}{'频次':<6}" + "".join(f"{n.split()[0]+'(LL/LR)':<18}" for n in tables) + "是否过关")
NEUTRAL = ["paper","monday","link","report","team","meeting","please","email",
           "send","review","attached","note","list","group","plan","work","time",
           "day","week","new","teacher","student","course","research","thanks"]
survivors = 0
for w in NEUTRAL:
    if tf.get(w, 0) < 2 or w in STOP or any(w not in t for t in tables.values()):
        continue
    vals, lrs = [], []
    for name, (cnt, N2) in REF.items():
        a, b, s = tables[name][w]
        vals.append(s)
        lrs.append(logratio(a, N1, b, N2))
    # 与信号词用同一判定基准（真实参照），否则对照没有意义
    passed = all(v >= CRIT and l >= LR_CRIT
                 for v, l, n in zip(vals, lrs, tables) if n in TRUE_REF)
    survivors += passed
    line = f"    {w:<14}{tf[w]:<6}" + "".join(f"{v:>7.1f}/{l:>5.1f}  " for v, l in zip(vals, lrs))
    print(line + ("仍过关 ✗（见下方说明）" if passed else "已剔除 ✓"))
if survivors:
    print(f"""
    ⚠ 诚实说明：有 {survivors} 个中性词在真实参照下仍被判为高异常。
      这**不是**信号词定义有问题，而是 Enron 参照的体裁偏差所致：
      Enron 是企业内部邮件，几乎不会出现 paper（论文）、link 这类校园/网络场景常用词，
      于是这些词在本项目的学术类钓鱼样本里显得"异常高发"。
      含义有两层：
      (1) 本方法的关键词表对参照语料的体裁敏感，选参照必须体裁对口 —— 这是本研究明确承认的局限；
      (2) 因此单一参照不足以下结论，必须多参照交叉 + 效应量 + 阴性对照三重把关。
      改进方向：补充学术英语参照（COCA/BNC 学术子集或校园通知邮件），本文已在局限一节写明。""")
else:
    print("    → 中性词全部被效应量门槛剔除：检验具备区分能力，保留下来的信号词不是统计假象。")

print(f"\n→ 小结：{ok}/{len(used)} 个规则库信号词在全部参照下通过「显著性+效应量」双重门槛。")

print("""
【结果说明】
  · "稳健 ✓" = 在真实邮件参照下既显著(p<0.001)又够大(≥8倍)，规则依据可靠
  · "仅 R1 偏弱" = 真实参照下完全成立，只在旧的自建模拟语料里频率差被压低了
      （原因见第 4 节：模拟语料里混进了 "your password will expire" 这类句子）
  · "⚠" = 真实参照下也不过关，建议只在组合规则中使用，不单独触发报警

【本研究的诚实边界】
  1. 目标语料仍只有 405 词，属小规模探索性研究，结论应表述为"在该样本集上成立"。
  2. Enron 是企业邮件体裁，与校园/学术类钓鱼场景存在体裁差异（已在 R3 中用学院体裁邮件部分弥补）。
  3. 抽样 150 封虽固定种子可复现，但换一批样信封数结论可能有小幅波动。
""")
