# GitHub認証エラー解決ガイド

デバイス認証画面で進めない場合の対処法です。

## 解決方法：Personal Access Token（PAT）を使用

デバイス認証の代わりに、Personal Access Tokenを使用してGitHubに接続します。

### ステップ1: Personal Access Tokenを作成

詳細な手順は`CREATE_TOKEN_STEP_BY_STEP.md`を参照してください。

**簡易手順:**
1. [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)にアクセス
2. 「Generate new token (classic)」をクリック
3. 以下の設定を入力：
   - **Note**: `tabelog-checker`（任意の名前）
   - **Expiration**: `No expiration`（個人利用の場合）または`90 days`
   - **Repository access**: 「All repositories」を選択（重要！）
   - **Permissions**: 「Account」セクションで「+ Add permissions」をクリック
     - **Repository permissions** → ✅ `repo`（すべてのチェックボックス）
4. 「Generate token」をクリック
5. **重要**: 表示されたトークンをコピーして安全に保管（後で表示されません）

### ステップ2: トークンを使用してGitHubに接続

ターミナルで以下のコマンドを実行：

```bash
cd /Volumes/mitomo_SSD/tabelog_checker

# Gitリポジトリを初期化（まだの場合）
git init

# ファイルを追加
git add .

# 初回コミット
git commit -m "Initial commit: 食べログチェッカーアプリ"

# リモートリポジトリを追加
# 注意: リポジトリは事前にGitHubで作成しておく（プライベート推奨）
git remote add origin https://github.com/あなたのユーザー名/tabelog-checker.git

# ブランチ名を設定
git branch -M main

# プッシュ（ユーザー名とパスワードの代わりにトークンを使用）
git push -u origin main
```

**認証情報の入力:**
- **Username**: あなたのGitHubユーザー名
- **Password**: 作成したPersonal Access Token（パスワードの代わりに入力）

### ステップ3: 認証情報を保存（オプション）

次回から認証情報を入力しなくて済むようにする：

```bash
# Git Credential Helperを設定
git config --global credential.helper osxkeychain
```

これで、次回からは自動的に認証情報が使用されます。

## 代替方法：SSH認証を使用

Personal Access Tokenの代わりにSSH認証を使用することもできます。

### SSH鍵の設定

1. SSH鍵を生成（まだ持っていない場合）：
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. SSH鍵をGitHubに登録：
   - [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys)
   - 「New SSH key」をクリック
   - 公開鍵（`~/.ssh/id_ed25519.pub`）の内容をコピーして貼り付け

3. リモートURLをSSHに変更：
```bash
git remote set-url origin git@github.com:あなたのユーザー名/tabelog-checker.git
```

## トラブルシューティング

### エラー: "remote: Support for password authentication was removed"

→ Personal Access Tokenを使用してください（上記の手順を参照）

### エラー: "Permission denied"

→ リポジトリへのアクセス権限を確認してください

### デバイス認証画面が表示される

→ Personal Access TokenまたはSSH認証を使用してください
