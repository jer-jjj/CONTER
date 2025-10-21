#!/bin/bash
# 点名器启动脚本 - Linux/macOS

echo "正在启动点名器..."
echo

# 激活虚拟环境并运行应用
source .venv/bin/activate
python main.py
