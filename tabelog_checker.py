"""
食べログチェック機能の共通モジュール
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import os
from datetime import datetime

# Googleスプレッドシート連携（オプション）
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

# User-Agent設定（一般的なブラウザを偽装）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# URLリストファイルのパス（ローカル環境用のフォールバック）
URLS_FILE = 'urls.json'
RESULTS_DIR = 'results'

# Googleスプレッドシート設定（Streamlit Secretsから取得）
def get_google_sheets_config():
    """
    Streamlit SecretsからGoogleスプレッドシートの設定を取得
    
    Returns:
        dict: 設定情報（設定がない場合はNone）
    """
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            if 'google_sheets' in st.secrets:
                config = st.secrets['google_sheets']
                # 必須項目のチェック
                if 'spreadsheet_id' in config and config['spreadsheet_id']:
                    return config
                else:
                    print("⚠️  Googleスプレッドシート設定にspreadsheet_idがありません")
            else:
                print("⚠️  Streamlit Secretsに'google_sheets'セクションがありません")
        else:
            print("⚠️  Streamlit Secretsが利用できません")
    except Exception as e:
        print(f"⚠️  Googleスプレッドシート設定の取得エラー: {e}")
        import traceback
        traceback.print_exc()
    return None

def get_google_sheets_client():
    """
    Googleスプレッドシートのクライアントを取得
    
    Returns:
        gspread.Client: クライアントオブジェクト（取得できない場合はNone）
    """
    if not GSPREAD_AVAILABLE:
        print("⚠️  gspreadライブラリがインストールされていません")
        return None
    
    config = get_google_sheets_config()
    if not config:
        return None
    
    try:
        # 認証情報を取得
        creds_dict = config.get('credentials')
        if not creds_dict:
            print("⚠️  Googleスプレッドシート設定に'credentials'がありません")
            return None
        
        # 認証情報からクライアントを作成
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        print("✅ Googleスプレッドシートクライアントの認証に成功しました")
        return client
    except Exception as e:
        print(f"❌ Googleスプレッドシート認証エラー: {e}")
        import traceback
        traceback.print_exc()
        return None

def load_urls(force_refresh=False):
    """
    保存されたURLリストを読み込む
    Googleスプレッドシートが設定されている場合はそちらから、なければローカルJSONファイルから読み込む
    
    Args:
        force_refresh: Trueの場合、強制的にスプレッドシートから再読み込み（デフォルト: False）
    
    Returns:
        list: URLのリスト
    """
    # Googleスプレッドシートから読み込みを試みる
    # force_refreshがTrueの場合、クライアントを再取得して最新データを取得
    client = get_google_sheets_client()
    if client:
        try:
            config = get_google_sheets_config()
            if not config:
                print("⚠️  load_urls: 設定が取得できませんでした")
                # フォールバックに進む
            else:
                spreadsheet_id = config.get('spreadsheet_id')
                worksheet_name = config.get('worksheet_name', 'Sheet1')
                
                if not spreadsheet_id:
                    print("⚠️  load_urls: spreadsheet_idが設定されていません")
                    # フォールバックに進む
                else:
                    print(f"ℹ️  load_urls: スプレッドシートから読み込み開始 (ID: {spreadsheet_id[:20]}..., ワークシート: {worksheet_name})")
                    spreadsheet = client.open_by_key(spreadsheet_id)
                    worksheet = spreadsheet.worksheet(worksheet_name)
                    
                    # データを取得（ヘッダー行を含む）
                    # 最新のデータを確実に取得するため、毎回スプレッドシートから直接読み込む
                    all_values = worksheet.get_all_values()
                    
                    # デバッグ用：読み込み時刻を記録
                    import datetime
                    print(f"📅 スプレッドシート読み込み時刻: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"ℹ️  読み込んだ行数: {len(all_values)}行")
                    
                    if not all_values:
                        print("⚠️  Googleスプレッドシートが空です")
                        return []
                    
                    # ヘッダー行を取得
                    headers = [h.strip() for h in all_values[0]]
                    print(f"ℹ️  ヘッダー行: {headers}")
                    
                    # URL列のインデックスを探す（大文字小文字を区別しない）
                    url_col_idx = None
                    for idx, header in enumerate(headers):
                        header_upper = header.upper()
                        if header_upper == 'URL' or header_upper == 'URLS' or 'URL' in header_upper:
                            url_col_idx = idx
                            print(f"✅ URL列を検出: 列{idx + 1} ({header})")
                            break
                    
                    if url_col_idx is None:
                        # URL列が見つからない場合、4列目（インデックス3）を試す
                        # 構造: 番号、店舗名、その他、URL の場合
                        if len(headers) >= 4:
                            url_col_idx = 3  # 4列目（0-indexedなので3）
                            print(f"ℹ️  URL列が見つからないため、4列目（インデックス{url_col_idx}）を使用します")
                        else:
                            # それでも見つからない場合、tabelog.comを含む列を探す
                            print(f"ℹ️  データからURL列を検索中...")
                            for row_idx, row in enumerate(all_values[1:6]):  # 最初の5行をチェック
                                for col_idx, cell in enumerate(row):
                                    if 'tabelog.com' in cell:
                                        url_col_idx = col_idx
                                        print(f"✅ データからURL列を検出: 列{col_idx + 1} (行{row_idx + 2})")
                                        break
                                if url_col_idx is not None:
                                    break
                    
                    if url_col_idx is None:
                        print("❌ GoogleスプレッドシートでURL列が見つかりません")
                        print(f"   見つかった列: {headers}")
                        print(f"   列数: {len(headers)}")
                        return []
                    
                    # データ行からURLを抽出（ヘッダー行を除く）
                    urls = []
                    for row_idx, row in enumerate(all_values[1:], start=2):  # ヘッダー行をスキップ、行番号は2から
                        if len(row) > url_col_idx:
                            url = row[url_col_idx].strip()
                            # 食べログのURLかチェック
                            if url and 'tabelog.com' in url and url.startswith('http'):
                                urls.append(url)
                                print(f"  ✅ 行{row_idx}: URLを追加: {url[:50]}...")
                            elif url and url.startswith('http'):
                                # tabelog.comが含まれていない場合も警告
                                print(f"⚠️  行{row_idx}: tabelog.comが含まれていないURLをスキップ: {url[:50]}...")
                            elif url:
                                print(f"ℹ️  行{row_idx}: 空でないセルがありますが、URLではありません: {url[:30]}...")
                    
                    if urls:
                        print(f"✅ Googleスプレッドシートから{len(urls)}件のURLを読み込みました（列: {headers[url_col_idx] if url_col_idx < len(headers) else 'N/A'}）")
                    else:
                        print("⚠️  GoogleスプレッドシートからURLが見つかりませんでした")
                        print(f"   データ行数: {len(all_values) - 1}行（ヘッダー除く）")
                    return urls
        except Exception as e:
            print(f"❌ Googleスプレッドシートからの読み込みエラー: {e}")
            import traceback
            traceback.print_exc()
            # エラーが発生した場合はローカルファイルにフォールバック
    
    # ローカルJSONファイルから読み込み（フォールバック）
    if os.path.exists(URLS_FILE):
        try:
            with open(URLS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                urls = data.get('urls', [])
                if urls:
                    print(f"✅ ローカルファイルから{len(urls)}件のURLを読み込みました")
                return urls
        except Exception as e:
            print(f"URLリストの読み込みエラー: {e}")
            return []
    return []

def save_urls(urls):
    """
    URLリストを保存する
    Googleスプレッドシートが設定されている場合はそちらに、なければローカルJSONファイルに保存する
    
    Args:
        urls: URLのリスト
    """
    # Googleスプレッドシートに保存を試みる
    client = get_google_sheets_client()
    if client:
        try:
            config = get_google_sheets_config()
            spreadsheet_id = config.get('spreadsheet_id')
            worksheet_name = config.get('worksheet_name', 'URLs')
            
            if spreadsheet_id:
                spreadsheet = client.open_by_key(spreadsheet_id)
                
                # ワークシートが存在しない場合は作成
                try:
                    worksheet = spreadsheet.worksheet(worksheet_name)
                except gspread.exceptions.WorksheetNotFound:
                    worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=2)
                    # ヘッダーを設定
                    worksheet.update('A1', 'URL')
                    worksheet.update('B1', '店舗名')
                
                # 既存のデータをクリア（ヘッダーを除く）
                existing_data = worksheet.get_all_values()
                if len(existing_data) > 1:
                    worksheet.delete_rows(2, len(existing_data))
                
                # 新しいデータを追加
                if urls:
                    # URLのみのリストを作成（店舗名は空）
                    values = [[url, ''] for url in urls]
                    worksheet.append_rows(values)
                
                return
        except Exception as e:
            print(f"Googleスプレッドシートへの保存エラー: {e}")
            # エラーが発生した場合はローカルファイルにフォールバック
    
    # ローカルJSONファイルに保存（フォールバック）
    data = {'urls': urls}
    with open(URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_premium_plan(html_content):
    """
    食べログページのHTMLから有料プランかどうかを判定する
    
    Args:
        html_content: HTMLコンテンツ（文字列）
    
    Returns:
        bool: 有料プランの場合True、無料プランの場合False
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 判定要素1: PR文セクションに 'pr-comment--unmember' クラスがあるか
    # このクラスがある場合は無料会員（支払い不備など）
    pr_comment_section = soup.find(class_='pr-comment')
    if pr_comment_section:
        classes = pr_comment_section.get('class', [])
        if 'pr-comment--unmember' in classes:
            return False  # 無料会員
    
    # 判定要素2: 「無料でお店のPRができます」という案内があるか
    # この案内がある場合は無料会員
    if '無料でお店のPRができます' in html_content:
        return False  # 無料会員
    
    # 上記の条件に該当しない場合は有料会員と判定
    return True

