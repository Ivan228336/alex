from models.models import Game
from utils.image_draw import TennisDraw
from repository.v1.post.post_score import GameRepository
import logging

class GameService:
    def update(self, score: Game, court_id: int):
        try:
            gr = GameRepository()
            path = gr.get_skin()
            td = TennisDraw(data=score)
            image = td.draw_all(path=path)
            gr.update(score=score, court_id=court_id, image=image)
        except Exception as e:
            logging.error("Ошибка при сохраннии", exc_info=True)
            raise e
