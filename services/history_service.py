from datetime import datetime
from typing import Optional, Tuple, List, Dict
import json
from peewee import fn
from database.models import db, UserHistory

RU_MONTHS = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

ALLOWED_ACTIONS = ("city_set", "view_place", "add_favorite")


def _norm_place_type(t: Optional[str]) -> str:
    return (t or "all").strip().lower()


def _cache_tag(place_type: Optional[str]) -> str:
    return f"places_cache:{_norm_place_type(place_type)}"


def save_city_set(
    user_id: int, city: str, lat: float, lon: float, weather: Optional[str] = None
) -> None:
    """
    Логируем установку города (как раньше) + обновляем служебную запись current_city.
    Погоду сохраняем в поле 'weather' без изменения формата message.
    """
    now = datetime.utcnow()
    with db.atomic():

        UserHistory.create(
            user_id=user_id,
            action="city_set",
            message=f"Город установлен: {city}",
            city=city,
            lat=lat,
            lon=lon,
            weather=weather,
            tag=None,
            data_json=None,
            created_at=now,
        )

        row = (
            UserHistory.select()
            .where(
                (UserHistory.user_id == user_id) & (UserHistory.tag == "current_city")
            )
            .order_by(UserHistory.created_at.desc())
            .first()
        )

        if row:
            row.city = city
            row.lat = lat
            row.lon = lon
            if weather is not None:
                row.weather = weather
            row.message = "Текущий город установлен"
            row.created_at = now
            row.save()
        else:
            UserHistory.create(
                user_id=user_id,
                action="state",
                message="Текущий город установлен",
                city=city,
                lat=lat,
                lon=lon,
                weather=weather,
                tag="current_city",
                data_json=None,
                created_at=now,
            )


def get_current_coords(user_id: int) -> Optional[Tuple[str, float, float]]:
    """
    Возвращает (city, lat, lon) из последней записи current_city или None
    """
    row = (
        UserHistory.select()
        .where((UserHistory.user_id == user_id) & (UserHistory.tag == "current_city"))
        .order_by(UserHistory.created_at.desc())
        .first()
    )
    if not row or row.lat is None or row.lon is None:
        return None
    return (row.city or "", float(row.lat), float(row.lon))


def get_cached_places(
    user_id: int, place_type: Optional[str] = None
) -> Optional[List[Dict]]:
    """
    Возвращает список мест для последних координат (из current_city), если кэш есть.
    Кэш валиден до смены города (координат).
    """
    # Берём точные lat/lon из последней записи current_city,
    # чтобы сравнение по БД было без погрешностей
    cur = (
        UserHistory.select()
        .where((UserHistory.user_id == user_id) & (UserHistory.tag == "current_city"))
        .order_by(UserHistory.created_at.desc())
        .first()
    )
    if not cur or cur.lat is None or cur.lon is None:
        return None

    row = (
        UserHistory.select()
        .where(
            (UserHistory.user_id == user_id)
            & (UserHistory.tag == _cache_tag(place_type))
            & (UserHistory.lat == cur.lat)
            & (UserHistory.lon == cur.lon)
        )
        .order_by(UserHistory.created_at.desc())
        .first()
    )
    if not row or not row.data_json:
        return None
    try:
        return json.loads(row.data_json)
    except Exception:
        return None


def get_cached_place_by_id(user_id: int, place_id: str) -> Optional[Dict]:
    """
    Ищет место по place_id среди ВСЕХ кэшей категорий для текущих координат.
    Возвращает dict места или None.
    """
    # берём текущие координаты
    cur = (
        UserHistory.select()
        .where((UserHistory.user_id == user_id) & (UserHistory.tag == "current_city"))
        .order_by(UserHistory.created_at.desc())
        .first()
    )
    if not cur or cur.lat is None or cur.lon is None:
        return None

    # пробегаем все записи кэша для этих координат
    rows = (
        UserHistory.select()
        .where(
            (UserHistory.user_id == user_id)
            & (UserHistory.lat == cur.lat)
            & (UserHistory.lon == cur.lon)
            & (UserHistory.tag.startswith("places_cache"))
        )
        .order_by(UserHistory.created_at.desc())
    )

    pid = str(place_id)
    for r in rows:
        if not r.data_json:
            continue
        try:
            lst = json.loads(r.data_json) or []
        except Exception:
            continue
        for p in lst:
            if str(p.get("place_id")) == pid:
                return p
    return None


def set_cached_places(
    user_id: int, places: List[Dict], place_type: Optional[str] = None
) -> None:
    """
    Сохраняет кэш для актуальных координат (из current_city).
    Запись служебная: action='state', tag='places_cache', без влияния на «Историю за месяц».
    """
    cur = (
        UserHistory.select()
        .where((UserHistory.user_id == user_id) & (UserHistory.tag == "current_city"))
        .order_by(UserHistory.created_at.desc())
        .first()
    )
    if not cur or cur.lat is None or cur.lon is None:
        return

    with db.atomic():
        UserHistory.create(
            user_id=user_id,
            action="state",
            message=None,
            city=cur.city,
            lat=cur.lat,
            lon=cur.lon,
            tag=_cache_tag(place_type),
            data_json=json.dumps(places, ensure_ascii=False),
            created_at=datetime.utcnow(),
        )


def save_view_place(user_id: int, place_type: str, name: str, address: str, link: str):
    """
    Логируем просмотр места.
    """
    UserHistory.create(
        user_id=user_id,
        action="view_place",
        place_type=place_type,
        name=name,
        address=address,
        link=link,
        created_at=datetime.utcnow(),
    )


def save_add_favorite(
    user_id: int, place_type: str, name: str, address: str, link: str
):
    """
    Логируем добавление места в избранное.
    """
    UserHistory.create(
        user_id=user_id,
        action="add_favorite",
        place_type=place_type,
        name=name,
        address=address,
        link=link,
        created_at=datetime.utcnow(),
    )


def get_months_with_data(user_id: int):
    """
    Возвращает список кортежей (year:int, month:int, count:int) по которым есть записи.
    """
    q = (
        UserHistory.select(
            fn.strftime("%Y", UserHistory.created_at).alias("y"),
            fn.strftime("%m", UserHistory.created_at).alias("m"),
            fn.COUNT(UserHistory.id).alias("cnt"),
        )
        .where(
            (UserHistory.user_id == user_id)
            & (UserHistory.action.in_(ALLOWED_ACTIONS))
            & (UserHistory.action != "state")
        )
        .group_by("y", "m")
        .order_by(fn.strftime("%Y-%m", UserHistory.created_at).desc())
    )
    months = []
    for row in q.dicts():
        year = int(row["y"])
        month = int(row["m"])
        cnt = row["cnt"]
        months.append((year, month, cnt))
    return months


def get_history_by_month(user_id: int, year: int, month: int, limit: int = 50):
    """
    Возвращает записи за конкретный месяц.
    """
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    q = (
        UserHistory.select()
        .where(
            (UserHistory.user_id == user_id)
            & (UserHistory.created_at >= start)
            & (UserHistory.created_at < end)
            & (UserHistory.tag.is_null(True))
            & (UserHistory.action != "state")
        )
        .order_by(UserHistory.created_at.desc())
        .limit(limit)
    )
    return list(q)


def delete_history_by_month(user_id: int, year: int, month: int):
    """
    Удаляет записи за конкретный месяц.
    """
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    (
        UserHistory.delete()
        .where(
            (UserHistory.user_id == user_id)
            & (UserHistory.created_at >= start)
            & (UserHistory.created_at < end)
        )
        .execute()
    )
