from PIL import Image, ImageDraw, ImageFont
import os


def flatten_list(nflist):
    result_list = []

    def _recursive(_list):
        if not isinstance(_list, list):
            result_list.append(_list)
        else:
            for item in _list:
                _recursive(item.split('\n'))

    _recursive(nflist)
    return result_list


def split_text_into_rows(count, text):
    if len(text) <= count:
        return [text]
    else:
        last_space_position = text[:count].rfind(' ')
        return flatten_list([text[:last_space_position], split_text_into_rows(count, text[count:])])


def create(text):
    PADDING = 20
    FONT_SIZE = 28
    SYM_IN_ROW = 30
    IMAGE_WIDTH = 640

    base_path = os.path.dirname(__file__)
    font_path = os.path.join(base_path, 'assets/Lora-Regular.ttf')

    text_rows = split_text_into_rows(SYM_IN_ROW, text)
    IMAGE_HEIGHT = len(text_rows) + PADDING * 2

    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0))
    drawer = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, FONT_SIZE)

    for index in range(len(text_rows)):
        x = FONT_SIZE * 1 + PADDING
        y = PADDING
        drawer.text((x, y), text_rows[index], font=font)

    image_path = os.path.join(base_path, 'img/post.png')
    img.save(image_path)
