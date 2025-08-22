from models import db, FavoritePlace, UserHistory


def db_init():
    db.connect()
    db.create_tables([FavoritePlace, UserHistory])
    db.close()


if __name__ == "__main__":
    db_init()
