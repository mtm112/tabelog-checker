#!/bin/bash

# スケジュール設定スクリプト
# macOSのlaunchdを使用して毎日自動実行を設定します

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_FILE="$SCRIPT_DIR/com.tabelog.checker.plist"
PLIST_NAME="com.tabelog.checker"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "=========================================="
echo "食べログチェッカー スケジュール設定"
echo "=========================================="
echo ""

# ログディレクトリを作成
mkdir -p "$SCRIPT_DIR/logs"
echo "✅ ログディレクトリを作成しました"

# plistファイルのパスを更新
echo "📝 plistファイルのパスを更新中..."
sed -i '' "s|/Volumes/mitomo_SSD/tabelog_checker|$SCRIPT_DIR|g" "$PLIST_FILE"
echo "✅ plistファイルを更新しました"

# 既存の設定をアンロード（存在する場合）
if launchctl list | grep -q "$PLIST_NAME"; then
    echo "📤 既存の設定をアンロード中..."
    launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist" 2>/dev/null || true
fi

# plistファイルをLaunchAgentsにコピー
echo "📋 LaunchAgentsにコピー中..."
cp "$PLIST_FILE" "$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"
echo "✅ plistファイルをコピーしました"

# launchdに登録
echo "🚀 launchdに登録中..."
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"
echo "✅ launchdに登録しました"

echo ""
echo "=========================================="
echo "設定完了！"
echo "=========================================="
echo ""
echo "📅 実行スケジュール:"
echo "   - 毎日 9:00 に実行"
echo "   - 毎月3-10日の間のみ実際にチェックを実行"
echo ""
echo "📋 確認コマンド:"
echo "   launchctl list | grep $PLIST_NAME"
echo ""
echo "🛑 停止コマンド:"
echo "   launchctl unload $LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"
echo ""
echo "▶️  再開コマンド:"
echo "   launchctl load $LAUNCH_AGENTS_DIR/$PLIST_NAME.plist"
echo ""
echo "📁 ログファイル:"
echo "   $SCRIPT_DIR/logs/check.log"
echo "   $SCRIPT_DIR/logs/check_error.log"
echo ""
