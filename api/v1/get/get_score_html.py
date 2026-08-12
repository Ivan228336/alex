import os.path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from settings import get_data_dir
from repository.v1.post.post_score import GameRepository
from PIL import Image

router = APIRouter()


@router.get("/get_score_html/{court_id}", response_class=HTMLResponse)
def get_html(court_id: int = 0):
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

    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                html, body {{
                    width: 1920px;
                    height: 1080px;
                    background-color: rgba(0, 0, 0, 0); /* прозрачный фон */
                    overflow: hidden;
                    position: relative;
                }}
    
                /* Картинка с чёткими размерами в правом верхнем углу */
                img {{
                    position: fixed;
                    top: 60px;
                    right: 40px;
                    max-width: 330px;
                    max-height: 100px;
                    width: auto;
                    height: auto;
                    object-fit: contain;
                    image-rendering: crisp-edges;
                    display: block;
                }}
            </style>
        </head>
        <body>
            <img src="/get_score/{court_id}" alt="Score">
        </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
