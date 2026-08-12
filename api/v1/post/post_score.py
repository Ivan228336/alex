from fastapi import APIRouter
from models.models import Game
from service.v1.post.post_score import GameService
from fastapi import HTTPException

router = APIRouter()


@router.post("/post_score/{court_id}")
async def post_score(payload: Game, court_id: int = 0):
    try:
        GameService().update(payload, court_id)
    except Exception as e:
        return HTTPException(400, str(e))
    return 200, {
        "message": "Успешно обновлено"
    }