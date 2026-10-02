#!/bin/bash
# 语盾 LinguaShield · 推送到 GitHub
# 用法：先在 https://github.com/new 创建名为 linguashield 的 Public 空仓库
#      （不要勾选 README / .gitignore / license），然后双击或运行本脚本。

cd "C:/Users/10508/Desktop/语盾LinguaShield-项目材料/源码_666" || exit 1

git remote remove origin 2>/dev/null
git remote add origin git@github.com:yoisakikanade0210/linguashield.git
git branch -M main

echo "正在推送到 github.com/yoisakikanade0210/linguashield ..."
git push -u origin main

if [ $? -eq 0 ]; then
  echo ""
  echo "推送成功！仓库地址："
  echo "  https://github.com/yoisakikanade0210/linguashield"
else
  echo ""
  echo "推送失败，常见原因："
  echo "  1. 还没在 GitHub 网页上创建 linguashield 仓库"
  echo "  2. 创建时勾选了 README/.gitignore（远程仓库非空，需先 pull）"
fi
