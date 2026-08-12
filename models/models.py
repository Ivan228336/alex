from pydantic import BaseModel


class Game(BaseModel):
    first_player: str | None = ''
    second_player: str | None = ''
    first_point: str | None = ''
    second_point: str | None = ''
    first_game_1: int | None = 0
    first_game_2: int | None = 0
    first_game_3: int | None = 0
    second_game_1: int | None = 0
    second_game_2: int | None = 0
    second_game_3: int | None = 0
    server: int | None = 0
    is_visible: bool | None = True

    @property
    def is_clear(self):
        return not (self.first_player or self.second_player)