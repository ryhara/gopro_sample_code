#!/usr/bin/env python3
"""
GoPro 11 Black 時間指定録画スクリプト（USB接続）
"""

import time
import sys
import threading
from gopro_connection import GoProConnection, discover_usb_ip

# Configuration constants
SERIAL_NUMBER_SUFFIX = "616"  # Change this to your camera's serial number last 3 digits
RECORDING_DURATION = 5       # Recording duration in seconds


def main():
    """USB接続での時間指定録画"""
    print("GoPro 11 Black 時間指定録画")
    print("=" * 40)

    try:
        # IPアドレスを計算
        usb_ip = discover_usb_ip(SERIAL_NUMBER_SUFFIX)
        print(f"計算されたUSB IPアドレス: {usb_ip}")
        print(f"録画時間: {RECORDING_DURATION}秒")

        # USB接続でGoProに接続
        gopro = GoProConnection(connection_type="usb", camera_ip=usb_ip)
        print("GoProにUSB接続を試行中...")

        # 有線USB制御を有効化
        print("有線USB制御を有効化中...")
        wired_control = gopro.enable_wired_usb_control()
        print(f"有線USB制御: {wired_control}")

        # カメラの状態を確認
        print("カメラの状態を確認中...")
        state = gopro.get_camera_state()
        print(f"カメラ状態: {state}")

        print(f"\n録画開始！ {RECORDING_DURATION}秒後に自動停止します...")

        # 録画開始
        start_result = gopro.start_video()
        print(f"録画開始結果: {start_result}")

        # カウントダウン表示
        for remaining in range(RECORDING_DURATION, 0, -1):
            print(f"\r残り時間: {remaining}秒", end="", flush=True)
            time.sleep(1)

        print("\n録画停止中...")

        # 録画停止
        stop_result = gopro.stop_video()
        print(f"録画停止結果: {stop_result}")

        print("\n" + "=" * 40)
        print(f"{RECORDING_DURATION}秒間の録画が完了しました！")

    except ValueError as e:
        print(f"エラー: {e}")
        print("シリアル番号の設定を確認してください")
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("録画を手動で停止してください")
        sys.exit(1)


if __name__ == "__main__":
    main()
