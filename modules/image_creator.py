from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import random


watermark_colors = [
    (2, 106, 57),
    (189, 63, 41),
    (61, 40, 23),
    (102, 68, 125),
    (38, 40, 61)
]


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


def add_watermark(image, watermark, opacity=1, wm_interval=0):
    assert opacity >= 0 and opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    for y in range(0, image.size[1], watermark.size[1]+wm_interval):
        for x in range(0, image.size[0], watermark.size[0]+wm_interval):
            layer.paste(watermark, (x, y))
    return Image.composite(layer,  image,  layer)


def create(text):
    PADDING = 20
    FONT_SIZE = 26
    SYM_IN_ROW = 43
    IMAGE_WIDTH = 650
    LINE_HEIGTH = 30

    base_path = os.path.dirname(__file__)
    font_path = os.path.join(base_path, '../assets/Lora-Regular.ttf')
    bg_path = os.path.join(base_path, '../assets/bg2.png')

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

    color = watermark_colors[random.randint(0, len(watermark_colors))]
    water = Image.new('RGB', (10, 10), color=color)
    image_path = os.path.join(base_path, '../img/post{}.png'.format(color[0]))
    final_img = add_watermark(img, water, opacity=0.5)
    fdrawer = ImageDraw.Draw(final_img)
    for index in range(len(text_rows)):
        x = LINE_HEIGTH * index + PADDING
        y = PADDING
        fdrawer.text((y, x), text_rows[index], font=font, fill=(255, 255, 255))
    final_img.save(image_path)
    return image_path
