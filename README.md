# Гид по досугу и развлечениям — Telegram Bot

Интеллектуальный Telegram-бот, который помогает пользователю организовать досуг в городе:  
- показывает актуальную погоду  
- предлагает варианты досуга и активностей 
- находит рестораны, кафе, музеи и другие места 
- сохраняет историю и избранное  

---

## Возможности
- Определение местоположения (по геолокации или введённому городу)
- Получение прогноза погоды (WeatherAPI)
- Поиск мест через Google Places API
- Советы по досугу с помощью AI (Groq LLaMA 3 через OpenAI SDK)
- Сохранение истории советов и избранных мест в базе SQLite
- Управление через удобные inline-кнопки (Подробнее, Далее, Назад, Добавить в избранное)

---

## Стек технологий
- **Python** ≥ 3.10 (рекомендуется 3.11)
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) — работа с Telegram Bot API
- [Requests](https://docs.python-requests.org/) — HTTP-запросы
- [Peewee ORM](http://docs.peewee-orm.com/) — база данных SQLite
- [python-dotenv](https://pypi.org/project/python-dotenv/) — загрузка переменных окружения
- [OpenAI SDK](https://pypi.org/project/openai/) — доступ к Groq (модель LLaMA 3)

---

## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone <repo-url>
cd TelegramBot
```

### 2. Создайте виртуальное окружение
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3. Установите зависимости
```bash
pip install -r requirements.txt
```

### 4. Настройте переменные окружения
Скопируйте шаблон `.env`:
```bash
cp .env.template .env
```

Заполните поля в `.env`:
```ini
BOT_TOKEN=ваш_токен_бота
WEATHER_API_KEY=ваш_api_ключ_WeatherAPI
GOOGLE_API_KEY=ваш_api_ключ_Google
GROQ_API_KEY=ваш_api_ключ_Groq
```

### 5. Подготовьте базу данных
```bash
cd database
python db_init.py
cd ..
```

### 6. Запустите бота
```bash
python main.py
```

Бот будет работать в режиме **polling** (бесконечный цикл опроса Telegram).

---

## Команды
- `/start` — начало работы, выбор местоположения
- `/help` — справка

---

## Структура проекта
```
TelegramBot/
  config_data/        # конфигурация (.env и настройки)
  database/           # ORM Peewee, миграции и инициализация SQLite
  handlers/           # обработчики команд и колбэков
  keyboards/          # inline-кнопки и клавиатуры
  services/           # модули интеграций (погода, Google Places, AI)
  utils/              # вспомогательные функции (user_context, команды)
  loader.py           # инициализация TeleBot и state storage
  main.py             # точка входа (polling)
  requirements.txt    # зависимости
  .env.template       # шаблон переменных окружения
  README.md           # документация
```

---

## Переменные окружения
- `BOT_TOKEN` — токен Telegram-бота (от @BotFather)
- `WEATHER_API_KEY` — ключ [WeatherAPI](https://www.weatherapi.com/)
- `GOOGLE_API_KEY` — ключ Google (Geocoding + Places API)
- `GROQ_API_KEY` — ключ [Groq](https://console.groq.com/keys)

---

## База данных
- Используется SQLite (файл `bot_data.db`)
- ORM: Peewee
- Основные таблицы:
  - `UserHistory` — история действий
  - `Favorites` — избранное пользователя

---

## AI-интеграция
Используется [OpenAI SDK](https://github.com/openai/openai-python) с кастомным `base_url=https://api.groq.com/openai/v1` для работы с моделью `llama3-70b-8192`.

Пример вызова:
```python
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
```

---

## TODO / Roadmap
- [ ] Добавить удаление избранного (выборочно)
- [ ] Добавить мультиязычность
- [ ] Расширить поддержку API (отели, маршруты)
- [ ] Расширить поиск мест по ключевым словам
- [ ] Добавить сортировку мест (по рейтингу, расстоянию)

---

## Лицензия
MIT License
Copyright (c) 2025 Владимир Успенский (Skillbox Final Project)