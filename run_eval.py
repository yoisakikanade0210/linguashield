


import csv
from collections import defaultdict
from engine import analyze



ALERT_LEVELS = ("高危", "可疑")


scene_stat = defaultdict(lambda: [0, 0])


def load_samples(path="samples.csv"):
    
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:

            if not row.get("text") or not row["text"].strip():
                continue
            rows.append(row)
    return rows


def judge(text):
    
    r = analyze(text)
    alerted = r["level"].startswith(ALERT_LEVELS)
    return r["score"], r["level"], alerted, r["reasons"]


def safe_div(a, b):
    
    return a / b if b else 0.0


def main():
    try:
        samples = load_samples()
    except FileNotFoundError:
        print("找不到 samples.csv —— 确认文件和 run_eval.py 在同一个文件夹里")
        return
    except UnicodeDecodeError:
        print("编码错误 —— 用 Excel 另存为时请选择「CSV UTF-8」格式")
        return

    if not samples:
        print("samples.csv 里没有读到有效样本（可能全空，或正文列为空）")
        return


    tp = fp = tn = fn = 0
    failures = []
    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

    for row in samples:
        sid = row.get("id", "").strip()
        scene = row.get("scene", "").strip()
        text = row["text"]
        source = row.get("source", "").strip()



        truth = (row.get("is_phish", "").strip() == "1")

        score, level, alerted, reasons = judge(text)
        scene_stat[scene][1] += 1


        if truth and alerted:
            tp += 1
        elif truth and not alerted:
            fn += 1
            scene_stat[scene][0] += 1
            failures.append((sid, scene, "漏报（钓鱼没抓到）", score, level, source))
        elif (not truth) and alerted:
            fp += 1
            scene_stat[scene][0] += 1
            failures.append((sid, scene, "误报（正常被判危险）", score, level, source))
        else:
            tn += 1

    total = tp + fp + tn + fn


    accuracy = safe_div(tp + tn, total)
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    fpr = safe_div(fp, fp + tn)

    out("=" * 70)
    out("  语盾·农信 LinguaShield Agri · 测试集评测报告")
    out("=" * 70)
    out(f"  样本总数：{total}")
    out(f"    其中钓鱼样本 {tp + fn} 条，正常邮件 {fp + tn} 条（自建测试集，见 source 字段）")
    out("    场景覆盖：校园通知 / 学术诈骗 / 农业国际合作（BEC）")
    out("")
    out("  【混淆矩阵】")
    out(f"    抓对钓鱼(TP) = {tp}     漏报(FN) = {fn}")
    out(f"    误报(FP)     = {fp}     正确放行(TN) = {tn}")
    out("")
    out("  【核心指标】")
    out(f"    准确率 Accuracy  = {accuracy * 100:.1f}%")
    out(f"    精确率 Precision = {precision * 100:.1f}%   （工具报警时有多可信）")
    out(f"    召回率 Recall    = {recall * 100:.1f}%   （钓鱼抓得全不全）")
    out(f"    误报率 FPR       = {fpr * 100:.1f}%   （正常邮件被冤枉的比例）★最关键")
    out("")


    if scene_stat:
        out("  【分场景错误分布】")
        for scene, (err, cnt) in sorted(scene_stat.items(), key=lambda x: -x[1][0]):
            mark = "  ← 最薄弱" if err and cnt and err / cnt >= 0.3 else ""
            out(f"    {scene:<24} 错误 {err}/{cnt}{mark}")
        out("")


    out(f"  【失败案例清单】共 {len(failures)} 条")
    if failures:
        for sid, scene, kind, score, level, source in failures:
            out(f"    [{sid}] {scene}")
            out(f"          {kind}    得分 {score}  判定 {level}")
            if source:
                out(f"          来源：{source}")
    else:
        out("    （无失败案例）")
    out("")
    out("=" * 70)


    with open("评测报告.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n>>> 已生成 评测报告.txt")


if __name__ == "__main__":
    main()
