import asyncio
import os
from repository.v1.post.post_score import GameRepository as gr
from PIL import Image

class FrameBuffer:
    def __init__(self, court_id: int, fps: int = 2):
        self.court_id = court_id
        self.interval = 1.0 / fps
        self._last_frame: bytes = None

        pass

    def get_current_frame(self):
        return self.current_frame

    def update_frame(self, new_frame):
        self.current_frame = new_frame

    def frames_loop(self):
        pass
