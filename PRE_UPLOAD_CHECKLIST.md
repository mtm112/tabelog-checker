# GitHubアップロード前チェックリスト

## ✅ アップロード前に確認すべき項目

### 1. 機密情報の確認

以下のファイルに機密情報が含まれていないか確認：

- [x] `notifier.py` - 機密情報を削除済み（Streamlit Secretsから読み込む）
- [x] `test_line_messaging.py` - 削除済み
- [ ] `urls.json` - `.gitignore`で除外されているか確認
- [ ] Googleサービスアカウントキー（`*-*.json`）が存在しないか確認

### 2. 除外されるファイル・フォルダ

`.gitignore`により以下のファイル・フォルダは自動的に除外されます：

- ✅ `venv/` - 仮想環境（除外）
- ✅ `__pycache__/` - Pythonキャッシュ（除外）
- ✅ `urls.json` - 登録URL（除外）
- ✅ `results/` - チェック結果（除外）
- ✅ `logs/` - ログファイル（除外）
- ✅ `*.csv` - CSVファイル（除外）
- ✅ `*.log` - ログファイル（除外）
- ✅ `.DS_Store` - macOSシステムファイル（除外）

### 3. アップロードされるファイル

以下のファイルがアップロードされます：

#### 必須ファイル
- ✅ `app.py` - メインアプリ
- ✅ `tabelog_checker.py` - 共通モジュール
- ✅ `notifier.py` - 通知機能
- ✅ `check_scheduled.py` - スケジュール実行用
- ✅ `requirements.txt` - 依存パッケージ
- ✅ `README.md` - 説明書
- ✅ `.gitignore` - Git除外設定
- ✅ `.streamlit/config.toml` - Streamlit設定（存在する場合）

#### ドキュメント
- ✅ `GITHUB_DEPLOY.md` - デプロイ手順
- ✅ `GOOGLE_SHEETS_SETUP.md` - Googleスプレッドシート設定
- ✅ `README_STREAMLIT_CLOUD.md` - Streamlit Cloud手順
- ✅ `SECURITY.md` - セキュリティ注意事項

#### ローカル用ファイル（アップロードしても問題なし）
- ✅ `run.sh` - ローカル起動スクリプト
- ✅ `setup_schedule.sh` - スケジュール設定（macOS用）
- ✅ `remove_schedule.sh` - スケジュール削除（macOS用）
- ✅ `com.tabelog.checker.plist` - launchd設定（macOS用）

**注意**: ローカル用ファイルはStreamlit Cloudでは使用されませんが、残しておいても問題ありません。

## 🚨 アップロード前に必ず確認

### 機密情報チェック

```bash
# 機密情報が含まれていないか確認
grep -r "92UbKB2XYFR0OnKneOJzznIXwm9XcKXk" . --exclude-dir=venv --exclude-dir=.git
grep -r "U91213832394f27472183239eb2441542" . --exclude-dir=venv --exclude-dir=.git
```

上記コマンドで何も表示されなければ安全です。

### Git除外確認

```bash
# 除外されるファイルを確認
git status --ignored
```

`venv/`、`urls.json`、`results/`などが表示されれば正しく除外されています。

## 📝 アップロード手順

1. **プライベートリポジトリを作成**（重要！）
2. 以下のコマンドでアップロード：

```bash
cd /Volumes/mitomo_SSD/tabelog_checker
git init
git add .
git commit -m "Initial commit: 食べログチェッカーアプリ"
git remote add origin https://github.com/あなたのユーザー名/tabelog-checker.git
git branch -M main
git push -u origin main
```

## ⚠️ 注意事項

- **必ずプライベートリポジトリを使用してください**
- 機密情報はStreamlit CloudのSecretsで管理してください
- `urls.json`はローカルにのみ存在し、GitHubにはアップロードされません
