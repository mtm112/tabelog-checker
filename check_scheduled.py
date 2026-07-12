#!/usr/bin/env python3
"""
スケジュール実行用のバッチスクリプト
毎月3-15日の間、登録されているURLを自動チェックします。
"""
import sys
from datetime import datetime
from tabelog_checker import load_urls, check_all_urls, save_results_to_csv, ensure_results_dir
from notifier import notify_free_restaurants

SCHEDULE_DAY_START = 3
SCHEDULE_DAY_END = 15

def main():
    """メイン処理"""
    # 実行日を確認（毎月3-15日の間のみ実行）
    today = datetime.now()
    day = today.day

    if day < SCHEDULE_DAY_START or day > SCHEDULE_DAY_END:
        print(f"今日は{day}日です。スケジュール実行は毎月{SCHEDULE_DAY_START}-{SCHEDULE_DAY_END}日の間のみです。")
        sys.exit(0)
    
    print(f"スケジュールチェック実行: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # URLリストを読み込み
    urls = load_urls()
    
    if not urls:
        print("⚠️  登録されているURLがありません。")
        sys.exit(0)
    
    print(f"📋 チェック対象URL: {len(urls)}件")
    print("-" * 50)
    
    # チェック実行
    try:
        results = check_all_urls(urls, delay=1)
        
        # 結果を保存
        ensure_results_dir()
        timestamp = today.strftime('%Y%m%d_%H%M%S')
        filename = f"tabelog_check_result_{timestamp}.csv"
        saved_file = save_results_to_csv(results, filename)
        
        # 結果サマリー
        total = len(results)
        premium = len([r for r in results if r['status'] == '有料'])
        free = len([r for r in results if r['status'] == '無料/要確認'])
        error = len([r for r in results if r['status'] == 'エラー'])
        
        print("-" * 50)
        print("✅ チェック完了")
        print(f"   総件数: {total}")
        print(f"   有料: {premium}")
        print(f"   無料/要確認: {free}")
        print(f"   エラー: {error}")
        print(f"   結果ファイル: {saved_file}")
        print("-" * 50)
        
        # 無料/要確認がある場合は警告表示
        if free > 0:
            print("⚠️  無料/要確認の店舗があります！")
            for result in results:
                if result['status'] == '無料/要確認':
                    print(f"   - {result['shop_name']}: {result['url']}")

        # 通知を送信（無料/要確認あり、または毎月3日の定期報告）
        notify_free_restaurants(results, check_date=today)
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
