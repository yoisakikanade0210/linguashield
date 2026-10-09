# -*- coding: utf-8 -*-
"""
run_holdout.py —— 留出样本（hold-out）真实检验
======================================================================
为什么需要这个脚本？
--------------------------------------------------
samples.csv 的 134 条样本和 rules.py 的规则是"同一只手"写出来的，
在它上面跑出 100% 是**必然**的，说明不了泛化能力 —— 这叫过拟合，
是评审老师最容易质疑的一点。

所以本脚本读入 `holdout/holdout_agri.csv`：一组**撰写规则时刻意
没参考过的**农业国际合作邮件（32 条，16 钓鱼 / 16 正常），
用来回答一个诚实的问题：
    "遇到没见过的邮件，语盾·农信 还准不准？"

运行：python run_holdout.py
输出：控制台 + 留出检验报告.txt

★ 使用规范：holdout 一旦跑过，就不能再拿它来调规则。
  如果调了规则再跑，它就退化成普通测试集了。要重新留出新的。
"""

import csv
import os
from engine import analyze

HOLDOUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "holdout", "holdout_agri.csv")
ALERT_LEVELS = ("高危", "可疑")


def main():
    try:
        rows = []
        with open(HOLDOUT, "r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("text") and row["text"].strip():
                    rows.append(row)
    except FileNotFoundError:
        print(f"找不到留出样本：{HOLDOUT}")
        return

    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

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
    acc = (tp + tn) / total if total else 0
    prec = tp / (tp + fp) if (tp + fp) else 0
    rec = tp / (tp + fn) if (tp + fn) else 0
    fpr = fp / (fp + tn) if (fp + tn) else 0

    out("=" * 70)
    out("  语盾·农信 · 留出样本（hold-out）真实检验报告")
    out("=" * 70)
    out("  说明：本组样本在撰写规则时**未参考过**，用于检验泛化能力，")
    out("        是比 samples.csv 更诚实的指标。")
    out("")
    out(f"  样本总数：{total}（钓鱼 {tp + fn} 条 / 正常 {fp + tn} 条）")
    out("")
    out("  【混淆矩阵】")
    out(f"    抓对钓鱼(TP) = {tp}     漏报(FN) = {fn}")
    out(f"    误报(FP)     = {fp}     正确放行(TN) = {tn}")
    out("")
    out("  【核心指标】")
    out(f"    准确率 Accuracy  = {acc * 100:.1f}%")
    out(f"    精确率 Precision = {prec * 100:.1f}%")
    out(f"    召回率 Recall    = {rec * 100:.1f}%")
    out(f"    误报率 FPR       = {fpr * 100:.1f}%")
    out("")

    out(f"  【未通过案例】共 {len(failures)} 条")
    for sid, scene, kind, score, level in failures:
        out(f"    [{sid}] {scene}  {kind}  得分 {score}  {level}")
    if not failures:
        out("    （无）")
    out("")
    out("=" * 70)

    with open("留出检验报告.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n>>> 已生成 留出检验报告.txt")


if __name__ == "__main__":
    main()
