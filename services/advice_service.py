import os
import openai  # если используешь OpenAI
# from groq import Groq  # если Groq (вставим позже, если нужно)

openai.api_key = os.getenv("GROQ_API_KEY")

def get_ai_advice(city: str, condition: str, temp_c: float) -> str:
    prompt = (
        f"Ты — дружелюбный помощник по досугу.\n"
        f"Сейчас пользователь находится в городе {city}.\n"
        f"Погода: {condition}, температура: {temp_c}°C.\n"
        f"Предложи 1-2 интересных и полезных идеи, чем заняться, исходя из этих условий. "
        f"Избегай банальных фраз. Пиши кратко и интересно."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Ошибка при получении совета: {e}"