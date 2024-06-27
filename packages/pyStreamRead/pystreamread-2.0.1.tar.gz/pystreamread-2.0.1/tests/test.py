import add_path

import cv2
import subprocess
import threading

from video_stream import VideoStream


def check_ping(ip_address):
    # 构造ping命令
    # '-c 1'表示只ping一次，'-W 1'表示超时时间为1秒
    command = ['ping', '-c', '1', '-W', '1', ip_address]

    # 执行ping命令
    try:
        # 执行ping命令，捕获输出
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True)

        # 检查输出中是否有"1 received"（表明ping通）
        if "1 received" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # ping命令返回非0状态，表示ping失败
        return False


class VideoStreamTest:
    def __init__(self) -> None:
        self.video_stream = VideoStream(
            "rtsp://192.168.0.206:554/H264?W=1280&H=960&BR=500000&FPS=30",
            ffmpeg_log_level="quiet"
        )


def connect_video_stream(vst):
    vst = VideoStreamTest()


def test_read_stream():
    # video_stream = VideoStream(
    #     "rtsp://192.168.0.205:554/H264?W=1280&H=960&BR=2000000&FPS=30",
    #     ffmpeg_log_level="debug"
    # )

    vst = VideoStreamTest()
    no_connect_count = 0
    while True:
        try:
            # if not check_ping("192.168.0.206"):
            #     vst.video_stream.open()

            ok, frame = vst.video_stream.stream_read()
            if not ok:
                # print("nnnnnn???????-------********~~~~~~")
                if no_connect_count > 10:
                    vst.video_stream.close()
                    vst.video_stream.open()
                    no_connect_count = 0

                no_connect_count += 1
                continue
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            break


test_read_stream()
