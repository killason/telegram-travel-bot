from services.weather_service import get_weather

lat, lon = 41.7151, 44.8271  # Тбилиси
print(get_weather(lat, lon))