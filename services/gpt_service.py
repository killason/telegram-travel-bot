import os
import openai
from datetime import datetime  

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_ai_advice(city: str, condition: str, temp_c: float, user_name: str) -> str:
    """Получает совет от AI о том, чем заняться в городе с учетом погоды и времени суток."""

    now = datetime.now()

    # Время суток
    hour = now.hour
    if 5 <= hour < 12:
        time_of_day = "утро"
    elif 12 <= hour < 17:
        time_of_day = "день"
    elif 17 <= hour < 21:
        time_of_day = "вечер"
    else:
        time_of_day = "ночь"

    # День недели
    weekday = now.weekday()
    day_type = "выходной" if weekday >= 5 else "будний день"

    prompt = (
        f"Ты — дружелюбный помощник по досугу. Отвечаешь на русском языке.\n"
        f"Пользователя зовут {user_name}.\n"
        f"Сейчас пользователь находится в городе {city}.\n"
        f"Погода: {condition}, температура: {temp_c}°C.\n"
        f"Время суток: {time_of_day}, день недели: {day_type}.\n"
        f"Предложи 1-2 интересных и полезных идеи, чем заняться, исходя из этих условий."
        f"Ответ должен быть кратким, живым и неформальным, с эмодзи, подходящими к каждому совету. "
        f"Давай реальные советы связанные с реальными местами и достопримечательностями в этом городе.\n"
    )

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка при получении совета: {e}"
    