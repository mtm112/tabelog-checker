# GitHubアップロード手順

このアプリをGitHubにアップロードする手順です。

## ⚠️ 重要な注意事項

### プライベートリポジトリの使用を推奨

個人利用のみの場合、**プライベートリポジトリ**を作成することを強く推奨します。

1. GitHubでリポジトリを作成する際、「Private」を選択git add .
2. これにより、コードが一般公開されません

### 機密情報について

以下の機密情報はコードから削除済みです。Streamlit CloudのSecrets機能で管理してください：

- LINE Messaging APIのトークン
- LINE Messaging APIのユーザーID
- Googleスプレッドシートの認証情報
- メール通知のSMTP設定

## アップロード手順

### 1. Gitリポジトリの初期化

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git init
```

### 2. ファイルをステージング

```bash
git add .
```

### 3. 初回コミット

```bash
git commit -m "Initial commit: 食べログチェッカーアプリ"
```

### 4. GitHubでリポジトリを作成

1. [GitHub](https://github.com)にログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ名を入力（例：`tabelog-checker`）
4. **「Private」を選択**（重要！）
5. 「Create repository」をクリック

### 5. Personal Access Tokenを作成

デバイス認証画面で進めない場合は、Personal Access Tokenを使用してください。

1. [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. 「Generate new token (classic)」をクリック
3. 以下の設定：
   - **Note**: `tabelog-checker`
   - **Expiration**: お好みの期間
   - **Select scopes**: `repo`にチェック
4. 「Generate token」をクリック
5. **表示されたトークンをコピー**（後で表示されません）

詳細は`GITHUB_AUTH_GUIDE.md`を参照してください。

### 6. リモートリポジトリを追加してプッシュ

```bash
git remote add origin https://github.com/あなたのユーザー名/tabelog-checker.git
git branch -M main
git push -u origin main
```

**認証情報の入力:**
- **Username**: あなたのGitHubユーザー名
- **Password**: 作成したPersonal Access Token（パスワードの代わりに入力）

## Streamlit Cloudでの設定

### 1. Streamlit Cloudに接続

1. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
2. GitHubアカウントでログイン
3. 「New app」をクリック
4. 作成したリポジトリを選択

### 2. アプリ設定

- **Main file path**: `app.py`
- **Python version**: 3.11（推奨）

### 3. Secrets設定

「Secrets」タブで以下の設定を追加：

#### LINE Messaging API設定

```toml
[notifier]
LINE_MESSAGING_ENABLED = true
LINE_MESSAGING_CHANNEL_ACCESS_TOKEN = "あなたのチャネルアクセストークン"
LINE_MESSAGING_USER_ID = "あなたのユーザーID"
```

#### メール通知設定（使用する場合）

```toml
[notifier]
EMAIL_ENABLED = true
EMAIL_TO = "送信先メールアドレス"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "送信元メールアドレス"
SMTP_PASSWORD = "アプリパスワード"
```

#### Googleスプレッドシート設定

`GOOGLE_SHEETS_SETUP.md`を参照してください。

### 4. デプロイ

「Deploy!」をクリックしてデプロイを開始します。

## セキュリティチェックリスト

アップロード前に以下を確認してください：

- [ ] プライベートリポジトリを作成した
- [ ] 機密情報がコードに含まれていない
- [ ] `.gitignore`に機密ファイルが含まれている
- [ ] `test_line_messaging.py`が削除されている
- [ ] Streamlit Secretsに必要な設定を追加した

## トラブルシューティング

### 認証エラー

- Streamlit Secretsに正しく設定されているか確認
- トークンやIDに余分なスペースや改行が含まれていないか確認

### インポートエラー

- `requirements.txt`に必要なパッケージがすべて含まれているか確認
- Streamlit Cloudのログを確認

## 今後の更新方法

コードを更新した場合：

```bash
git add .
git commit -m "更新内容の説明"
git push origin main
```

Streamlit Cloudは自動的に再デプロイされます。
