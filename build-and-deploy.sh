#!/bin/bash
# 构建前端并同步到 nginx 静态目录，然后重载 nginx

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
DIST_TARGET="/var/www/test.keqiao.wang"

echo "==> 1. 构建前端..."
cd "$FRONTEND_DIR"
npm run build

echo "==> 2. 同步到 $DIST_TARGET ..."
mkdir -p "$DIST_TARGET"
cp -r "$FRONTEND_DIR/dist/"* "$DIST_TARGET/"

echo "==> 3. 重载 nginx..."
nginx -t 2>&1 | grep -q "syntax ok" && nginx -s reload

echo "✅ 部署完成"