def extract_shop_name(html_content):
    """
    HTMLから店舗名を抽出する
    
    Args:
        html_content: HTMLコンテンツ（文字列）
    
    Returns:
        str: 店舗名（取得できない場合は空文字列）
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 店舗名の取得を試みる（複数のパターンを試す）
    # パターン1: h2 class="display-name"
    name_element = soup.find('h2', class_='display-name')
    if name_element:
        return name_element.get_text(strip=True)
    
    # パターン2: h1 class="display-name"
    name_element = soup.find('h1', class_='display-name')
    if name_element:
        return name_element.get_text(strip=True)
    
    # パターン3: titleタグから取得
    title_element = soup.find('title')
    if title_element:
        title_text = title_element.get_text(strip=True)
        # 「店舗名 | 食べログ」の形式から店舗名を抽出
        if '|' in title_text:
            return title_text.split('|')[0].strip()
        return title_text
    
    return ""

def check_tabelog_url(url):
    """
    食べログURLをチェックしてステータスを返す
    
    Args:
        url: チェックするURL
    
    Returns:
        dict: {
            'url': URL,
            'shop_name': 店舗名,
            'status': '有料' or '無料/要確認',
            'error': エラーメッセージ（エラーがない場合はNone）
        }
    """
    result = {
        'url': url,
        'shop_name': '',
        'status': '',
        'error': None
    }
    
    try:
        # URLの検証
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            result['error'] = '無効なURL形式です'
            result['status'] = 'エラー'
            return result
        
        # 食べログのURLかチェック
        if 'tabelog.com' not in parsed.netloc:
            result['error'] = '食べログのURLではありません'
            result['status'] = 'エラー'
            return result
        
        # リクエスト送信
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # HTMLパース
        html_content = response.text
        
        # 店舗名を抽出
        shop_name = extract_shop_name(html_content)
        result['shop_name'] = shop_name if shop_name else '取得失敗'
        
        # 有料/無料を判定
        if is_premium_plan(html_content):
            result['status'] = '有料'
        else:
            result['status'] = '無料/要確認'
        
    except requests.exceptions.Timeout:
        result['error'] = 'タイムアウトエラー'
        result['status'] = 'エラー'
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            result['error'] = '404エラー（ページが見つかりません）'
        else:
            result['error'] = f'HTTPエラー: {e.response.status_code}'
        result['status'] = 'エラー'
    except requests.exceptions.ConnectionError:
        result['error'] = '接続エラー'
        result['status'] = 'エラー'
    except Exception as e:
        result['error'] = f'予期しないエラー: {str(e)}'
        result['status'] = 'エラー'
    
    return result

def check_all_urls(urls, delay=1):
    """
    複数のURLをチェックする
    
    Args:
        urls: URLのリスト
        delay: アクセス間隔（秒）
    
    Returns:
        list: チェック結果のリスト
    """
    results = []
    for idx, url in enumerate(urls):
        result = check_tabelog_url(url)
        results.append(result)
        
        # アクセス間隔をあける（最後のURL以外）
        if idx < len(urls) - 1:
            import time
            time.sleep(delay)
    
    return results

def save_results_to_csv(results, filename=None):
    """
    結果をCSVファイルに保存する
    
    Args:
        results: チェック結果のリスト
        filename: ファイル名（Noneの場合は自動生成）
    
    Returns:
        str: 保存されたファイルのパス
    """
    import pandas as pd
    
    ensure_results_dir()
    
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"tabelog_check_result_{timestamp}.csv"
    
    filepath = os.path.join(RESULTS_DIR, filename)
    
    df = pd.DataFrame(results)
    df = df[['shop_name', 'url', 'status', 'error']]
    df.columns = ['店舗名', 'URL', 'ステータス', 'エラー']
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    return filepath

def ensure_results_dir():
    """結果保存用のディレクトリが存在するか確認し、なければ作成"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
