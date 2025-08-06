#!/usr/bin/env python3
"""
GoPro 11 Black 接続デモスクリプト
"""

from gopro_connection import GoProConnection, discover_usb_ip


def main():
    """GoPro 11 Black接続デモ"""
    print("GoPro 11 Black 接続デモ")
    print("=" * 40)

    print("接続方法を選択してください:")
    print("1. WiFi接続")
    print("2. USB接続")
    print("3. 両方の接続をテスト")

    while True:
        choice = input("選択 (1/2/3): ").strip()

        if choice == "1":
            wifi_demo()
            break
        elif choice == "2":
            usb_demo()
            break
        elif choice == "3":
            wifi_demo()
            print("\n" + "=" * 40)
            usb_demo()
            break
        else:
            print("1、2、または3を入力してください")


def wifi_demo():
    """WiFi接続デモ"""
    print("\nWiFi接続デモ")
    print("-" * 20)

    try:
        gopro = GoProConnection(connection_type="wifi")
        print("GoProにWiFi接続を試行中...")

        # 基本的なテスト
        state = gopro.get_camera_state()
        print(f"カメラ状態: {state}")

        info = gopro.get_camera_info()
        print(f"カメラ情報: {info}")

        print("WiFi接続テスト完了！")

    except Exception as e:
        print(f"WiFi接続エラー: {e}")


def usb_demo():
    """USB接続デモ"""
    print("\nUSB接続デモ")
    print("-" * 20)

    print("シリアル番号の最後3桁を入力してください:")
    print("例: シリアル番号が 'C0000123456789' の場合、'789' を入力")

    try:
        serial_input = input("シリアル番号（最後の3桁）: ").strip()

        if len(serial_input) < 3:
            print("エラー: シリアル番号は最低3桁必要です")
            return

        # IPアドレスを計算
        usb_ip = discover_usb_ip(serial_input)
        print(f"計算されたUSB IPアドレス: {usb_ip}")

        gopro = GoProConnection(connection_type="usb", camera_ip=usb_ip)
        print("GoProにUSB接続を試行中...")

        # 有線USB制御を有効化
        wired_control = gopro.enable_wired_usb_control()
        print(f"有線USB制御: {wired_control}")

        # 基本的なテスト
        state = gopro.get_camera_state()
        print(f"カメラ状態: {state}")

        print("USB接続テスト完了！")

    except Exception as e:
        print(f"USB接続エラー: {e}")


if __name__ == "__main__":
    main()
