# Streamlit Cloud デプロイガイド

このアプリをStreamlit Cloudで公開する手順です。

## デプロイ手順

### 1. GitHubにリポジトリをプッシュ

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/あなたのユーザー名/tabelog_checker.git
git push -u origin main
```

### 2. Streamlit Cloudでデプロイ

1. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
2. 「New app」をクリック
3. GitHubリポジトリを選択
4. 以下の設定を入力：
   - **Main file path**: `app.py`
   - **Python version**: 3.11（推奨）
5. 「Deploy!」をクリック

### 3. 環境変数・シークレットの設定（オプション）

通知機能を使用する場合、Streamlit Cloudのシークレット機能を使用して設定を管理できます。

1. Streamlit Cloudのアプリ設定画面で「Secrets」を開く
2. 以下の形式で設定を追加：

```toml
[notifier]
LINE_MESSAGING_ENABLED = true
LINE_MESSAGING_CHANNEL_ACCESS_TOKEN = "あなたのトークン"
LINE_MESSAGING_USER_ID = "あなたのユーザーID"
```

ただし、現在の実装では設定をコード内に直接記述しているため、シークレット機能は使用していません。

## 注意事項

### ファイルの保存について

- Streamlit Cloudは一時的なストレージを使用します
- アプリを再起動すると、`urls.json`や`results/`ディレクトリの内容は失われる可能性があります
- 永続的な保存が必要な場合は、外部ストレージ（AWS S3、Google Cloud Storageなど）を使用することを検討してください

### スケジュール実行について

- Streamlit Cloudでは`launchd`を使用したスケジュール実行はできません
- スケジュール実行が必要な場合は、別途サーバーで`check_scheduled.py`を実行するか、GitHub ActionsなどのCI/CDサービスを使用してください

### 通知機能について

- LINE Messaging APIの設定は`notifier.py`に直接記述されています
- セキュリティのため、本番環境では環境変数やシークレット管理を使用することを推奨します

## トラブルシューティング

### 依存関係のエラー

`requirements.txt`に必要なパッケージがすべて含まれているか確認してください。

### インポートエラー

ローカル環境とStreamlit Cloudの環境が異なる場合、パスの問題が発生する可能性があります。
相対インポートを使用している場合は、絶対インポートに変更することを検討してください。

### メモリ不足

大量のURLをチェックする場合、Streamlit Cloudのメモリ制限に達する可能性があります。
アクセス間隔を調整するか、チェックするURL数を制限してください。
