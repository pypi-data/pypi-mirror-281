import add_path

import cv2

from video_stream import VideoStream


class VideoStreamTest:
    def __init__(self) -> None:
        self.video_stream = VideoStream(
            "rtsp://192.168.0.205:554/H264?W=1280&H=960&BR=2000000&FPS=30",
            ffmpeg_log_level="debug"
        )


def test_read_stream():
    # video_stream = VideoStream(
    #     "rtsp://192.168.0.205:554/H264?W=1280&H=960&BR=2000000&FPS=30",
    #     ffmpeg_log_level="debug"
    # )

    vst = VideoStreamTest()

    while True:
        ok, frame = vst.video_stream.stream_read()
        if not ok:
            continue

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


test_read_stream()
