# GitHub Actions によるクラウド自動実行

PCがシャットダウンしていても、GitHub Actions が毎日自動でチェックを実行します。

## 仕組み

```
GitHub Actions（クラウド）
  ↓ 毎日 9:00 JST
check_scheduled.py を実行
  ↓ 毎月3〜10日のみ実際にチェック
GoogleスプレッドシートからURL読込
  ↓
食べログをチェック
  ↓
無料/要確認があれば LINE / メール通知
```

- **Streamlit Cloud**: 手動チェック用のWeb UI（そのまま利用可能）
- **GitHub Actions**: 自動チェック用（PC不要）

## セットアップ手順

### 1. GitHub Secrets を登録

リポジトリ `https://github.com/mtm112/tabelog-checker` で:

1. **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** で以下を追加

#### 必須（Googleスプレッドシート）

| Secret名 | 値 |
|----------|-----|
| `GOOGLE_SHEETS_SPREADSHEET_ID` | スプレッドシートID |
| `GOOGLE_SHEETS_WORKSHEET_NAME` | ワークシート名（例: `Sheet1`） |
| `GOOGLE_SHEETS_CREDENTIALS_JSON` | サービスアカウントJSONの**全文**（1行で貼り付け） |

`GOOGLE_SHEETS_CREDENTIALS_JSON` の取得方法:
- GCPでダウンロードしたJSONファイルをテキストエディタで開く
- 中身をすべてコピーしてSecretに貼り付け

#### 通知（LINE を使う場合）

| Secret名 | 値 |
|----------|-----|
| `LINE_MESSAGING_ENABLED` | `true` |
| `LINE_MESSAGING_CHANNEL_ACCESS_TOKEN` | チャネルアクセストークン |
| `LINE_MESSAGING_USER_ID` | ユーザーID |

#### 通知（メールを使う場合）

| Secret名 | 値 |
|----------|-----|
| `EMAIL_ENABLED` | `true` |
| `EMAIL_TO` | 送信先メールアドレス |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | Gmailアドレス |
| `SMTP_PASSWORD` | アプリパスワード |

### 2. コードを GitHub にプッシュ

```bash
git add .
git commit -m "GitHub Actions によるクラウド自動実行を追加"
git push origin main
```

### 3. 動作確認

1. GitHub リポジトリの **Actions** タブを開く
2. 左メニューから「食べログ自動チェック」を選択
3. **Run workflow** → **Run workflow** で手動実行
4. 実行ログで結果を確認

毎月3〜10日以外に手動実行した場合、「スケジュール実行は毎月3-10日の間のみ」と表示されて正常終了します。

### 4. 結果CSVの確認

チェック実行後、Actions の実行詳細 → **Artifacts** から CSV をダウンロードできます（90日間保存）。

## 注意事項

- GitHub Actions の cron は **UTC基準** です（ワークフロー内で JST 9:00 = UTC 0:00 に設定済み）
- 無料プランでも public リポジトリなら問題なく動作します
- private リポジトリは月2,000分まで無料
- スケジュール実行は最大15分程度遅れることがあります
- 60日間リポジトリにアクティビティがないとスケジュールが停止する場合があります

## ローカル launchd との関係

| 方式 | PC必要 | 用途 |
|------|--------|------|
| GitHub Actions | 不要 | **自動チェック（推奨）** |
| launchd（Mac） | 必要 | ローカル実行（不要なら停止可） |

ローカルスケジュールを停止する場合:

```bash
./remove_schedule.sh
```
