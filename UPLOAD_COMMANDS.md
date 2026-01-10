# GitHubアップロード用コマンド

## 方法1: スクリプトを使用（簡単）

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
./upload_to_github.sh
```

スクリプトが対話形式で案内します。

## 方法2: 手動でコマンドを実行

### ステップ1: Gitリポジトリの初期化（初回のみ）

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git init
```

### ステップ2: ファイルを追加

```bash
git add .
```

### ステップ3: コミット

```bash
git commit -m "Initial commit: 食べログチェッカーアプリ"
```

### ステップ4: リモートリポジトリを追加（初回のみ）

```bash
git remote add origin https://github.com/あなたのユーザー名/tabelog-checker.git
```

**注意**: `あなたのユーザー名`と`tabelog-checker`を実際の値に置き換えてください。

### ステップ5: ブランチ名を設定

```bash
git branch -M main
```

### ステップ6: GitHubにプッシュ

```bash
git push -u origin main
```

**認証情報の入力:**
- **Username**: あなたのGitHubユーザー名（例：`mtm112`）
- **Password**: Personal Access Token（パスワードの代わりに入力）

## リポジトリが既に存在する場合

既にリモートリポジトリが設定されている場合：

```bash
git push -u origin main
```

## トラブルシューティング

### エラー: "remote origin already exists"

既にリモートリポジトリが設定されている場合：

```bash
# 既存の設定を確認
git remote -v

# 必要に応じて削除して再設定
git remote remove origin
git remote add origin https://github.com/あなたのユーザー名/tabelog-checker.git
```

### エラー: "Permission denied"

- Personal Access Tokenが正しいか確認
- トークンに`repo`権限があるか確認
- リポジトリへのアクセス権限があるか確認

### エラー: "Repository not found"

- リポジトリがGitHub上で作成されているか確認
- リポジトリURLが正しいか確認
- プライベートリポジトリの場合、トークンに適切な権限があるか確認
