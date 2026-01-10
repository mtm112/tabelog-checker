# 食べログ掲載ステータスチェッカー

食べログの店舗ページが有料プランか無料プランかを自動でチェックするStreamlitアプリケーションです。

## 機能

- **URL管理機能**: チェックしたい食べログURLを事前に登録・管理
- **一括チェック**: 複数の食べログURLを一括でチェック
- **有料/無料プランの自動判定**: HTMLの要素を解析して自動判定
- **結果表示**: 表形式で表示（無料/要確認は赤色でハイライト）
- **結果保存**: チェック結果をCSV形式で自動保存
- **過去の結果確認**: 過去のチェック結果を確認可能
- **通知機能**: 無料/要確認の店舗が見つかった場合にLINEまたはメールで通知
  - LINE Messaging API
  - メール通知（SMTP）
- **スケジュール実行**: 毎月3-10日の間、毎日自動チェック（macOSのlaunchd使用）
- **エラーハンドリング**: 404エラー、接続エラーなどに対応

## インストール

1. リポジトリをクローンまたはダウンロードします。

2. 仮想環境を作成します（推奨）：

```bash
python3 -m venv venv
```

3. 仮想環境をアクティベートします：

```bash
# macOS/Linuxの場合
source venv/bin/activate

# Windowsの場合
venv\Scripts\activate
```

4. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

## 使い方

### Streamlitアプリの起動

1. 仮想環境をアクティベートします（まだの場合）：

```bash
source venv/bin/activate
```

2. アプリを起動します：

```bash
streamlit run app.py
```

または、起動スクリプトを使用：

```bash
./run.sh
```

3. ブラウザが自動的に開きます（開かない場合は、表示されたURLにアクセスしてください）。

### URL管理とチェック

アプリには3つのタブがあります：

1. **URL管理タブ**: 
   - チェックしたい食べログURLを登録・管理
   - URLの追加・削除が可能

2. **チェック実行タブ**:
   - 登録済みURLを一括チェック
   - 結果は自動的に`results/`ディレクトリに保存されます

3. **過去の結果タブ**:
   - 過去のチェック結果を確認・ダウンロード

4. **通知設定タブ**:
   - LINE Messaging APIまたはメール通知の設定
   - 無料/要確認の店舗が見つかった場合に自動通知

### スケジュール実行の設定（macOS）

毎月3-10日の間、毎日自動でチェックを実行するように設定できます。

1. **スケジュールを設定**:

```bash
./setup_schedule.sh
```

これにより、毎日9:00に自動実行が設定されます（実際のチェックは毎月3-10日の間のみ実行されます）。

2. **スケジュールの確認**:

```bash
launchctl list | grep com.tabelog.checker
```

3. **スケジュールの停止**:

```bash
./remove_schedule.sh
```

4. **手動でチェックを実行**:

```bash
source venv/bin/activate
python check_scheduled.py
```

### 実行時間の変更

実行時間を変更したい場合は、`com.tabelog.checker.plist`ファイルを編集してください：

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>  <!-- 時間（0-23） -->
    <key>Minute</key>
    <integer>0</integer>   <!-- 分（0-59） -->
</dict>
```

編集後、以下のコマンドで再読み込み：

```bash
./remove_schedule.sh
./setup_schedule.sh
```

### 通知設定

無料/要確認の店舗が見つかった場合に、LINEまたはメールで通知を受け取れます。

#### LINE Messaging API（推奨）

⚠️ **重要**: LINE Notifyは2025年3月31日にサービス終了予定です。LINE Messaging APIへの移行を推奨します。

1. [LINE Developers Console](https://developers.line.biz/console/)にアクセス
2. プロバイダーを作成（初回のみ）
3. Messaging APIチャネルを作成
4. チャネルアクセストークンを取得
5. 友だち追加用のQRコードを表示し、自分のLINEアカウントで友だち追加
6. ユーザーIDを取得（Webhookイベントで取得するか、[LINE公式アカウントマネージャー](https://manager.line.biz/)で確認）
7. アプリの「通知設定」タブで設定を入力

#### メール通知

Gmailを使用する場合：

1. Googleアカウントの設定→セキュリティ
2. 2段階認証を有効にする
3. 「アプリパスワード」を生成
4. アプリの「通知設定」タブでSMTP設定を入力

## 判定ロジック

以下の要素の有無で有料/無料を判定しています：

- `id="js-rst-calendar-target"`（予約カレンダー）
- `class="pr-comment-title"`（PR文）

どちらかが存在すれば「有料」、どちらも存在しなければ「無料/要確認」と判定します。

## ファイル構成

```
tabelog_checker/
├── app.py                    # Streamlitアプリ（メイン）
├── tabelog_checker.py        # 共通チェック機能モジュール
├── check_scheduled.py         # スケジュール実行用スクリプト
├── notifier.py                 # 通知機能モジュール
├── com.tabelog.checker.plist # launchd設定ファイル
├── setup_schedule.sh         # スケジュール設定スクリプト
├── remove_schedule.sh        # スケジュール削除スクリプト
├── run.sh                    # アプリ起動スクリプト
├── requirements.txt          # 依存パッケージ
├── urls.json                 # 登録URLリスト（自動生成）
├── notification_config.json   # 通知設定（自動生成）
├── results/                  # チェック結果保存ディレクトリ（自動生成）
└── logs/                     # ログファイル保存ディレクトリ（自動生成）
```

## 注意事項

- 食べログの利用規約を遵守してください
- 大量のアクセスは避けてください
- アクセス間隔は1秒に設定されています（サーバー負荷軽減のため）
- スケジュール実行は毎月3-10日の間のみ実際にチェックを実行します
- このツールは業務効率化のための補助ツールとして使用してください

## ライセンス

このプロジェクトは個人利用・業務利用を目的としています。
