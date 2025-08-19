from datetime import datetime
from peewee import fn
from database.models import UserHistory

RU_MONTHS = {
    1:"Январь",2:"Февраль",3:"Март",4:"Апрель",5:"Май",6:"Июнь",
    7:"Июль",8:"Август",9:"Сентябрь",10:"Октябрь",11:"Ноябрь",12:"Декабрь"
}

def save_city_set(user_id: int, city: str, weather_text: str|None):
    UserHistory.create(
        user_id=user_id, action="city_set", city=city, weather=weather_text or "", created_at=datetime.utcnow()
    )

def save_view_place(user_id: int, place_type: str, name: str, address: str, link: str):
    UserHistory.create(
        user_id=user_id, action="view_place", place_type=place_type, name=name, address=address, link=link,
        created_at=datetime.utcnow()
    )

def save_add_favorite(user_id: int, place_type: str, name: str, address: str, link: str):
    UserHistory.create(
        user_id=user_id, action="add_favorite", place_type=place_type, name=name, address=address, link=link,
        created_at=datetime.utcnow()
    )

def get_months_with_data(user_id: int):
    """
    Возвращает список кортежей (year:int, month:int, count:int) по которым есть записи.
    """
    q = (UserHistory
         .select(fn.strftime('%Y', UserHistory.created_at).alias('y'),
                 fn.strftime('%m', UserHistory.created_at).alias('m'),
                 fn.COUNT(UserHistory.id).alias('cnt'))
         .where(UserHistory.user_id == user_id)
         .group_by('y', 'm')
         .order_by(fn.strftime('%Y-%m', UserHistory.created_at).desc()))
    months = []
    for row in q.dicts():
        year = int(row['y'])
        month = int(row['m'])
        cnt = row['cnt']
        months.append((year, month, cnt))
    return months

def get_history_by_month(user_id: int, year: int, month: int, limit: int = 50):
    """
    Возвращает записи за конкретный месяц.
    """
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year+1, 1, 1)
    else:
        end = datetime(year, month+1, 1)

    q = (UserHistory
         .select()
         .where((UserHistory.user_id == user_id) &
                (UserHistory.created_at >= start) &
                (UserHistory.created_at < end))
         .order_by(UserHistory.created_at.desc())
         .limit(limit))
    return list(q)

def delete_history_by_month(user_id: int, year: int, month: int):
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year+1, 1, 1)
    else:
        end = datetime(year, month+1, 1)
    (UserHistory
     .delete()
     .where((UserHistory.user_id == user_id) &
            (UserHistory.created_at >= start) &
            (UserHistory.created_at < end))
     .execute())
