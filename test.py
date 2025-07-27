#from services.weather_service import get_weather
from services.advice_service import get_ai_advice

# lat, lon = 41.7151, 44.8271  # Тбилиси
# print(get_weather(lat, lon))

print(get_ai_advice("Тбилиси", "обдачно", 31.5))