#!/bin/bash
# 赛博森森成长网站 - 本地预览脚本

echo "🐱 启动赛博森森成长网站本地服务器..."
echo "📂 网站目录: /home/gem/.openclaw/workspace/sensen-website"
echo "🌐 访问地址: http://localhost:8080"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

cd /home/gem/.openclaw/workspace/sensen-website
python3 -m http.server 8080
