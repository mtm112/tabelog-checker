# Personal Access Token作成手順（ステップバイステップ）

## ステップ1: GitHubにログイン

1. [GitHub](https://github.com)にアクセス
2. 右上のプロフィールアイコンをクリック
3. 「Settings」を選択

## ステップ2: Developer settingsに移動

1. 左メニューの一番下にある「Developer settings」をクリック
2. 左メニューから「Personal access tokens」を選択
3. 「Tokens (classic)」をクリック

## ステップ3: 新しいトークンを作成

1. 「Generate new token」ボタンをクリック
2. 「Generate new token (classic)」を選択

## ステップ4: トークンの設定

### Note（トークン名）
- 任意の名前を入力（例：`tabelog-checker`、`tabelog-checker-v2`）
- 複数のトークンを使い分ける場合に識別しやすい名前を付ける

### Expiration（有効期限）
- ドロップダウンから選択：
  - `90 days`（90日）
  - `No expiration`（無期限）← **個人利用の場合はこちらを推奨**
  - その他の期間

### Repository access（リポジトリアクセス）
**重要**: 「All repositories」を選択してください

- ❌ Public repositories（公開リポジトリのみ、プライベートリポジトリにアクセス不可）
- ✅ **All repositories**（すべてのリポジトリ、プライベートリポジトリも含む）← **これを選択**
- ❌ Only select repositories（特定のリポジトリのみ）

### Permissions（権限）
「Account」セクションで「+ Add permissions」をクリック

**Repository permissions** セクションで以下を選択：
- ✅ **repo**（すべてのチェックボックスにチェック）
  - ✅ repo:status
  - ✅ repo_deployment
  - ✅ public_repo
  - ✅ repo:invite
  - ✅ security_events

**重要**: `repo`のチェックボックスを選択すると、すべてのサブ項目が自動的に選択されます。

## ステップ5: トークンを生成

1. 画面下部の「Generate token」ボタンをクリック
2. **重要**: 表示されたトークンをすぐにコピーしてください
   - 例：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - この画面を閉じると、もう一度表示されません
3. トークンを安全な場所に保存（メモ帳など）

## ステップ6: トークンを使用してプッシュ

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git push -u origin main
```

**認証情報の入力:**
- **Username**: `mtm112`
- **Password**: コピーしたPersonal Access Token（パスワードの代わりに入力）

## 注意事項

### セキュリティ
- トークンはパスワードと同じように扱ってください
- 他人に共有しないでください
- 不要になったトークンは削除してください

### トークンの管理
- 複数のトークンを作成できます
- 古いトークンは削除して、新しいトークンを使用することを推奨
- トークン一覧から、作成日時や有効期限を確認できます

### トークンを忘れた場合
- トークンは再表示できません
- 新しいトークンを作成する必要があります
- 古いトークンは無効化できます（トークン一覧から削除）

## トラブルシューティング

### トークンが表示されない
- ページをリロードしてみてください
- ブラウザのポップアップブロッカーを確認してください

### トークンがすぐに消えた
- トークンは一度しか表示されません
- 新しいトークンを作成してください

### 権限エラーが出る
- `repo`権限が正しく設定されているか確認
- 「All repositories」を選択しているか確認
