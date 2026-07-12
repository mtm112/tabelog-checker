"""
通知機能モジュール
LINE Messaging API、メール通知をサポート
"""
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# 通知設定（Streamlit Secrets / 環境変数から読み込み）
# ============================================

def _parse_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('true', '1', 'yes', 'on')


def _get_notification_config_from_env():
    """環境変数から通知設定を取得（GitHub Actions等）"""
    return {
        'LINE_MESSAGING_ENABLED': _parse_bool(os.environ.get('LINE_MESSAGING_ENABLED')),
        'LINE_MESSAGING_CHANNEL_ACCESS_TOKEN': os.environ.get('LINE_MESSAGING_CHANNEL_ACCESS_TOKEN', ''),
        'LINE_MESSAGING_USER_ID': os.environ.get('LINE_MESSAGING_USER_ID', ''),
        'EMAIL_ENABLED': _parse_bool(os.environ.get('EMAIL_ENABLED')),
        'EMAIL_TO': os.environ.get('EMAIL_TO', ''),
        'SMTP_SERVER': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
        'SMTP_PORT': int(os.environ.get('SMTP_PORT', '587') or 587),
        'SMTP_USER': os.environ.get('SMTP_USER', ''),
        'SMTP_PASSWORD': os.environ.get('SMTP_PASSWORD', ''),
    }


def get_notification_config():
    """
    通知設定を取得
    優先順位: Streamlit Secrets → 環境変数

    Returns:
        dict: 通知設定
    """
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and 'notifier' in st.secrets:
            return st.secrets['notifier']
    except Exception:
        pass

    env_config = _get_notification_config_from_env()
    if env_config.get('LINE_MESSAGING_CHANNEL_ACCESS_TOKEN') or env_config.get('EMAIL_TO'):
        return env_config
    return {}

def get_line_messaging_config():
    """LINE Messaging API設定を取得"""
    config = get_notification_config()
    return {
        'enabled': config.get('LINE_MESSAGING_ENABLED', False),
        'channel_access_token': config.get('LINE_MESSAGING_CHANNEL_ACCESS_TOKEN', ''),
        'user_id': config.get('LINE_MESSAGING_USER_ID', '')
    }

def get_email_config():
    """メール通知設定を取得"""
    config = get_notification_config()
    return {
        'enabled': config.get('EMAIL_ENABLED', False),
        'to': config.get('EMAIL_TO', ''),
        'smtp': {
            'server': config.get('SMTP_SERVER', 'smtp.gmail.com'),
            'port': config.get('SMTP_PORT', 587),
            'user': config.get('SMTP_USER', ''),
            'password': config.get('SMTP_PASSWORD', '')
        }
    }

def send_line_messaging_api(message, user_id=None, channel_access_token=None):
    """
    LINE Messaging APIで通知を送信
    
    Args:
        message: 送信するメッセージ
        user_id: 送信先のユーザーID（Noneの場合はStreamlit Secretsから取得）
        channel_access_token: チャネルアクセストークン（Noneの場合はStreamlit Secretsから取得）
    
    Returns:
        bool: 送信成功時True
    """
    if user_id is None or channel_access_token is None:
        line_config = get_line_messaging_config()
        if user_id is None:
            user_id = line_config.get('user_id', '')
        if channel_access_token is None:
            channel_access_token = line_config.get('channel_access_token', '')
    
    if not user_id or not channel_access_token:
        print("LINE Messaging APIの設定が不完全です（ユーザーIDまたはチャネルアクセストークンが設定されていません）")
        return False
    
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    data = {
        'to': user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"LINE Messaging API送信エラー: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"レスポンス: {e.response.text}")
        return False

def send_email(subject, body, to_email=None, smtp_config=None):
    """
    メールで通知を送信
    
    Args:
        subject: 件名
        body: 本文
        to_email: 送信先メールアドレス
        smtp_config: SMTP設定（辞書形式）
    
    Returns:
        bool: 送信成功時True
    """
    if not to_email:
        print("送信先メールアドレスが設定されていません")
        return False
    
    if not smtp_config:
        print("SMTP設定が設定されていません")
        return False
    
    smtp_server = smtp_config.get('server', 'smtp.gmail.com')
    smtp_port = smtp_config.get('port', 587)
    smtp_user = smtp_config.get('user')
    smtp_password = smtp_config.get('password')
    
    if not smtp_user or not smtp_password:
        print("SMTP設定が不完全です")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False

def notify_free_restaurants(results):
    """
    無料/要確認の店舗がある場合に通知を送信
    
    Args:
        results: チェック結果のリスト
    """
    free_restaurants = [r for r in results if r['status'] == '無料/要確認']
    
    if not free_restaurants:
        return
    
    # 通知設定を取得
    line_config = get_line_messaging_config()
    email_config = get_email_config()
    
    # 通知を送信するかチェック
    if not line_config.get('enabled', False) and not email_config.get('enabled', False):
        return
    
    # メッセージを作成
    message_lines = ["⚠️ 無料/要確認の店舗が見つかりました\n"]
    message_lines.append("以下の店舗が無料プランに変更されています：\n")
    for r in free_restaurants:
        shop_name = r['shop_name'] if r['shop_name'] else '店舗名不明'
        message_lines.append(f"・{shop_name}")
        message_lines.append(f"  {r['url']}\n")
    
    message = '\n'.join(message_lines)
    
    # LINE Messaging APIで通知
    if line_config.get('enabled', False):
        send_line_messaging_api(
            message,
            user_id=line_config.get('user_id'),
            channel_access_token=line_config.get('channel_access_token')
        )
    
    # メールで通知
    if email_config.get('enabled', False) and email_config.get('to'):
        subject = f"【食べログチェッカー】無料/要確認の店舗が{len(free_restaurants)}件見つかりました"
        send_email(subject, message, email_config.get('to'), email_config.get('smtp'))
