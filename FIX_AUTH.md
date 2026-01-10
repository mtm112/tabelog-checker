# 認証エラー解決方法

「Invalid username or token」エラーが発生した場合の対処法です。

## 解決手順

### ステップ1: リモートURLを確認・修正

```bash
cd /Volumes/mitomo_SSD/tabelog_checker

# 現在のリモートURLを確認
git remote -v

# 通常の形式に戻す（既に実行済み）
git remote set-url origin https://github.com/mtm112/tabelog-checker.git
```

### ステップ2: 保存された認証情報をクリア

```bash
# macOSのキーチェーンから認証情報を削除
git credential-osxkeychain erase
host=github.com
protocol=https
# （Ctrl+Dで終了）
```

または、キーチェーンアクセスアプリから手動で削除：
1. 「キーチェーンアクセス」アプリを開く
2. 「github.com」を検索
3. 該当する項目を削除

### ステップ3: Personal Access Tokenを再確認

1. [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. 作成したトークンを確認
3. トークンが有効期限内か確認
4. トークンに`repo`権限があるか確認

### ステップ4: 再度プッシュ

```bash
git push -u origin main
```

**認証情報の入力:**
- **Username**: `mtm112`
- **Password**: Personal Access Token（パスワードの代わり）

## トークンが正しくない場合

新しいトークンを作成：

1. [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. 「Generate new token (classic)」をクリック
3. 設定：
   - **Note**: `tabelog-checker-v2`
   - **Expiration**: お好みの期間
   - **Repository access**: 「All repositories」を選択
   - **Permissions**: `repo`にチェック（すべてのチェックボックス）
4. 「Generate token」をクリック
5. 新しいトークンをコピー
6. 再度`git push`を実行

## 代替方法：SSH認証を使用

Personal Access Tokenでうまくいかない場合、SSH認証を使用することもできます。

### SSH鍵の設定

```bash
# SSH鍵を生成（まだ持っていない場合）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 公開鍵を表示
cat ~/.ssh/id_ed25519.pub
```

1. 表示された公開鍵をコピー
2. [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys)にアクセス
3. 「New SSH key」をクリック
4. 公開鍵を貼り付けて保存

### リモートURLをSSHに変更

```bash
git remote set-url origin git@github.com:mtm112/tabelog-checker.git
git push -u origin main
```

SSH認証の場合は、認証情報の入力は不要です。
