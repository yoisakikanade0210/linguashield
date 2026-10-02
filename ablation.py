# -*- coding: utf-8 -*-
"""
ablation.py —— 三档消融实验
=================================================
用途：验证引擎里每一层（URL / 话术 / 组合）各自贡献了多少。
      对应模块 A「消融实验」学习项 + 国庆交付物「消融实验」。

三档设置：
  Tier 1  仅 URL      ：只用 URL 信誉层打分（关掉话术和组合）
  Tier 2  URL+话术    ：关掉组合层，看单条话术本身够不够
  Tier 3  全量（对照）：URL + 话术 + 组合，即当前 run_eval.py 的结果

报警阈值与 run_eval.py 一致：score >= 40（等级为"可疑/高危"即算报警）。

运行：python ablation.py
"""
import csv
from collections import defaultdict
from engine import (
    normalize, detect_language, check_urls, match_phrases, match_combos, WEIGHTS,
)

ALERT_THRESHOLD = 40  # 与 engine.level_text：>=40 即"可疑/高危"


def load_samples(path="samples.csv"):
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if not row.get("text") or not row["text"].strip():
                continue
            rows.append(row)
    return rows


def score_tier(text, tier):
    """按档位算总分。tier: 1=仅URL, 2=URL+话术, 3=全量"""
    clean = normalize(text)
    lang = detect_language(clean)
    url_score, _, _ = check_urls(clean)

    if tier == 1:
        # 仅 URL 层
        return int(url_score * WEIGHTS["url"])

    phrase_score, _, matched = match_phrases(clean, lang)
    if tier == 2:
        # URL + 话术，关掉组合
        return min(int(phrase_score * WEIGHTS["phrase"] + url_score * WEIGHTS["url"]), 100)

    # tier == 3 全量
    combo_score, _ = match_combos(matched)
    weighted = (
        phrase_score * WEIGHTS["phrase"]
        + combo_score * WEIGHTS["combo"]
        + url_score * WEIGHTS["url"]
    )
    return min(int(weighted), 100)


def evaluate(tier, samples):
    tp = fp = tn = fn = 0
    for row in samples:
        truth = row.get("is_phish", "").strip() == "1"
        score = score_tier(row["text"], tier)
        alerted = score >= ALERT_THRESHOLD
        if truth and alerted:
            tp += 1
        elif truth and not alerted:
            fn += 1
        elif (not truth) and alerted:
            fp += 1
        else:
            tn += 1
    total = tp + fp + tn + fn
    acc = (tp + tn) / total if total else 0
    prec = tp / (tp + fp) if (tp + fp) else 0
    rec = tp / (tp + fn) if (tp + fn) else 0
    fpr = fp / (fp + tn) if (fp + tn) else 0
    return tp, fp, tn, fn, acc, prec, rec, fpr


def main():
    samples = load_samples()
    print("=" * 78)
    print("  语盾 LinguaShield · 三档消融实验（报警阈值 = 分数 ≥ 40）")
    print("=" * 78)
    print(f"  样本总数：{len(samples)}（真实钓鱼 {sum(1 for r in samples if r['is_phish']=='1')} 条）\n")

    names = {
        1: "Tier 1  仅 URL 层（关掉话术+组合）",
        2: "Tier 2  URL + 话术（关掉组合）",
        3: "Tier 3  全量（URL+话术+组合）← 当前线上",
    }
    print(f"  {'配置':<40}{'TP':>4}{'FP':>4}{'TN':>4}{'FN':>4}"
          f"{'准确':>8}{'精确':>8}{'召回':>8}{'FPR':>8}")
    print("  " + "-" * 76)
    for tier in (1, 2, 3):
        tp, fp, tn, fn, acc, prec, rec, fpr = evaluate(tier, samples)
        print(f"  {names[tier]:<40}{tp:>4}{fp:>4}{tn:>4}{fn:>4}"
              f"{acc*100:>7.1f}%{prec*100:>7.1f}%{rec*100:>7.1f}%{fpr*100:>7.1f}%")

    print("\n  【怎么读这张表】")
    print("  · Tier1→Tier2 的差 = 话术库（你英语专业的核心资产）带来的提升")
    print("  · Tier2→Tier3 的差 = 组合规则（多类话术同现才报警）带来的提升")
    print("  · 召回率掉得最多那一档，就是'最不能没有'的那一层")
    print("=" * 78)


if __name__ == "__main__":
    main()
