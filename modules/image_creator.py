from PIL import Image, ImageDraw, ImageFont
import os


def flatten_list(nflist):
    result_list = []

    def _recursive(_list):
        if not isinstance(_list, list):
            result_list.append(_list)
        else:
            for item in _list:
                _recursive(item)

    _recursive(nflist)
    return result_list


def split_text_into_rows(count, text):
    if len(text) <= count:
        return [text]
    else:
        offset = text[:count].rfind(' ')
        return [text[:offset], split_text_into_rows(count, text[offset + 1:])]


def create(text):
    PADDING = 20
    FONT_SIZE = 26
    SYM_IN_ROW = 43
    IMAGE_WIDTH = 650
    LINE_HEIGTH = 30

    base_path = os.path.dirname(__file__)
    font_path = os.path.join(base_path, '../assets/Lora-Regular.ttf')
    bg_path = os.path.join(base_path, '../assets/bg.png')
    head_path = os.path.join(base_path, '../assets/header.png')

    text = text.split('\n')
    text_rows = []
    for i in range(0, len(text)):
        text_rows.append(split_text_into_rows(SYM_IN_ROW, text[i]))

    text_rows = flatten_list(text_rows)
    IMAGE_HEIGHT = len(text_rows)*LINE_HEIGTH + PADDING

    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0))
    drawer = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, FONT_SIZE)
    bg_img = Image.open(bg_path)

    bg__x, bg__y = 0, 0
    bg_size = bg_img.size

    while True:
        if bg__x >= img.size[0]:
            bg__x = 0
            bg__y += bg_size[0]
        if bg__y >= img.size[1]:
            break
        img.paste(bg_img, (bg__x, bg__y))
        bg__x += bg_size[0]

    for index in range(len(text_rows)):
        x = LINE_HEIGTH * index + PADDING
        y = PADDING
        drawer.text((y, x), text_rows[index], font=font, fill=(54, 40, 29))

    image_path = os.path.join(base_path, '../img/post.png')
    img.save(image_path)
    return image_path
