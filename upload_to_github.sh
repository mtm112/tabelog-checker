#!/bin/bash

# GitHubアップロード用スクリプト

echo "=========================================="
echo "食べログチェッカー GitHubアップロード"
echo "=========================================="
echo ""

# 現在のディレクトリを確認
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 作業ディレクトリ: $SCRIPT_DIR"
echo ""

# Gitリポジトリの初期化確認
if [ ! -d ".git" ]; then
    echo "🔧 Gitリポジトリを初期化します..."
    git init
    echo "✅ 初期化完了"
    echo ""
fi

# ファイルを追加
echo "📦 ファイルを追加します..."
git add .
echo "✅ ファイル追加完了"
echo ""

# ステータス確認
echo "📋 追加されたファイル:"
git status --short
echo ""

# コミット
echo "💾 コミットします..."
read -p "コミットメッセージを入力してください（Enterでデフォルト）: " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: 食べログチェッカーアプリ"
fi
git commit -m "$commit_msg"
echo "✅ コミット完了"
echo ""

# リモートリポジトリの確認
if ! git remote | grep -q "origin"; then
    echo "🔗 リモートリポジトリを設定します..."
    read -p "GitHubリポジトリURLを入力してください（例: https://github.com/ユーザー名/tabelog-checker.git）: " repo_url
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ リモートリポジトリ設定完了"
    else
        echo "❌ リポジトリURLが入力されませんでした"
        exit 1
    fi
    echo ""
fi

# ブランチ名を設定
echo "🌿 ブランチ名を設定します..."
git branch -M main
echo "✅ ブランチ名設定完了"
echo ""

# プッシュ
echo "🚀 GitHubにプッシュします..."
echo "⚠️  認証情報の入力が必要です:"
echo "   - Username: あなたのGitHubユーザー名"
echo "   - Password: Personal Access Token（パスワードの代わり）"
echo ""
read -p "プッシュを実行しますか？ (y/n): " confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    git push -u origin main
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✅ アップロード完了！"
        echo "=========================================="
    else
        echo ""
        echo "=========================================="
        echo "❌ アップロードに失敗しました"
        echo "=========================================="
        echo "以下を確認してください:"
        echo "  - Personal Access Tokenが正しいか"
        echo "  - リポジトリURLが正しいか"
        echo "  - リポジトリが存在するか"
    fi
else
    echo "❌ プッシュをキャンセルしました"
fi
