import requests
import time
import json
import threading
from typing import Optional, Dict, Any
import socket
import struct
from datetime import datetime, timedelta


class GoProConnection:
    """GoPro 11 Blackに接続するためのクラス"""

    def __init__(self, connection_type: str = "wifi", camera_ip: str = "10.5.5.9", port: int = 8080):
        """
        GoPro接続を初期化

        Args:
            connection_type: "wifi" または "usb"
            camera_ip: カメラのIPアドレス
            port: ポート番号（デフォルト: 8080）
        """
        self.connection_type = connection_type
        self.camera_ip = camera_ip
        self.port = port
        self.base_url = f"http://{camera_ip}:{port}"
        self.session = requests.Session()
        self.session.timeout = 10
        self.recording_timer = None
        self.stop_timer = None

    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        GoPro APIにリクエストを送信

        Args:
            endpoint: APIエンドポイント
            method: HTTPメソッド
            params: クエリパラメータ

        Returns:
            レスポンスデータ
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params)
            elif method.upper() == "PUT":
                response = self.session.put(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": str(e)}

    def get_camera_state(self) -> Dict[str, Any]:
        """カメラの状態を取得"""
        return self._make_request("/gopro/camera/state")

    def get_camera_info(self) -> Dict[str, Any]:
        """カメラ情報を取得"""
        return self._make_request("/gopro/camera/info")

    def get_media_list(self) -> Dict[str, Any]:
        """メディアファイルリストを取得"""
        return self._make_request("/gopro/media/list")

    def start_webcam(self, resolution: int = 12, fov: int = 0, port: int = 8554, protocol: str = "RTSP") -> Dict[str, Any]:
        """
        ウェブカメラモードを開始

        Args:
            resolution: 解像度 (4=480p, 7=720p, 12=1080p)
            fov: 視野角 (0=Wide, 2=Narrow, 3=Superview, 4=Linear)
            port: ストリーミングポート
            protocol: プロトコル ("RTSP" または "TS")
        """
        params = {
            "res": resolution,
            "fov": fov,
            "port": port,
            "protocol": protocol
        }
        return self._make_request("/gopro/webcam/start", params=params)

    def stop_webcam(self) -> Dict[str, Any]:
        """ウェブカメラモードを停止"""
        return self._make_request("/gopro/webcam/stop")

    def get_webcam_status(self) -> Dict[str, Any]:
        """ウェブカメラの状態を取得"""
        return self._make_request("/gopro/webcam/status")

    def take_photo(self) -> Dict[str, Any]:
        """写真を撮影"""
        return self._make_request("/gopro/camera/shutter/start")

    def start_video(self) -> Dict[str, Any]:
        """動画録画を開始"""
        return self._make_request("/gopro/camera/shutter/start")

    def stop_video(self) -> Dict[str, Any]:
        """動画録画を停止"""
        return self._make_request("/gopro/camera/shutter/stop")

    def schedule_recording(self, delay_seconds: int, duration_seconds: Optional[int] = None) -> Dict[str, Any]:
        """
        時間指定で録画をスケジュール

        Args:
            delay_seconds: 録画開始までの遅延時間（秒）
            duration_seconds: 録画時間（秒）。Noneの場合は手動で停止するまで録画

        Returns:
            スケジュール結果
        """
        if delay_seconds < 0:
            return {"error": "Delay must be positive"}

        print(f"録画を {delay_seconds} 秒後に開始します...")

        # 録画開始タイマー
        self.recording_timer = threading.Timer(delay_seconds, self._start_recording)
        self.recording_timer.start()

        # 録画停止タイマー（durationが指定されている場合）
        if duration_seconds and duration_seconds > 0:
            self.stop_timer = threading.Timer(delay_seconds + duration_seconds, self._stop_recording)
            self.stop_timer.start()
            print(f"録画は {duration_seconds} 秒間続きます")

        return {"message": f"Recording scheduled to start in {delay_seconds} seconds"}

    def _start_recording(self):
        """録画を開始（内部メソッド）"""
        try:
            result = self.start_video()
            print(f"録画を開始しました: {result}")
        except Exception as e:
            print(f"録画開始エラー: {e}")

    def _stop_recording(self):
        """録画を停止（内部メソッド）"""
        try:
            result = self.stop_video()
            print(f"録画を停止しました: {result}")
        except Exception as e:
            print(f"録画停止エラー: {e}")

    def cancel_scheduled_recording(self) -> Dict[str, Any]:
        """スケジュールされた録画をキャンセル"""
        if self.recording_timer:
            self.recording_timer.cancel()
            self.recording_timer = None
            print("録画開始タイマーをキャンセルしました")

        if self.stop_timer:
            self.stop_timer.cancel()
            self.stop_timer = None
            print("録画停止タイマーをキャンセルしました")

        return {"message": "Scheduled recording cancelled"}

    def record_at_time(self, start_time: str, duration_minutes: Optional[int] = None) -> Dict[str, Any]:
        """
        指定した時刻に録画を開始

        Args:
            start_time: 開始時刻（"HH:MM" 形式、例: "14:30"）
            duration_minutes: 録画時間（分）。Noneの場合は手動で停止するまで録画

        Returns:
            スケジュール結果
        """
        try:
            # 現在時刻を取得
            now = datetime.now()

            # 開始時刻を解析
            start_hour, start_minute = map(int, start_time.split(":"))
            target_time = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

            # 今日の指定時刻が既に過ぎている場合は明日に設定
            if target_time <= now:
                target_time += timedelta(days=1)

            # 遅延時間を計算（秒）
            delay_seconds = int((target_time - now).total_seconds())

            print(f"録画開始時刻: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"現在時刻: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"遅延時間: {delay_seconds} 秒")

            # 録画時間を秒に変換
            duration_seconds = duration_minutes * 60 if duration_minutes else None

            return self.schedule_recording(delay_seconds, duration_seconds)

        except ValueError as e:
            return {"error": f"Invalid time format: {e}. Use HH:MM format (e.g., '14:30')"}

    def get_settings(self, setting_id: int) -> Dict[str, Any]:
        """
        設定値を取得

        Args:
            setting_id: 設定ID
        """
        return self._make_request(f"/gopro/camera/setting?option={setting_id}")

    def set_setting(self, setting_id: int, value: int) -> Dict[str, Any]:
        """
        設定値を変更

        Args:
            setting_id: 設定ID
            value: 設定値
        """
        params = {"option": setting_id, "value": value}
        return self._make_request("/gopro/camera/setting", method="POST", params=params)

    def keep_alive(self) -> Dict[str, Any]:
        """接続を維持するためのキープアライブ信号を送信"""
        return self._make_request("/gopro/camera/keep_alive")

    def enable_wired_usb_control(self) -> Dict[str, Any]:
        """USB経由での有線制御を有効化（USB接続時のみ）"""
        if self.connection_type == "usb":
            return self._make_request("/gopro/camera/control/wired_usb?p=1")
        else:
            return {"error": "This command is only available for USB connections"}


def discover_usb_ip(serial_number: str) -> str:
    """
    USB接続時のIPアドレスを計算

    Args:
        serial_number: カメラのシリアル番号（最後の3桁を使用）

    Returns:
        計算されたIPアドレス
    """
    if len(serial_number) < 3:
        raise ValueError("Serial number must be at least 3 digits")

    last_three = serial_number[-3:]
    x = int(last_three[0])
    y = int(last_three[1])
    z = int(last_three[2])

    return f"172.2{x}.1{y}{z}.51"