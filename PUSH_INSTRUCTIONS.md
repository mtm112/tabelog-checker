# git push実行時の認証情報入力方法

## 現在の状態

`git push -u origin main`を実行すると、認証情報の入力待ちになっています。

## 認証情報の入力方法

ターミナルに以下のようなプロンプトが表示されているはずです：

```
Username for 'https://github.com': 
```

または

```
Password for 'https://mtm112@github.com': 
```

## 入力手順

### ステップ1: Usernameを入力

プロンプトが表示されたら：

1. **Username for 'https://github.com':** と表示されたら
2. `mtm112` と入力
3. **Enterキー**を押す

### ステップ2: Password（トークン）を入力

次に：

1. **Password for 'https://mtm112@github.com':** と表示されたら
2. **Personal Access Token**を貼り付け
   - パスワードではなく、作成したトークンを入力
   - 例：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
3. **Enterキー**を押す

### 注意事項

- パスワード欄には、GitHubのパスワードではなく、**Personal Access Token**を入力してください
- トークンは画面に表示されませんが、入力は反映されています
- トークンをコピーして貼り付けるのが確実です

## プロンプトが表示されない場合

### 方法1: 新しいターミナルで実行

現在のターミナルを中断（Ctrl+C）して、新しいターミナルで実行：

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git push -u origin main
```

### 方法2: 認証情報をクリアして再試行

```bash
# 保存された認証情報をクリア
git credential-osxkeychain erase
host=github.com
protocol=https
# （Ctrl+Dで終了）

# 再度プッシュ
git push -u origin main
```

### 方法3: URLにトークンを直接埋め込む（一時的）

```bash
# トークンをURLに埋め込む（YOUR_TOKENを実際のトークンに置き換え）
git remote set-url origin https://mtm112:YOUR_TOKEN@github.com/mtm112/tabelog-checker.git

# プッシュ
git push -u origin main

# プッシュ後、URLを元に戻す（セキュリティのため）
git remote set-url origin https://github.com/mtm112/tabelog-checker.git
```

## 確認方法

プッシュが成功すると、以下のようなメッセージが表示されます：

```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), done.
To https://github.com/mtm112/tabelog-checker.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```
