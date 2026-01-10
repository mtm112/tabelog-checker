# Googleスプレッドシート連携設定ガイド

このアプリをGoogleスプレッドシートと連携させるための設定手順です。

## ステップ1: Google Cloud Platform (GCP) でプロジェクトを作成

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクト選択ドロップダウンから「新しいプロジェクト」をクリック
3. プロジェクト名を入力（例：`tabelog-checker`）
4. 「作成」をクリック
5. 作成したプロジェクトを選択

## ステップ2: Google Sheets API を有効化

1. Google Cloud Consoleの左メニューから「APIとサービス」→「ライブラリ」を選択
2. 検索バーに「Google Sheets API」と入力
3. 「Google Sheets API」を選択
4. 「有効にする」をクリック

## ステップ3: Google Drive API を有効化

1. 同じく「APIとサービス」→「ライブラリ」を選択
2. 検索バーに「Google Drive API」と入力
3. 「Google Drive API」を選択
4. 「有効にする」をクリック

## ステップ4: サービスアカウントを作成

1. Google Cloud Consoleの左メニューから「APIとサービス」→「認証情報」を選択
2. 「認証情報を作成」→「サービスアカウント」を選択
3. サービスアカウント名を入力（例：`tabelog-checker-service`）
4. 「作成して続行」をクリック
5. ロールは「編集者」を選択（または必要に応じて「オーナー」）
6. 「続行」をクリック
7. 「完了」をクリック

## ステップ5: サービスアカウントキーをダウンロード

1. 作成したサービスアカウントをクリック
2. 「キー」タブを選択
3. 「キーを追加」→「新しいキーを作成」を選択
4. キーのタイプで「JSON」を選択
5. 「作成」をクリック
6. JSONファイルがダウンロードされます（例：`tabelog-checker-xxxxx.json`）
7. **重要**: このJSONファイルは安全に保管してください。他人に共有しないでください。

## ステップ6: Googleスプレッドシートを作成

1. [Googleスプレッドシート](https://sheets.google.com/)にアクセス
2. 新しいスプレッドシートを作成
3. スプレッドシート名を設定（例：`食べログチェッカー URL管理`）
4. 1行目にヘッダーを設定：
   - A1: `番号`（または任意の列名）
   - B1: `店舗名`
   - C1: 任意の列（使用しない列でも可）
   - D1: `URL`（重要：4列目（D列）にURLを配置してください）
5. 2行目以降にデータを入力：
   - 例：
     ```
     番号 | 店舗名 | その他 | URL
     1    | 店舗A | メモ   | https://tabelog.com/tokyo/A1303/A130301/13269043/
     2    | 店舗B | メモ   | https://tabelog.com/tokyo/A1304/A130401/13314297/
     ```
6. スプレッドシートのURLからスプレッドシートIDを取得：
   - URL例: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`
   - スプレッドシートID: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`（`/d/`と`/edit`の間の部分）

**重要**: 
- 「URL」列は4列目（D列）に配置してください
- 列名は「URL」または「URLs」を推奨しますが、自動検出も可能です
- URL列が見つからない場合、4列目（D列、インデックス3）を自動的に使用します
- 食べログのURL（`tabelog.com`を含む）のみが読み込まれます

## ステップ7: サービスアカウントにスプレッドシートへのアクセス権限を付与

1. 作成したスプレッドシートを開く
2. 右上の「共有」ボタンをクリック
3. ダウンロードしたJSONファイルを開き、`client_email`の値をコピー（例：`tabelog-checker-service@your-project.iam.gserviceaccount.com`）
4. 共有ダイアログにサービスアカウントのメールアドレスを貼り付け
5. 権限を「編集者」に設定
6. 「送信」をクリック（通知は送信しなくてOK）

## ステップ8: Streamlit Cloud に認証情報を設定

1. Streamlit Cloudのアプリ設定画面で「Secrets」を開く
2. 以下の形式で設定を追加：

```toml
[google_sheets]
spreadsheet_id = "あなたのスプレッドシートID"
worksheet_name = "Sheet1"

[google_sheets.credentials]
type = "service_account"
project_id = "あなたのプロジェクトID"
private_key_id = "あなたのprivate_key_id"
private_key = "-----BEGIN PRIVATE KEY-----\nあなたのprivate_key\n-----END PRIVATE KEY-----\n"
client_email = "あなたのサービスアカウントのメールアドレス"
client_id = "あなたのclient_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "あなたのclient_x509_cert_url"
```

### 認証情報の取得方法

ダウンロードしたJSONファイルを開き、以下の値をコピーして上記の形式に当てはめてください：

- `spreadsheet_id`: ステップ6で取得したスプレッドシートID
- `worksheet_name`: ワークシート名（デフォルトは`URLs`、最初のシートを使用する場合は`Sheet1`など）
- `project_id`: JSONファイルの`project_id`
- `private_key_id`: JSONファイルの`private_key_id`
- `private_key`: JSONファイルの`private_key`（改行を含む場合は`\n`で表現）
- `client_email`: JSONファイルの`client_email`
- `client_id`: JSONファイルの`client_id`
- `auth_uri`: JSONファイルの`auth_uri`
- `token_uri`: JSONファイルの`token_uri`
- `auth_provider_x509_cert_url`: JSONファイルの`auth_provider_x509_cert_url`
- `client_x509_cert_url`: JSONファイルの`client_x509_cert_url`

### 設定例

JSONファイルの内容例：
```json
{
  "type": "service_account",
  "project_id": "tabelog-checker-123456",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
  "client_email": "tabelog-checker-service@tabelog-checker-123456.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tabelog-checker-service%40tabelog-checker-123456.iam.gserviceaccount.com"
}
```

Streamlit Secretsの設定例：
```toml
[google_sheets]
spreadsheet_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
worksheet_name = "URLs"

[google_sheets.credentials]
type = "service_account"
project_id = "tabelog-checker-123456"
private_key_id = "abc123..."
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
client_email = "tabelog-checker-service@tabelog-checker-123456.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/tabelog-checker-service%40tabelog-checker-123456.iam.gserviceaccount.com"
```

## ステップ9: 動作確認

1. Streamlit Cloudでアプリを再デプロイ
2. アプリでURLを追加
3. Googleスプレッドシートを確認し、URLが追加されていることを確認

## トラブルシューティング

### エラー: "The caller does not have permission"

- サービスアカウントにスプレッドシートへのアクセス権限が付与されているか確認
- スプレッドシートの共有設定でサービスアカウントのメールアドレスが追加されているか確認

### エラー: "Spreadsheet not found"

- `spreadsheet_id`が正しいか確認
- スプレッドシートIDはURLの`/d/`と`/edit`の間の部分です

### エラー: "Worksheet not found"

- `worksheet_name`が正しいか確認
- ワークシート名は大文字小文字を区別します
- デフォルトのワークシート名は`Sheet1`です

### 認証エラー

- JSONファイルの内容が正しくStreamlit Secretsに設定されているか確認
- `private_key`の改行が`\n`で正しく表現されているか確認

## セキュリティに関する注意事項

- サービスアカウントキー（JSONファイル）は絶対に公開リポジトリにコミットしないでください
- Streamlit Secretsは暗号化されて保存されますが、適切に管理してください
- 不要になったサービスアカウントキーは削除してください
