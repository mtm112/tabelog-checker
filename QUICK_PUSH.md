# クイックプッシュガイド

## 現在の状態

- ✅ Gitリポジトリは初期化済み
- ✅ コミットは作成済み
- ✅ リモートリポジトリは設定済み

## プッシュ方法

### 方法1: 直接プッシュ（認証情報を入力）

ターミナルで以下を実行：

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git push -u origin main
```

**認証情報の入力:**
1. **Username for 'https://github.com':** → `mtm112` と入力してEnter
2. **Password for 'https://mtm112@github.com':** → Personal Access Tokenを貼り付けてEnter

### 方法2: Credential Helperを使用（推奨）

初回のみ認証情報を入力し、次回からは自動認証されます：

```bash
# Credential Helperを設定（既に実行済み）
git config --global credential.helper osxkeychain

# プッシュ（初回のみ認証情報を入力）
git push -u origin main
```

### 方法3: URLにトークンを埋め込む（一時的）

```bash
# トークンをURLに埋め込む（YOUR_TOKENを実際のトークンに置き換え）
git remote set-url origin https://mtm112:YOUR_TOKEN@github.com/mtm112/tabelog-checker.git

# プッシュ
git push -u origin main

# プッシュ後、URLを元に戻す（セキュリティのため）
git remote set-url origin https://github.com/mtm112/tabelog-checker.git
```

## 認証情報が保存されている場合

既に認証情報が保存されている場合は、そのままプッシュできます：

```bash
git push -u origin main
```

## トラブルシューティング

### 認証エラーが出る場合

1. Personal Access Tokenが正しいか確認
2. トークンに`repo`権限があるか確認
3. リポジトリが存在するか確認

### 認証情報をクリアして再入力

```bash
# 保存された認証情報をクリア
git credential-osxkeychain erase
host=github.com
protocol=https

# 再度プッシュ（認証情報を再入力）
git push -u origin main
```
