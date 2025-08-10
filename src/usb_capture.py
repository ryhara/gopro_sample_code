#================================================================
#================================================================
# API-AIO(LNX)
# SingleAoサンプル
#                                                CONTEC Co., Ltd.
#================================================================
#================================================================
import ctypes
import sys
import caio
import time
import signal
from gopro_connection import GoProConnection, discover_usb_ip

# Configuration constants
SERIAL_NUMBER_SUFFIX = "616"  # Change this to your camera's serial number last 3 digits
RECORDING_DURATION = 300  # 録画時間（秒）

# Global variables for signal handling
gopro = None
aio_id = None

def err_msg(buf):
    return buf.raw.split(b'\x00', 1)[0].decode('utf-8', errors='replace')

def signal_handler(signum, frame):
    """Handle Ctrl+C signal to stop recording gracefully"""
    global gopro, aio_id
    print("\nCtrl+Cが検出されました。録画を停止しています...")

    if gopro:
        try:
            stop_result = gopro.stop_video()
            print("録画停止")
        except Exception as e:
            print(f"録画停止エラー: {e}")

    # Send stop signal via AIO
    if aio_id:
        try:
            err_str = ctypes.create_string_buffer(256)
            lret = ctypes.c_long()
            lret.value = caio.AioOutputDoBit(aio_id, 0, 1)
            time.sleep(0.1)
            lret.value = caio.AioOutputDoBit(aio_id, 0, 0)

            # Clean up AIO device
            lret.value = caio.AioExit(aio_id)
        except Exception as e:
            print(f"AIO終了エラー: {e}")

    print("プログラムを終了します")
    sys.exit(0)

#================================================================
# 文字列を数値に変換できるかどうか確認する関数
#================================================================
def isnum(str, base):
    try:
        if 10 == base:
            int(str, 10)
        else:
            float(str)
    except:
        return False
    return True


#================================================================
# メイン関数
#================================================================
def main():
    global gopro, aio_id

    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    #----------------------------------------
    # 変数宣言
    #----------------------------------------
    err_str = ctypes.create_string_buffer(256)      # エラー文字列
    lret = ctypes.c_long()                          # 関数の戻り値
    aio_id = ctypes.c_short()                       # ID
    device_name = ctypes.create_string_buffer(50)   # デバイス名
    AoData = ctypes.c_float()                       # 変換データ
    MaxAoChannels = ctypes.c_short()                # 最大チャネル数
    usb_ip = discover_usb_ip(SERIAL_NUMBER_SUFFIX)
    gopro = GoProConnection(connection_type="usb", camera_ip=usb_ip)
    print("GoProにUSB接続を試行中...")
    # 有線USB制御を有効化
    print("有線USB制御を有効化中...")
    wired_control = gopro.enable_wired_usb_control()
    print(f"有線USB制御: {wired_control}")

    #----------------------------------------
    # デバイス名の入力確認
    #----------------------------------------
    device_name = "AIO000"
    #----------------------------------------
    # デバイスの初期化
    #----------------------------------------
    #----------------------------------------
    # 初期化処理
    #---cv)-------------------------------------
    lret.value = caio.AioInit(device_name.encode(), ctypes.byref(aio_id))
    if lret.value != 0:
        caio.AioGetErrorString(lret, err_str)
        print(f"AioInit = {lret.value} : {err_msg(err_str)}")
        sys.exit()
    #----------------------------------------
    # デバイスのリセット
    #----------------------------------------
    lret.value = caio.AioResetDevice(aio_id)
    if lret.value != 0:
        caio.AioGetErrorString(lret, err_str)
        print(f"AioResetDevice = {lret.value} : {err_msg(err_str)}")
        caio.AioExit(aio_id)
        sys.exit()

    #----------------------------------------
    # 指定チャネルを1回アナログ出力
    #----------------------------------------
    lret.value = caio.AioOutputDoBit(aio_id, 0, 1)
    time.sleep(0.1)
    lret.value = caio.AioOutputDoBit(aio_id, 0, 0)
    if lret.value != 0:
        caio.AioGetErrorString(lret, err_str)
        print(f"AioOutputDoBit = {lret.value} : {err_msg(err_str)}")
        caio.AioExit(aio_id)
        # sys.exit()

    # start capture
    start_result = gopro.start_video()
    print("録画開始（Ctrl+Cで停止）")

    try:
        for remaining in range(RECORDING_DURATION, 0, -1):
            print(f"\r残り {remaining} 秒...", end="", flush=True)
            time.sleep(1)

        # Normal completion
        stop_result = gopro.stop_video()
        print("\n録画終了")
    except KeyboardInterrupt:
        # This should be handled by signal_handler, but just in case
        pass

    lret.value = caio.AioOutputDoBit(aio_id, 0, 1)
    time.sleep(0.1)
    lret.value = caio.AioOutputDoBit(aio_id, 0, 0)
    if lret.value != 0:
        caio.AioGetErrorString(lret, err_str)
        print(f"AioOutputDoBit = {lret.value} : {err_msg(err_str)}")
        caio.AioExit(aio_id)
        sys.exit()
    #----------------------------------------
    # デバイスの終了
    #----------------------------------------
    lret.value = caio.AioExit(aio_id)
    if lret.value != 0:
        caio.AioGetErrorString(lret, err_str)
        print(f"AioExit = {lret.value} : {err_msg(err_str)}")
        sys.exit()

    print("finish")
    sys.exit()


#----------------------------------------
# main関数呼び出し
#----------------------------------------
if __name__ == "__main__":
    main()