from peewee import (
    Model,
    CharField,
    FloatField,
    DateTimeField,
    IntegerField,
    TextField,
    AutoField,
)
from playhouse.sqlite_ext import SqliteExtDatabase
from datetime import datetime

# Подключение к БД
db = SqliteExtDatabase("bot_data.db")


# Базовая модель
class BaseModel(Model):
    class Meta:
        database = db


# Избранные места
class FavoritePlace(BaseModel):
    user_id = IntegerField(index=True)  # ID пользователя
    place_id = CharField()  # ID места в Google Places
    name = CharField()  # название места
    address = CharField()  # адрес места
    place_type = CharField()  # тип места (еда, отель и т.д.)
    link = CharField()  # ссылка на место
    photo_url = CharField(null=True)  # URL фото места
    created_at = DateTimeField(default=datetime.now)  # дата добавления в избранное

    class Meta:
        indexes = (
            (
                ("user_id", "place_id"),
                False,
            ),  # ускорение выборок/антидублей по месту у юзера
        )


# История действий пользователя
class UserHistory(BaseModel):
    id = AutoField()  # автоинкрементный ID
    user_id = IntegerField(index=True)  # ID пользователя
    action = CharField()  # 'city_set' | 'view_place' | 'add_favorite'
    message = TextField(null=True)  # текст сообщения
    city = CharField(null=True)  # город, если применимо
    lat = FloatField(null=True)  # широта
    lon = FloatField(null=True)  # долгота
    tag = CharField(null=True, index=True)  # тег действия, если есть
    weather = CharField(null=True)  # кратко: "Ясно, +24°C"
    place_type = CharField(null=True)  # тип места
    name = CharField(null=True)  # название места
    address = CharField(null=True)  # адрес места
    link = TextField(null=True)  # ссылка на место
    data_json = TextField(null=True)  # JSON с дополнительными данными
    created_at = DateTimeField(
        default=datetime.utcnow, index=True
    )  # дата добавления в избранное

    class Meta:
        indexes = (
            (("user_id", "tag", "created_at"), False),  # быстрые выборки состояния/кэша
        )
