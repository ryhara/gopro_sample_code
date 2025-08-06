#!/usr/bin/env python3
"""
GoPro 11 Black WiFi接続用スクリプト
"""

import time
import sys
from gopro_connection import GoProConnection


def main():
    """WiFi接続でのGoPro制御"""
    print("GoPro 11 Black WiFi接続テスト")
    print("=" * 40)

    try:
        # WiFi接続でGoProに接続
        gopro = GoProConnection(connection_type="wifi")
        print("GoProにWiFi接続を試行中...")

        # カメラの状態を確認
        print("\n1. カメラの状態を確認:")
        state = gopro.get_camera_state()
        print(f"カメラ状態: {state}")

        # カメラ情報を取得
        print("\n2. カメラ情報を取得:")
        info = gopro.get_camera_info()
        print(f"カメラ情報: {info}")

        # ウェブカメラの状態を確認
        print("\n3. ウェブカメラの状態を確認:")
        webcam_status = gopro.get_webcam_status()
        print(f"ウェブカメラ状態: {webcam_status}")

        # キープアライブを送信
        print("\n4. キープアライブを送信:")
        keep_alive = gopro.keep_alive()
        print(f"キープアライブ: {keep_alive}")

        # メディアファイルリストを取得
        print("\n5. メディアファイルリストを取得:")
        media_list = gopro.get_media_list()
        print(f"メディアファイル数: {len(media_list.get('media', []))}")

        print("\n" + "=" * 40)
        print("WiFi接続テスト完了！")
        print("\n利用可能なコマンド:")
        print("- gopro.take_photo() - 写真撮影")
        print("- gopro.start_video() - 動画録画開始")
        print("- gopro.stop_video() - 動画録画停止")
        print("- gopro.schedule_recording(10, 60) - 10秒後に録画開始、60秒間録画")
        print("- gopro.record_at_time('14:30', 30) - 14:30に録画開始、30分間録画")
        print("- gopro.start_webcam() - ウェブカメラ開始")
        print("- gopro.stop_webcam() - ウェブカメラ停止")
        print("- gopro.get_media_list() - メディアファイル一覧取得")

        # インタラクティブモード
        print("\nインタラクティブモードを開始します...")
        print("コマンドを入力してください（'quit'で終了）:")

        while True:
            try:
                command = input("> ").strip()

                if command.lower() == 'quit':
                    print("終了します")
                    break
                elif command.lower() == 'photo':
                    result = gopro.take_photo()
                    print(f"写真撮影: {result}")
                elif command.lower() == 'video_start':
                    result = gopro.start_video()
                    print(f"動画録画開始: {result}")
                elif command.lower() == 'video_stop':
                    result = gopro.stop_video()
                    print(f"動画録画停止: {result}")
                elif command.lower() == 'webcam_start':
                    result = gopro.start_webcam()
                    print(f"ウェブカメラ開始: {result}")
                elif command.lower() == 'webcam_stop':
                    result = gopro.stop_webcam()
                    print(f"ウェブカメラ停止: {result}")
                elif command.lower() == 'state':
                    result = gopro.get_camera_state()
                    print(f"カメラ状態: {result}")
                elif command.lower() == 'media':
                    result = gopro.get_media_list()
                    print(f"メディアファイル: {result}")
                elif command.lower() == 'help':
                    print("利用可能なコマンド:")
                    print("  photo - 写真撮影")
                    print("  video_start - 動画録画開始")
                    print("  video_stop - 動画録画停止")
                    print("  webcam_start - ウェブカメラ開始")
                    print("  webcam_stop - ウェブカメラ停止")
                    print("  state - カメラ状態確認")
                    print("  media - メディアファイル一覧")
                    print("  help - ヘルプ表示")
                    print("  quit - 終了")
                else:
                    print("不明なコマンドです。'help'で利用可能なコマンドを確認してください。")

            except KeyboardInterrupt:
                print("\n終了します")
                break
            except Exception as e:
                print(f"エラー: {e}")

    except Exception as e:
        print(f"WiFi接続エラー: {e}")
        print("\n接続を確認してください:")
        print("1. GoProカメラのWiFiアクセスポイントが有効になっているか")
        print("2. PCがGoProのWiFiネットワークに接続されているか")
        print("3. カメラのIPアドレスが正しいか（デフォルト: 10.5.5.9:8080）")
        sys.exit(1)


if __name__ == "__main__":
    main()