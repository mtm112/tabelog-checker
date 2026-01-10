# Personal Access Tokenを使用してプッシュする方法

## 方法1: URLにトークンを埋め込む（一時的）

**注意**: この方法は一時的なものです。プッシュ後はURLを元に戻すことを推奨します。

```bash
cd /Volumes/mitomo_SSD/tabelog_checker

# リモートURLを変更（トークンを埋め込む）
git remote set-url origin https://mtm112:YOUR_TOKEN@github.com/mtm112/tabelog-checker.git

# プッシュ
git push -u origin main

# プッシュ後、URLを元に戻す（セキュリティのため）
git remote set-url origin https://github.com/mtm112/tabelog-checker.git
```

`YOUR_TOKEN`を実際のPersonal Access Tokenに置き換えてください。

## 方法2: Git Credential Helperを使用（推奨）

認証情報を保存して、次回から自動的に使用します。

```bash
cd /Volumes/mitomo_SSD/tabelog_checker

# Credential Helperを設定
git config --global credential.helper osxkeychain

# プッシュ（初回のみ認証情報を入力）
git push -u origin main
```

**初回の認証情報入力:**
- **Username**: `mtm112`
- **Password**: Personal Access Token

次回からは自動的に認証情報が使用されます。

## 方法3: 環境変数を使用

```bash
cd /Volumes/mitomo_SSD/tabelog_checker

# 環境変数にトークンを設定
export GIT_ASKPASS=echo
export GIT_USERNAME=mtm112
export GIT_PASSWORD=YOUR_TOKEN

# または、URLに直接埋め込む（一時的）
git remote set-url origin https://mtm112:YOUR_TOKEN@github.com/mtm112/tabelog-checker.git
git push -u origin main
```

## 最も簡単な方法

以下のコマンドを実行し、プロンプトが表示されたら認証情報を入力してください：

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git push -u origin main
```

**入力する内容:**
- **Username for 'https://github.com':** `mtm112`
- **Password for 'https://mtm112@github.com':** Personal Access Token（パスワードの代わり）
