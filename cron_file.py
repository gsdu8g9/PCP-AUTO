from modules import image_creator
from db.data_provider import DataProvider


def main():
    db = DataProvider()
    if not db.check_posts_in_base():
        from modules import parser
        parser.parse()

    text = db.get_post_text()
    image_creator.create(text)

    db.close_conn()


if __name__ == '__main__':
    main()
