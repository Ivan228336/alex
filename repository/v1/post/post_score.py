from models.models import Game
import json
from settings import get_data_dir, get_base_dir
import os


html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Score Overlay</title>
    <style>
        body {{
            margin: 0;
            background-color: #ffff0000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        img {{
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <img id="scoreImage" src="http://127.0.0.1:8000/get_score" alt="Tennis Score">
    <script>
        const imgElement = document.getElementById('scoreImage');
        const url = 'http://127.0.0.1:8000/get_score/{0}';
        setInterval(() => {{
            imgElement.src = url + '?t=' + new Date().getTime();
        }}, 500); // 500 мс = 0.5 сек
    </script>
</body>
</html>"""


class GameRepository:
    def update(self, score: Game, court_id: int, image):
        data_dir = get_data_dir() / "media"
        data_dir.mkdir(exist_ok=True)
        with open(f"{data_dir}/data_{court_id}.json", "w", encoding="utf-8") as f:
            json.dump(score.model_dump(), f, ensure_ascii=False)


        dir_out = get_data_dir() / "media"
        dir_out.mkdir(exist_ok=True)
        path = dir_out / f"tennis_score_{court_id}.png"

        image.save(path, format="PNG")
        image.close()

        # if not os.path.exists(dir_out / f"tennis_score_{court_id}.html"):
        #     html = f"""<!DOCTYPE html>
        #                 <html lang="ru">
        #                 <head>
        #                     <meta charset="UTF-8">
        #                     <title>Score Overlay</title>
        #                     <style>
        #                         body {{
        #                             margin: 0;
        #                             background-color: #ffff0000;
        #                             display: flex;
        #                             justify-content: center;
        #                             align-items: center;
        #                             height: 100vh;
        #                         }}
        #                         img {{
        #                             max-width: 100%;
        #                         }}
        #                     </style>
        #                 </head>
        #                 <body>
        #                     <img id="scoreImage" src="http://127.0.0.1:8000/get_score" alt="Tennis Score">
        #                     <script>
        #                         const imgElement = document.getElementById('scoreImage');
        #                         const url = 'http://127.0.0.1:8000/get_score/{court_id}';
        #                         setInterval(() => {{
        #                             imgElement.src = url + '?t=' + new Date().getTime();
        #                         }}, 500); // 500 мс = 0.5 сек
        #                     </script>
        #                 </body>
        #                 </html>"""
        #
        #     with open(f"{data_dir}/tennis_score_{court_id}.html", "w", encoding="utf-8") as html_f:
        #         html_f.write(html)

    def get_skin(self):
        skin_dir = get_data_dir() / "skin"
        image_path = skin_dir / "skin.png"
        if not os.path.exists(image_path):
            return get_base_dir() / "static" / "score_empty.png"
        return image_path
