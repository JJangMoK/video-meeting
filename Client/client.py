import numpy as np
import requests
import time
import json


def byte_to_frame(chunk, shape):
    return (np.frombuffer(chunk, dtype=np.uint8).reshape(shape))


class Client:
    def __init__(self, url, frame_per_sec=30):
        self.url = url
        self.frame_per_sec = frame_per_sec
        info = requests.get(url + "/info")
        self.info = eval(info.text)

    def request_frame(self, func):
        """
        @param func: feeds frame! func(frame)
        frame: RGB888 image as numpy array
        if you want stop video stream, then raise Any Exception.
        Instead, you have to handle it.
        """
        with requests.get(self.url + "/stream", stream=True) as r:
            for chunk in r.iter_content(chunk_size=self.info["size"]):
                frame = byte_to_frame(chunk, self.info["shape"])
                func(frame)
                time.sleep(1/self.frame_per_sec)

    def send_link(self, zoom_link):
        ans = requests.post(self.url + "/open_link", data={"url" : zoom_link})
        return ans.status_code != 400 
