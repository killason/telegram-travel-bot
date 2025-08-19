from peewee import (
    Model, CharField, FloatField, DateTimeField,
    IntegerField, TextField
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
    user_id = IntegerField()
    place_id = CharField()
    name = CharField()
    address = CharField()
    place_type = CharField()
    link = CharField()
    photo_url = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)

# История действий пользователя
class UserHistory(BaseModel):
    user_id = IntegerField()
    action = CharField()          # 'city_set' | 'view_place' | 'add_favorite'
    city = CharField(null=True)
    weather = CharField(null=True) # кратко: "Ясно, +24°C"
    place_type = CharField(null=True) # тип места
    name = CharField(null=True) # название места
    address = CharField(null=True)
    link = TextField(null=True)
    created_at = DateTimeField(default=datetime.utcnow)
