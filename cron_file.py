from modules import image_creator
from db.data_provider import DataProvider
from modules import ok_api
import os


def main():
    db = DataProvider()
    if not db.check_posts_in_base():
        from modules import parser
        parser.parse()

    text = db.get_post_text()
    base_path = os.path.dirname(__file__)
    img_folder_path = os.path.join(base_path, 'img')
    img_listdir = os.listdir(img_folder_path)
    if len(img_listdir) == 0:
        image_path = image_creator.create(text)
    else:
        image_path = os.path.join(img_folder_path, img_listdir[0])

    post_result = ok_api.post(image_path)
    if post_result:
        os.remove(image_path)
        db.mark_posted()
    db.close_conn()


if __name__ == '__main__':
    main()
