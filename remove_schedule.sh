#!/bin/bash

# スケジュール削除スクリプト

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.tabelog.checker"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "=========================================="
echo "食べログチェッカー スケジュール削除"
echo "=========================================="
echo ""

# launchdからアンロード
if launchctl list | grep -q "$PLIST_NAME"; then
    echo "📤 launchdからアンロード中..."
    launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist" 2>/dev/null || true
    echo "✅ アンロードしました"
else
    echo "ℹ️  登録されていないようです"
fi

# plistファイルを削除
if [ -f "$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist" ]; then
    echo "🗑️  plistファイルを削除中..."
    rm "$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"
    echo "✅ plistファイルを削除しました"
else
    echo "ℹ️  plistファイルが見つかりませんでした"
fi

echo ""
echo "=========================================="
echo "削除完了！"
echo "=========================================="
