# 语盾 LinguaShield · 源码说明

面向大学生的中英双语钓鱼文本检测工具。
作者：匿名（Anonymous）

---

## 一、文件说明

| 文件 | 作用 |
|---|---|
| `rules.py` | 规则库：中英文话术组、组权重、组合规则 |
| `engine.py` | 检测引擎：语言判定、打分、判定理由生成 |
| `gen_samples.py` | 生成测试集 `samples.csv` |
| `samples.csv` | 104 条标注测试集（source 字段逐条注明来源） |
| `run_eval.py` | 评测脚本，输出四项指标与混淆矩阵 |
| `ablation.py` | 三档消融实验 |
| `run_test.py` | 单条文本快速测试 |
| `corpus_B_keywords.py` | 关键词表与话步分析 |
| `corpus_B_robust.py` | 多参照稳健性检验（含效应量门槛与阴性对照） |
| `评测报告.txt` / `稳健性检验报告.txt` | 上述脚本的运行输出 |

## 二、运行方式

无需安装任何第三方库，Python 3.8+ 即可：

```bash
python run_eval.py           # 输出四项指标与混淆矩阵
python corpus_B_robust.py    # 输出三参照稳健性检验结果
python ablation.py           # 输出三档消融实验
python run_test.py           # 单条文本测试
```

当前实测结果（104 条自建测试集）：
准确率 99.0% / 精确率 97.8% / 召回率 100% / 误报率 1.7%（TP=44, FN=0, FP=1, TN=59）。

## 三、关于参照语料数据集（重要）

`corpus_B_robust.py` 中的 R2/R3 参照语料来自公开的 **Enron-Spam** 数据集。
因附件体积限制，本包**未包含**该数据文件（原始 CSV 约 5 MB）。

如需完整复现稳健性检验，请自行下载并放置：

1. 下载地址（GitHub 公开镜像）：
   https://raw.githubusercontent.com/muskanchugh-ds/Spam-Email-Classification/master/spam_ham_dataset.csv
2. 在本目录下新建 `corpus_raw/` 文件夹，将文件保存为：
   `corpus_raw/spam_ham_dataset.csv`
3. 重新运行 `python corpus_B_robust.py`

数据出处：
Metsis, V., Androutsopoulos, I., & Paliouras, G. (2006).
*Spam Filtering with Naive Bayes — Which Naive Bayes?* CEAS 2006.

未放置该数据时脚本仍可运行，但会退化为仅使用 R1 自建参照语料。

## 四、已知局限

- 测试集为自建模拟样本，结论应表述为"在该样本集上成立"。
- Enron 属企业邮件体裁，与校园/学术场景存在体裁差异，已在报告中说明。
- 仅检测文本内容，不处理附件与图片型钓鱼。

---

感谢审阅。
