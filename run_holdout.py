


import csv
import os
from engine import analyze

BASE = os.path.dirname(os.path.abspath(__file__))
ALERT_LEVELS = ("高危", "可疑")

HOLDOUTS = [
    ("v1", os.path.join(BASE, "holdout", "holdout_agri.csv"),
     "2026-10-02 轮 · 首批农业留出样本（已用于调规则，不可再作泛化证据）"),
    ("v2", os.path.join(BASE, "holdout", "holdout_agri_v2.csv"),
     "2026-10-09 轮 · 语料扩建后第二批（已被用于调规则，不可再作泛化证据）"),
    ("v3", os.path.join(BASE, "holdout", "holdout_v3.csv"),
     "2026-10-09 终验 · 全新品类与场景，规则定稿后一次性运行 ★当前唯一有效证据"),
]


def run_one(path):
    
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            rows = [r for r in csv.DictReader(f)
                    if r.get("text") and r["text"].strip()]
    except FileNotFoundError:
        return None

    tp = fp = tn = fn = 0
    failures = []
    for row in rows:
        truth = row["is_phish"].strip() == "1"
        r = analyze(row["text"])
        alerted = r["level"].startswith(ALERT_LEVELS)
        if truth and alerted:
            tp += 1
        elif truth and not alerted:
            fn += 1
            failures.append((row["id"], row["scene"], "漏报", r["score"], r["level"]))
        elif (not truth) and alerted:
            fp += 1
            failures.append((row["id"], row["scene"], "误报", r["score"], r["level"]))
        else:
            tn += 1

    total = tp + fp + tn + fn
    stat = {
        "total": total,
        "acc": (tp + tn) / total if total else 0,
        "prec": tp / (tp + fp) if (tp + fp) else 0,
        "rec": tp / (tp + fn) if (tp + fn) else 0,
        "fpr": fp / (fp + tn) if (fp + tn) else 0,
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
    }
    return stat, failures


def main():
    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

    out("=" * 70)
    out("  语盾·农信 · 留出样本（hold-out）真实检验报告")
    out("=" * 70)
    out("  说明：留出样本在撰写规则时**未参考过**，用于检验泛化能力，")
    out("        是比 samples.csv 更诚实的指标。")
    out("")

    summary = []
    for tag, path, desc in HOLDOUTS:
        result = run_one(path)
        out("-" * 70)
        out(f"  【留出集 {tag}】{desc}")
        out(f"  文件：{os.path.basename(path)}")
        if result is None:
            out("  （文件不存在，跳过）")
            out("")
            continue
        stat, failures = result
        out(f"  样本 {stat['total']} 条（钓鱼 {stat['tp'] + stat['fn']} / 正常 {stat['fp'] + stat['tn']}）")
        out(f"    准确率 {stat['acc'] * 100:5.1f}%   精确率 {stat['prec'] * 100:5.1f}%"
            f"   召回率 {stat['rec'] * 100:5.1f}%   误报率 {stat['fpr'] * 100:5.1f}%")
        out(f"    混淆矩阵：TP={stat['tp']}  FN={stat['fn']}  FP={stat['fp']}  TN={stat['tn']}")
        out(f"    未通过 {len(failures)} 条：")
        for sid, scene, kind, score, level in failures:
            out(f"      [{sid}] {scene}  {kind}  {score}分  {level}")
        if not failures:
            out("      （无）")
        out("")
        summary.append((tag, stat, len(failures)))


    if summary:
        out("=" * 70)
        out("  【三轮汇总】")
        out("")
        out("    留出集   条数   准确率    精确率    召回率    误报率   首跑召回")

        first_run = {"v1": "61.1%", "v2": "50.0%", "v3": "20.0%"}
        for tag, stat, nf in summary:
            out(f"      {tag}     {stat['total']:>3}   "
                f"{stat['acc'] * 100:>6.1f}%  {stat['prec'] * 100:>6.1f}%  "
                f"{stat['rec'] * 100:>6.1f}%  {stat['fpr'] * 100:>6.1f}%  "
                f"{first_run.get(tag, '—'):>8}")
        out("")
        out("  ★「首跑召回」是该留出集**第一次**、且未参照它调整任何规则时的成绩。")
        out("    它才是泛化能力的真实刻度；调整后再跑的数字只能说明"
            "「改完之后当然不忘」。")
        out("")

        tot_norm = sum(s["fp"] + s["tn"] for _, s, _ in summary)
        tot_fp = sum(s["fp"] for _, s, _ in summary)
        out(f"  【最重要的一个数字】三轮共 {tot_norm} 条真实场景正常邮件，"
            f"误报 {tot_fp} 条。")
        out("    在本项目的设计取舍里（漏报:误报成本比约 5480:1），"
            "宁可漏、不可冤枉 ——")
        out("    这一点始终没有失守。")
        out("")

    out("=" * 70)
    out("  【方法与诚实性说明】")
    out("")
    out("    · v1 首跑 61.1%，据此补齐三条规则缺陷后达 100%；")
    out("      v2 首跑 50.0%，据此补齐五类词汇空缺（含中文敬语变体）后达 83.3%；")
    out("      v3 首跑 20.0%，**规则未再改动**，保留原样作为当前泛化能力的真实刻度。")
    out("    · v1/v2 的数字已经是「事后记忆」，不再代表泛化能力；")
    out("      任何时候要引用泛化指标，都应当引用 v3 的 20.0%。")
    out("    · 三轮首跑数字逐次下降，一个重要原因是语料本身在有意")
    out("      脱离套路写法（每次都换新品类、新场景下笔）；")
    out("      压测越严格，暴露的缺口越真实。这个下降应当被如实陈述，")
    out("      而不是挑选对自己有利的那一轮来汇报。")
    out("=" * 70)

    with open("留出检验报告.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n>>> 已生成 留出检验报告.txt")


if __name__ == "__main__":
    main()
