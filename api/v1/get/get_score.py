import os.path

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from settings import get_data_dir
from utils.generate_frames import generate_frames
from repository.v1.post.post_score import GameRepository
from PIL import Image

router = APIRouter()

class MJPEGStreamingResponse(StreamingResponse):
    media_type = "multipart/x-mixed-replace; boundary=frame"


@router.get("/get_score/{court_id}")
async def get_image(court_id: int = 0):
    if 0 > court_id or court_id > 10:
        return {"error": "Номер корта должен быть меньше 10"}
    proj_dir = get_data_dir()
    image_path = proj_dir / "media" / f"tennis_score_{court_id}.png"
    if not os.path.exists(image_path):
        gr = GameRepository()
        path = gr.get_skin()
        image = Image.open(path).convert("RGBA")
        image.save(image_path, format="PNG")
        image.close()
    return MJPEGStreamingResponse(generate_frames(image_path))
