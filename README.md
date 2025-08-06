> [!CAUTION]
> このコードはほぼAIによって生成されたコードです．
>
> usb接続と録画機能しか動作確認していません．
>
> APIリファレンスとこのコードを参考に自身でカスタム，検証して使うことを推奨します

# GoPro 11 Black Connection Library

GoPro 11 Black に接続して制御するための Python ライブラリです。

## ファイル構成

```
gopro/
├── src/
│   ├── gopro_connection.py    # メインクラス定義
│   ├── wifi_connection.py     # WiFi接続用スクリプト
│   ├── usb_connection.py      # USB接続用スクリプト
│   ├── main.py               # デモスクリプト
│   ├── video.py              # 録画スクリプト
│   ├── video_usb.py          # USB接続での録画スクリプト
│   └── video_wifi.py         # WiFi接続での録画スクリプト
├── README.md
└── pyproject.toml
```

## 機能

- WiFi 接続と USB 接続の両方をサポート
- 写真撮影・動画録画制御
- ウェブカメラモード制御
- カメラ設定の取得・変更
- メディアファイル管理
- 時間指定録画機能

## セットアップ

### 依存関係のインストール

```bash
uv sync
```

### GoPro 11 Black の準備

#### WiFi 接続の場合

1. GoPro カメラの WiFi アクセスポイントを有効にする
   -  GoProとスマホアプリを接続する
   -  スマホ画面側で`プレビューを有効にする`を押すとWi-FiがONになる
2. PCからカメラのWiFiに接続（SSID とパスワードはカメラの画面で確認可能）
3. WiFi用のプログラムを動かす

#### USB 接続の場合

1. USB-C ケーブルでカメラと PC を接続
2. カメラのシリアル番号を確認（バッテリー収納部のステッカーまたはカメラ UI）
3. シリアル番号の最後 3 桁から IP アドレスを計算
4. USB用のプログラムを動かす

## 使用方法

### 1. デモスクリプトの実行

```bash
cd src
```


```bash
# 基本的なデモ
python main.py

# WiFi接続専用
python wifi_connection.py

# USB接続専用
python usb_connection.py

# USB接続での録画
python video_usb.py

# WiFi接続での録画
python video_wifi.py
```

### 2. プログラムでの使用

```python
from gopro_connection import GoProConnection

# WiFi接続
gopro = GoProConnection(connection_type="wifi")

# USB接続（シリアル番号が必要）
from gopro_connection import discover_usb_ip
usb_ip = discover_usb_ip("789")  # 最後の3桁
gopro = GoProConnection(connection_type="usb", camera_ip=usb_ip)
```

### 3. カメラ制御

```python
# 写真撮影
gopro.take_photo()

# 動画録画を開始
gopro.start_video()

# 動画録画を停止
gopro.stop_video()
```

### 4. 時間指定録画

```python
# 10秒後に録画開始、60秒間録画
gopro.schedule_recording(10, 60)

# 14:30に録画開始、30分間録画
gopro.record_at_time('14:30', 30)

# スケジュールをキャンセル
gopro.cancel_scheduled_recording()
```

### 5. ウェブカメラモード

```python
# ウェブカメラを開始（1080p, Wide FOV）
gopro.start_webcam(resolution=12, fov=0)

# ウェブカメラを停止
gopro.stop_webcam()
```

### 6. メディアファイル管理

```python
# メディアファイルリストを取得
media_list = gopro.get_media_list()
```

### 7. 設定の取得・変更

```python
# 設定値を取得（例: 解像度設定）
resolution = gopro.get_settings(2)  # 設定ID 2 = 解像度

# 設定値を変更
gopro.set_setting(2, 12)  # 解像度を1080pに設定
```

## 実行方法

### WiFi 接続の場合

```bash
python wifi_connection.py
```

- カメラの WiFi アクセスポイントに接続してから実行
- インタラクティブモードでカメラを制御

### USB 接続の場合

```bash
python usb_connection.py
```

- シリアル番号の最後 3 桁を入力
- インタラクティブモードでカメラを制御

### デモ実行

```bash
python main.py
```

- WiFi 接続と USB 接続の両方をテスト
- 基本的な接続確認

## 注意事項

- GoPro 11 Black のファームウェアが最新版であることを確認してください
- WiFi 接続時は、カメラの WiFi アクセスポイントに接続してから API を使用してください
- USB 接続時は、シリアル番号の正確な確認が必要です
- カメラが録画中やシステムビジー状態の場合は、一部のコマンドが失敗する可能性があります

## サポートされている設定 ID

| 設定 ID | 設定項目               |
| ------- | ---------------------- |
| 2       | 動画解像度             |
| 3       | フレームレート         |
| 5       | 動画タイムラプスレート |
| 59      | 自動電源オフ           |
| 83      | GPS                    |
| 88      | LCD 明度               |
| 91      | LED                    |
| 108     | 動画アスペクト比       |
| 121     | 動画レンズ             |
| 122     | 写真レンズ             |
| 125     | 写真出力               |
| 128     | メディアフォーマット   |
| 134     | アンチフリッカー       |
| 135     | Hypersmooth            |
| 150     | 動画水平レベル調整     |
| 151     | 写真水平レベル調整     |

## 参考資料

- [Open GoPro HTTP API Documentation](https://gopro.github.io/OpenGoPro/http#section/Setup)
- [GoPro 11 Black ユーザーガイド](https://gopro.my.salesforce.com/sfc/p/#o0000000HJuF/a/3b000000NSrS/1pkAnpVWXhuK0VNFbooleEb5480gJ8l_NQOLHAsw6rA)
- [Quik (Mobile): How To Pair Your Camera](https://community.gopro.com/s/article/GoPro-Quik-How-To-Pair-Your-Camera?language=en_US#Hero91011Black)