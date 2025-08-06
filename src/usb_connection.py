#!/usr/bin/env python3
"""
GoPro 11 Black USB接続用スクリプト
"""

import time
import sys
from gopro_connection import GoProConnection, discover_usb_ip


def main():
    """USB接続でのGoPro制御"""
    print("GoPro 11 Black USB接続テスト")
    print("=" * 40)

    # シリアル番号の入力
    print("カメラのシリアル番号を入力してください")
    print("シリアル番号は以下の方法で確認できます:")
    print("- カメラのバッテリー収納部のステッカー")
    print("- カメラUI: Preferences >> About >> Camera Info")
    print("- Bluetooth Low Energy: Hardware Infoから読み取り")
    print("\n例: シリアル番号が 'C0000123456789' の場合、'789' を入力")

    while True:
        try:
            serial_input = input("シリアル番号（最後の3桁）: ").strip()

            if len(serial_input) < 3:
                print("エラー: シリアル番号は最低3桁必要です")
                continue

            # IPアドレスを計算
            usb_ip = discover_usb_ip(serial_input)
            print(f"計算されたUSB IPアドレス: {usb_ip}")

            # 確認
            confirm = input(f"IPアドレス {usb_ip} で接続しますか？ (y/n): ").strip().lower()
            if confirm == 'y':
                break
            else:
                print("シリアル番号を再入力してください")

        except ValueError as e:
            print(f"エラー: {e}")
        except KeyboardInterrupt:
            print("\n終了します")
            sys.exit(0)

    try:
        # USB接続でGoProに接続
        gopro = GoProConnection(connection_type="usb", camera_ip=usb_ip)
        print("GoProにUSB接続を試行中...")

        # 有線USB制御を有効化
        print("\n1. 有線USB制御を有効化:")
        wired_control = gopro.enable_wired_usb_control()
        print(f"有線USB制御: {wired_control}")

        # カメラの状態を確認
        print("\n2. カメラの状態を確認:")
        state = gopro.get_camera_state()
        print(f"カメラ状態: {state}")

        # カメラ情報を取得
        print("\n3. カメラ情報を取得:")
        info = gopro.get_camera_info()
        print(f"カメラ情報: {info}")

        # ウェブカメラの状態を確認
        print("\n4. ウェブカメラの状態を確認:")
        webcam_status = gopro.get_webcam_status()
        print(f"ウェブカメラ状態: {webcam_status}")

        # キープアライブを送信
        print("\n5. キープアライブを送信:")
        keep_alive = gopro.keep_alive()
        print(f"キープアライブ: {keep_alive}")

        # メディアファイルリストを取得
        print("\n6. メディアファイルリストを取得:")
        media_list = gopro.get_media_list()
        print(f"メディアファイル数: {len(media_list.get('media', []))}")

        print("\n" + "=" * 40)
        print("USB接続テスト完了！")
        print("\n利用可能なコマンド:")
        print("- photo - 写真撮影")
        print("- video_start - 動画録画開始")
        print("- video_stop - 動画録画停止")
        print("- webcam_start - ウェブカメラ開始")
        print("- webcam_stop - ウェブカメラ停止")
        print("- state - カメラ状態確認")
        print("- media - メディアファイル一覧")

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
        print(f"USB接続エラー: {e}")
        print("\n接続を確認してください:")
        print("1. USB-CケーブルでカメラとPCが接続されているか")
        print("2. シリアル番号が正しいか")
        print("3. カメラの電源が入っているか")
        sys.exit(1)


if __name__ == "__main__":
    main()