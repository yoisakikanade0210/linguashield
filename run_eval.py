# -*- coding: utf-8 -*-
"""
run_eval.py —— 100 条测试集评测
=================================================
用途：读取 samples.csv 里的样本，逐条跑检测引擎，
      算出 准确率 / 精确率 / 召回率 / 误报率，并生成评测报告。

运行：python run_eval.py
输出：控制台 + 评测报告.txt

和 run_test.py 的区别：
    run_test.py  = 8 条硬编码样本，给老师演示"原型能跑"
    run_eval.py  = 从 CSV 读任意条数，出真实统计数据 ← 国庆要用的
"""

import csv
from collections import defaultdict
from engine import analyze

# 判为这两档，就认为工具"报警了"
# startswith 可以接收元组，所以这两档开头都算报警
ALERT_LEVELS = ("高危", "可疑")

# 场景 -> [错误条数, 总条数]，用来看哪个场景最薄弱
scene_stat = defaultdict(lambda: [0, 0])


def load_samples(path="samples.csv"):
    """
    读取 CSV 测试集。

    ★★ 这里有一个必须记住的坑：encoding='utf-8-sig'，不能写 'utf-8'。

    原因：Excel 保存 CSV 时会在文件最开头偷偷加一个 BOM 标记。
    如果用 'utf-8' 读，第一行表头会变成 '\\ufeffid' 而不是 'id'，
    后面 row["id"] 全部取到空值，报错报得莫名其妙。
    'utf-8-sig' 会自动把这个标记去掉。
    """
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)   # DictReader：按表头取，不用记第几列
        for row in reader:
            # 跳过没填正文的空行（Excel 里经常留下空行）
            if not row.get("text") or not row["text"].strip():
                continue
            rows.append(row)
    return rows


def judge(text):
    """跑一次引擎，返回 (分数, 等级, 是否报警, 理由列表)"""
    r = analyze(text)
    alerted = r["level"].startswith(ALERT_LEVELS)
    return r["score"], r["level"], alerted, r["reasons"]


def safe_div(a, b):
    """安全除法：分母是 0 时返回 0，避免 ZeroDivisionError 崩溃"""
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

    # 混淆矩阵的四个格子
    tp = fp = tn = fn = 0
    failures = []       # 判错的条目，报告里要如实列出来
    lines = []

    def out(s=""):
        print(s)
        lines.append(s)

    for row in samples:
        sid = row.get("id", "").strip()
        scene = row.get("scene", "").strip()
        text = row["text"]
        source = row.get("source", "").strip()

        # 真实标签：1 = 真的是钓鱼，0 = 正常邮件
        # .strip() 是因为 Excel 单元格里可能带空格
        truth = (row.get("is_phish", "").strip() == "1")

        score, level, alerted, reasons = judge(text)
        scene_stat[scene][1] += 1

        # ---- 填混淆矩阵 ----
        if truth and alerted:
            tp += 1                                  # 抓对了的钓鱼
        elif truth and not alerted:
            fn += 1                                  # 漏报：钓鱼溜过去了
            scene_stat[scene][0] += 1
            failures.append((sid, scene, "漏报（钓鱼没抓到）", score, level, source))
        elif (not truth) and alerted:
            fp += 1                                  # 误报：正常邮件被冤枉
            scene_stat[scene][0] += 1
            failures.append((sid, scene, "误报（正常被判危险）", score, level, source))
        else:
            tn += 1                                  # 正确放行的正常邮件

    total = tp + fp + tn + fn

    # ---- 四个指标 ----
    accuracy = safe_div(tp + tn, total)              # 整体判断对的比例
    precision = safe_div(tp, tp + fp)                # 报警的里面，真钓鱼占多少
    recall = safe_div(tp, tp + fn)                   # 所有真钓鱼里，抓到了多少
    fpr = safe_div(fp, fp + tn)                      # 正常邮件被误报的比例

    out("=" * 70)
    out("  语盾 LinguaShield · 测试集评测报告")
    out("=" * 70)
    out(f"  样本总数：{total}")
    out(f"    其中钓鱼样本 {tp + fn} 条，正常邮件 {fp + tn} 条（自建测试集，见 source 字段）")
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

    # ---- 分场景表现 ----
    if scene_stat:
        out("  【分场景错误分布】")
        for scene, (err, cnt) in sorted(scene_stat.items(), key=lambda x: -x[1][0]):
            mark = "  ← 最薄弱" if err and cnt and err / cnt >= 0.3 else ""
            out(f"    {scene:<24} 错误 {err}/{cnt}{mark}")
        out("")

    # ---- 失败清单（报告的精华）----
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

    # 写报告
    with open("评测报告.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n>>> 已生成 评测报告.txt")


if __name__ == "__main__":
    main()
