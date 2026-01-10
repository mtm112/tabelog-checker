import streamlit as st
import pandas as pd
import time
from tabelog_checker import (
    load_urls, save_urls, check_all_urls, 
    save_results_to_csv, ensure_results_dir
)
import os
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="食べログ掲載ステータスチェッカー",
    page_icon="🍽️",
    layout="wide"
)

# タイトル
st.title("🍽️ 食べログ掲載ステータスチェッカー")
st.markdown("---")

# タブを作成
tab1, tab2, tab3 = st.tabs(["📝 URL管理", "🔍 チェック実行", "📊 過去の結果"])

# ========== タブ1: URL管理 ==========
with tab1:
    st.markdown("### 📝 登録URL管理")
    
    # Googleスプレッドシートの設定確認
    from tabelog_checker import get_google_sheets_config, get_google_sheets_client
    sheets_config = get_google_sheets_config()
    sheets_client = get_google_sheets_client()
    
    # デバッグ情報を表示
    with st.expander("🔍 デバッグ情報", expanded=False):
        st.write("**設定状態:**")
        st.write(f"- sheets_config存在: {sheets_config is not None}")
        st.write(f"- sheets_client存在: {sheets_client is not None}")
        
        if sheets_config:
            st.write("**設定内容:**")
            st.write(f"- spreadsheet_id: {sheets_config.get('spreadsheet_id', 'N/A')}")
            st.write(f"- worksheet_name: {sheets_config.get('worksheet_name', 'N/A')}")
            st.write(f"- credentials存在: {'credentials' in sheets_config}")
            if 'credentials' in sheets_config:
                creds = sheets_config.get('credentials', {})
                st.write(f"  - type: {creds.get('type', 'N/A')}")
                st.write(f"  - client_email: {creds.get('client_email', 'N/A')[:30]}...")
                st.write(f"  - project_id: {creds.get('project_id', 'N/A')}")
        
        # テスト読み込みボタン
        if st.button("🧪 スプレッドシート接続テスト", type="secondary"):
            if sheets_client:
                try:
                    config = get_google_sheets_config()
                    if config:
                        spreadsheet_id = config.get('spreadsheet_id')
                        worksheet_name = config.get('worksheet_name', 'Sheet1')
                        if spreadsheet_id:
                            spreadsheet = sheets_client.open_by_key(spreadsheet_id)
                            worksheet = spreadsheet.worksheet(worksheet_name)
                            all_values = worksheet.get_all_values()
                            st.success(f"✅ 接続成功！読み込んだ行数: {len(all_values)}行")
                            if all_values:
                                st.write("**ヘッダー行:**")
                                st.write(all_values[0])
                                if len(all_values) > 1:
                                    st.write("**最初のデータ行:**")
                                    st.write(all_values[1])
                        else:
                            st.error("❌ spreadsheet_idが設定されていません")
                    else:
                        st.error("❌ 設定が取得できませんでした")
                except Exception as e:
                    st.error(f"❌ エラー: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
            else:
                st.error("❌ クライアントが取得できませんでした")
    
    if sheets_config and sheets_client:
        col_status, col_reload = st.columns([3, 1])
        with col_status:
            st.success("✅ Googleスプレッドシートから読み込みます")
            spreadsheet_id = sheets_config.get('spreadsheet_id', 'N/A')
            worksheet_name = sheets_config.get('worksheet_name', 'Sheet1')
            st.info(f"📊 スプレッドシートID: {spreadsheet_id[:20]}... | ワークシート: {worksheet_name}")
            st.info("💡 URLは4列目（D列）から読み込みます")
        with col_reload:
            if st.button("🔄 スプレッドシートから再読み込み", type="secondary", use_container_width=True):
                # セッションステートをクリアして強制的に再読み込み
                if 'last_reload_time' in st.session_state:
                    del st.session_state['last_reload_time']
                if 'shop_names_cache' in st.session_state:
                    # キャッシュは保持（店舗名の再取得は不要なため）
                    pass
                st.success("再読み込みしました！")
                st.rerun()
    else:
        if not sheets_config:
            st.warning("⚠️ Googleスプレッドシートが設定されていません。")
            with st.expander("🔧 設定方法"):
                st.markdown("""
                Streamlit Cloudで使用する場合は、以下の手順で設定してください：
                
                1. Streamlit Cloudのアプリ設定画面で「Secrets」を開く
                2. `GOOGLE_SHEETS_SETUP.md`を参照して、以下の形式で設定を追加：
                
                ```toml
                [google_sheets]
                spreadsheet_id = "あなたのスプレッドシートID"
                worksheet_name = "Sheet1"
                
                [google_sheets.credentials]
                type = "service_account"
                project_id = "あなたのプロジェクトID"
                private_key_id = "あなたのprivate_key_id"
                private_key = "-----BEGIN PRIVATE KEY-----\\nあなたのprivate_key\\n-----END PRIVATE KEY-----\\n"
                client_email = "あなたのサービスアカウントのメールアドレス"
                client_id = "あなたのclient_id"
                auth_uri = "https://accounts.google.com/o/oauth2/auth"
                token_uri = "https://oauth2.googleapis.com/token"
                auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
                client_x509_cert_url = "あなたのclient_x509_cert_url"
                ```
                """)
        elif not sheets_client:
            st.error("❌ Googleスプレッドシートへの接続に失敗しました。認証情報を確認してください。")
        st.info("現在はローカルファイルから読み込みます。")
    
    # URLリストを読み込み（毎回最新のデータを取得）
    urls = load_urls()
    
    # 読み込み時刻を表示（デバッグ用）
    if sheets_config and sheets_client:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.caption(f"📅 最終読み込み時刻: {current_time} | 読み込んだURL数: {len(urls)}件")
    
    # URL追加セクション
    st.markdown("---")
    st.markdown("#### ➕ URL追加")
    new_url_input = st.text_area(
        "新しいURLを1行ずつ入力してください",
        height=150,
        placeholder="例:\nhttps://tabelog.com/tokyo/A1303/A130301/13269043/\nhttps://tabelog.com/tokyo/A1304/A130401/13314297/"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ URLを追加", type="primary"):
            if new_url_input.strip():
                new_urls = [url.strip() for url in new_url_input.strip().split('\n') if url.strip()]
                # 食べログのURLかチェック
                valid_urls = []
                invalid_urls = []
                for url in new_urls:
                    if 'tabelog.com' in url and url.startswith('http'):
                        if url not in urls:
                            valid_urls.append(url)
                        else:
                            st.warning(f"既に登録済み: {url}")
                    else:
                        invalid_urls.append(url)
                
                if invalid_urls:
                    st.error(f"無効なURLが{len(invalid_urls)}件あります。食べログのURLを入力してください。")
                
                if valid_urls:
                    urls.extend(valid_urls)
                    save_urls(urls)
                    # 新しく追加したURLの店舗名を取得
                    with st.spinner("店舗名を取得中..."):
                        from tabelog_checker import check_tabelog_url
                        import time
                        if 'shop_names_cache' not in st.session_state:
                            st.session_state.shop_names_cache = {}
                        for idx, url in enumerate(valid_urls):
                            result = check_tabelog_url(url)
                            shop_name = result['shop_name'] if result['shop_name'] else url
                            st.session_state.shop_names_cache[url] = shop_name
                            if idx < len(valid_urls) - 1:
                                time.sleep(0.5)  # アクセス間隔
                    st.success(f"{len(valid_urls)}件のURLを追加しました！")
                    st.rerun()
            else:
                st.error("URLを入力してください。")
    
    # URL一覧表示・削除セクション
    st.markdown("---")
    st.markdown(f"#### 📋 登録URL一覧 ({len(urls)}件)")
    
    if urls:
        # セッションステートで店舗名をキャッシュ
        if 'shop_names_cache' not in st.session_state:
            st.session_state.shop_names_cache = {}
        
        # 店舗名を取得（キャッシュがあれば使用、なければ「取得中...」を表示）
        shop_names = []
        url_display = []
        for url in urls:
            if url in st.session_state.shop_names_cache:
                shop_names.append(st.session_state.shop_names_cache[url])
            else:
                # キャッシュにない場合は「取得中...」を表示
                shop_names.append('取得中...')
            
            # URLの末尾部分を表示用に取得
            url_end = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
            url_display.append(url_end)
        
        # データフレームで表示
        df_urls = pd.DataFrame({
            '店舗名': shop_names,
            'URL': url_display,
            '削除': [False] * len(urls)
        })
        
        # 店舗名を更新するボタン
        if st.button("🔄 店舗名を更新", type="secondary"):
            with st.spinner("店舗名を取得中..."):
                from tabelog_checker import check_tabelog_url
                import time
                for idx, url in enumerate(urls):
                    if url not in st.session_state.shop_names_cache or st.session_state.shop_names_cache[url] == '取得中...':
                        result = check_tabelog_url(url)
                        shop_name = result['shop_name'] if result['shop_name'] else url
                        st.session_state.shop_names_cache[url] = shop_name
                    if idx < len(urls) - 1:
                        time.sleep(0.5)  # アクセス間隔
            st.success("店舗名を更新しました！")
            st.rerun()
        
        # チェックボックス付きで表示
        edited_df = st.data_editor(
            df_urls,
            column_config={
                "店舗名": st.column_config.TextColumn("店舗名", width="medium"),
                "URL": st.column_config.TextColumn("URL", width="medium"),
                "削除": st.column_config.CheckboxColumn("削除")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # URLのリンクを別途表示
        with st.expander("🔗 URL一覧（クリックで開く）"):
            for idx, url in enumerate(urls):
                shop_name_display = shop_names[idx] if idx < len(shop_names) else '取得中...'
                st.markdown(f"{idx + 1}. [{shop_name_display}]({url})")
        
        # 削除ボタン
        if st.button("🗑️ チェックしたURLを削除", type="secondary"):
            urls_to_keep = []
            for idx, row in edited_df.iterrows():
                if not row['削除']:
                    # 元のURLを取得（インデックスで対応）
                    original_url = urls[idx]
                    urls_to_keep.append(original_url)
            
            deleted_count = len(urls) - len(urls_to_keep)
            if deleted_count > 0:
                save_urls(urls_to_keep)
                # キャッシュからも削除
                for url in urls:
                    if url not in urls_to_keep:
                        st.session_state.shop_names_cache.pop(url, None)
                st.success(f"{deleted_count}件のURLを削除しました！")
                st.rerun()
        
        # 一括削除
        st.markdown("---")
        if st.button("⚠️ すべてのURLを削除", type="secondary"):
            save_urls([])
            # キャッシュもクリア
            st.session_state.shop_names_cache = {}
            st.success("すべてのURLを削除しました！")
            st.rerun()
    else:
        st.info("登録されているURLがありません。上記のフォームからURLを追加してください。")

# ========== タブ2: チェック実行 ==========
with tab2:
    st.markdown("### 🔍 チェック実行")
    
    # Googleスプレッドシートの設定確認
    from tabelog_checker import get_google_sheets_config, get_google_sheets_client
    sheets_config = get_google_sheets_config()
    sheets_client = get_google_sheets_client()
    
    if sheets_config and sheets_client:
        col_info, col_reload = st.columns([3, 1])
        with col_info:
            st.info("📊 GoogleスプレッドシートからURLを読み込みます（4列目からURLを取得）")
        with col_reload:
            if st.button("🔄 再読み込み", type="secondary", use_container_width=True):
                st.rerun()
    
    # URLリストを読み込み（毎回最新のデータを取得）
    urls = load_urls()
    
    if not urls:
        st.warning("⚠️ 登録されているURLがありません。")
        if sheets_config:
            st.info("Googleスプレッドシートに「番号」「店舗名」「URL」の3列でデータを入力してください。")
        else:
            st.info("「URL管理」タブからURLを追加するか、Googleスプレッドシートを設定してください。")
    else:
        st.info(f"📋 登録されているURL: {len(urls)}件")
        
        # 登録URLを表示
        with st.expander("📋 登録URL一覧を表示"):
            for idx, url in enumerate(urls, 1):
                st.markdown(f"{idx}. {url}")
        
        st.markdown("---")
        
        # チェックオプション
        col1, col2 = st.columns(2)
        with col1:
            use_registered = st.checkbox("登録済みURLを使用", value=True)
        with col2:
            delay = st.slider("アクセス間隔（秒）", 1, 5, 1)
        
        # 手動入力も可能にする
        if not use_registered:
            st.markdown("#### 手動入力")
            manual_urls_input = st.text_area(
                "チェックするURLを1行ずつ入力してください",
                height=150,
                placeholder="例:\nhttps://tabelog.com/tokyo/A1303/A130301/13269043/"
            )
            manual_urls = [url.strip() for url in manual_urls_input.strip().split('\n') if url.strip()] if manual_urls_input.strip() else []
        else:
            manual_urls = []
        
        # チェック実行
        target_urls = urls if use_registered else manual_urls
        
        if st.button("🔍 チェック開始", type="primary", use_container_width=True):
            if not target_urls:
                st.error("チェックするURLがありません。")
            else:
                st.info(f"{len(target_urls)}件のURLをチェックします...")
                
                # プログレスバー
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # チェック実行
                results = []
                for idx, url in enumerate(target_urls):
                    # プログレス更新
                    progress = (idx + 1) / len(target_urls)
                    progress_bar.progress(progress)
                    status_text.text(f"チェック中: {idx + 1}/{len(target_urls)} - {url}")
                    
                    # URLをチェック（共通モジュールを使用）
                    from tabelog_checker import check_tabelog_url
                    result = check_tabelog_url(url)
                    results.append(result)
                    
                    # アクセス間隔をあける（最後のURL以外）
                    if idx < len(target_urls) - 1:
                        time.sleep(delay)
                
                # プログレスバーを完了状態にする
                progress_bar.progress(1.0)
                status_text.text("チェック完了！")
                
                # 結果をデータフレームに変換
                df = pd.DataFrame(results)
                df = df[['shop_name', 'url', 'status', 'error']]
                df.columns = ['店舗名', 'URL', 'ステータス', 'エラー']
                
                st.markdown("---")
                st.markdown("### 📊 チェック結果")
                
                # 結果のサマリー
                total_count = len(df)
                premium_count = len(df[df['ステータス'] == '有料'])
                free_count = len(df[df['ステータス'] == '無料/要確認'])
                error_count = len(df[df['ステータス'] == 'エラー'])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("総件数", total_count)
                with col2:
                    st.metric("有料", premium_count, delta=None)
                with col3:
                    st.metric("無料/要確認", free_count, delta=None)
                with col4:
                    st.metric("エラー", error_count, delta=None)
                
                # データフレームを表示（スタイリング付き）
                def highlight_status(row):
                    """ステータスに応じて行をハイライト"""
                    if row['ステータス'] == '無料/要確認':
                        return ['background-color: #ffcccc'] * len(row)
                    elif row['ステータス'] == 'エラー':
                        return ['background-color: #ffffcc'] * len(row)
                    return [''] * len(row)
                
                styled_df = df.style.apply(highlight_status, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # 結果を保存
                ensure_results_dir()
                saved_file = save_results_to_csv(results)
                st.success(f"✅ 結果を保存しました: {saved_file}")
                
                # 無料/要確認の店舗がある場合は通知
                free_count = len([r for r in results if r['status'] == '無料/要確認'])
                if free_count > 0:
                    from notifier import notify_free_restaurants
                    notify_free_restaurants(results)
                    st.warning(f"⚠️ 無料/要確認の店舗が{free_count}件見つかりました。通知を送信しました。")
                
                # CSVダウンロードボタン
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 結果をCSVでダウンロード",
                    data=csv,
                    file_name=f"tabelog_check_result_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# ========== タブ3: 過去の結果 ==========
with tab3:
    st.markdown("### 📊 過去のチェック結果")
    
    ensure_results_dir()
    results_dir = 'results'
    
    if os.path.exists(results_dir):
        result_files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]
        result_files.sort(reverse=True)  # 新しい順
        
        if result_files:
            st.info(f"📁 保存されている結果ファイル: {len(result_files)}件")
            
            selected_file = st.selectbox(
                "表示するファイルを選択",
                result_files
            )
            
            if selected_file:
                filepath = os.path.join(results_dir, selected_file)
                df = pd.read_csv(filepath, encoding='utf-8-sig')
                
                st.markdown(f"#### 📄 {selected_file}")
                
                # サマリー
                total_count = len(df)
                premium_count = len(df[df['ステータス'] == '有料'])
                free_count = len(df[df['ステータス'] == '無料/要確認'])
                error_count = len(df[df['ステータス'] == 'エラー'])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("総件数", total_count)
                with col2:
                    st.metric("有料", premium_count)
                with col3:
                    st.metric("無料/要確認", free_count)
                with col4:
                    st.metric("エラー", error_count)
                
                # データフレーム表示
                def highlight_status(row):
                    if row['ステータス'] == '無料/要確認':
                        return ['background-color: #ffcccc'] * len(row)
                    elif row['ステータス'] == 'エラー':
                        return ['background-color: #ffffcc'] * len(row)
                    return [''] * len(row)
                
                styled_df = df.style.apply(highlight_status, axis=1)
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # ダウンロードボタン
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 CSVでダウンロード",
                    data=csv,
                    file_name=selected_file,
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("保存されている結果ファイルがありません。")
    else:
        st.info("結果ディレクトリが存在しません。")

# サイドバー
with st.sidebar:
    st.header("📋 使い方")
    st.markdown("""
    **URL管理タブ:**
    - チェックしたいURLを登録・管理
    
    **チェック実行タブ:**
    - 登録済みURLをチェック
    - 結果は自動保存されます
    
    **過去の結果タブ:**
    - 過去のチェック結果を確認
    """)
    st.markdown("---")
    st.markdown("### ⚠️ 注意事項")
    st.warning("""
    - 食べログの規約を遵守してください
    - 大量のアクセスは避けてください
    - アクセス間隔は調整可能です
    """)
    st.markdown("---")
    st.markdown("### 📅 スケジュール実行")
    st.info("""
    毎月3-10日の間、毎日自動チェックが実行されます。
    設定方法はREADMEを参照してください。
    """)

# フッター
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "食べログ掲載ステータスチェッカー v2.0 | "
    "食べログの規約を遵守してご利用ください"
    "</div>",
    unsafe_allow_html=True
)
