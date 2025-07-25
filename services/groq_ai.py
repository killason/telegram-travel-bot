import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1", 
)

def get_ai_response(prompt: str) -> str:
    """
    Получает ответ от AI на основе входного текста (prompt).
    """
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Ты помощник по досугу в городе. Помогаешь с идеями по погоде и настроению."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Ошибка Groq:", e)
        return "Произошла ошибка при обращении к AI."
    