from PIL import Image, ImageDraw, ImageFont
from settings import get_data_dir, get_base_dir
from models.models import Game
import sys
from pathlib import Path
import aggdraw

proj_dir = get_data_dir()

data_dir = get_base_dir()


class TennisDraw:
    def __init__(self, data: Game = None):
        self.data = data

    def draw_all(self, path=data_dir / "static" / "score_empty.png"):
        image = Image.open(path).convert("RGBA")

        if self.data.is_clear or not self.data.is_visible:
            image.putalpha(0)

        else:

            font_size = 35
            font_path_bd = data_dir / "static" / "arialbd.ttf"
            font_path = data_dir / "static" / "arial.ttf"
            font_bd = ImageFont.truetype(str(font_path_bd), size=font_size)
            font = ImageFont.truetype(str(font_path), size=font_size)
            pencil = ImageDraw.Draw(image)
            y1, y2 = 25, 110
            pixel_color = image.getpixel((430, 10))
            match self.data.server:
                case None | 0:
                    pass

                case 1:

                    canvas = aggdraw.Draw(image)
                    pen = aggdraw.Pen("white", 0)
                    brush = aggdraw.Brush(pixel_color) #(162, 39, 166)
                    cords = [380, 30, 380, 53, 400, 42.5]
                    canvas.polygon(cords, pen, brush)

                    canvas.flush()
                case 2:
                    canvas = aggdraw.Draw(image)
                    pen = aggdraw.Pen("white", 0)
                    brush = aggdraw.Brush(pixel_color)
                    cords = [380, 115, 380, 138, 400, 127.5]

                    canvas.polygon(cords, pen, brush)

                    canvas.flush()

                    # pencil.polygon([(380, 25), (380, 60), (410, 42.5)], fill=(162, 39, 166))
            player_name_1 = self.data.first_player.upper()
            player_name_2 = self.data.second_player.upper()

            # pencil.text((10, 25), player_name_1, font=font_bd, fill=(162, 39, 166))
            # pencil.text((10, 110), player_name_2, font=font_bd, fill=(162, 39, 166))

            bbox1 = font.getbbox(player_name_1)
            bbox2 = font.getbbox(player_name_2)

            width_1 = bbox1[2] - bbox1[0]
            width_2 = bbox2[2] - bbox2[0]

            max_width = max(width_1, width_2)


            if max_width <= 360:
                pencil.text((10, 25), player_name_1, font=font, fill=pixel_color)
                pencil.text((10, 110), player_name_2, font=font, fill=pixel_color)

            else:
                current_font_size = int(((370 / max_width) * font_size))
                correct_font = ImageFont.truetype(str(font_path), size=current_font_size)
                pencil.text((10, 42.5), player_name_1, anchor="lm", font=correct_font, fill=pixel_color)
                pencil.text((10, 127.5), player_name_2, anchor="lm", font=correct_font, fill=pixel_color)


            cords_first = [(670, y1), (680, y1)][(len(self.data.first_point) == 1)]
            cords_second = [(670, y2), (680, y2)][(len(self.data.second_point) == 1)]

            pencil.text((690, 42.5), self.data.first_point.upper(), font=font_bd, anchor='mm', fill=pixel_color)
            pencil.text((690, 127.5), self.data.second_point.upper(), font=font_bd, anchor='mm', fill=pixel_color)

            pencil.text((440, y1), str(self.data.first_game_3), font=font_bd, fill=(255, 255, 255))
            pencil.text((520, y1), str(self.data.first_game_2), font=font_bd, fill=(255, 255, 255))
            pencil.text((600, y1), str(self.data.first_game_1), font=font_bd, fill=(255, 255, 255))
            pencil.text((440, y2), str(self.data.second_game_3), font=font_bd, fill=(255, 255, 255))
            pencil.text((520, y2), str(self.data.second_game_2), font=font_bd, fill=(255, 255, 255))
            pencil.text((600, y2), str(self.data.second_game_1), font=font_bd, fill=(255, 255, 255))


            image.putalpha(255)


        return image
        # if path is None:
        #     if getattr(sys, 'frozen', False):
        #         dir_out = Path(sys.executable).parent / "media"
        #     else:
        #         dir_out = proj_dir / "media"
        #     dir_out.mkdir(exist_ok=True)
        #     path = dir_out / "tennis_score.png"
        #
        # image.save(path, format="PNG")
        # image.close()