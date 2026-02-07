#!/bin/bash
# 在 VPS 上运行此脚本完成部署（建议：先 ssh 登录 VPS，再执行）
# 用法：bash deploy_vps.sh  或  curl -sL <url> | bash

set -e
INSTALL_DIR="/opt/github/lms_demo"
REPO_URL="https://github.com/bean4896/lms_demo.git"

echo "==> 安装依赖（如未安装）..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv git > /dev/null 2>&1 || true

echo "==> 克隆/更新项目到 $INSTALL_DIR ..."
if [ -d "$INSTALL_DIR/.git" ]; then
  cd "$INSTALL_DIR" && git pull
else
  mkdir -p /opt/github
  git clone "$REPO_URL" "$INSTALL_DIR"
  cd "$INSTALL_DIR"
fi

echo "==> 创建虚拟环境并安装 Python 依赖..."
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

echo "==> 启动 Gunicorn（前台，监听 0.0.0.0:5000）..."
echo "    访问: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_VPS_IP'):5000"
echo "    按 Ctrl+C 停止。要后台运行请用: nohup ... & 或 systemd"
exec venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 "app:app"
