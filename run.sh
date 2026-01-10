#!/bin/bash

# 仮想環境をアクティベートしてStreamlitアプリを起動するスクリプト

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境が存在するか確認
if [ ! -d "venv" ]; then
    echo "仮想環境が見つかりません。作成します..."
    python3 -m venv venv
    echo "仮想環境を作成しました。"
fi

# 仮想環境をアクティベート
source venv/bin/activate

# パッケージがインストールされているか確認
if ! python -c "import streamlit" 2>/dev/null; then
    echo "必要なパッケージをインストールします..."
    pip install -r requirements.txt
fi

# Streamlitアプリを起動
echo "アプリを起動しています..."
streamlit run app.py
