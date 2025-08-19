from typing import Any

user_context: dict[int, dict[str, Any]] = {}

def set_context(user_id: int, **kwargs) -> None:
    """
    Устанавливает или обновляет контекст пользователя.
    """
    if user_id not in user_context:
        user_context[user_id] = {}
    user_context[user_id].update(kwargs)

def get_context(user_id: int) -> dict[str, Any]:
    """Получает контекст пользователя."""
    return user_context.get(user_id, {})

def update_offset(user_id: int, offset: int):
    """Обновляет смещение для пользователя."""

    if user_id in user_context:
        user_context[user_id]["offset"] = offset

def clear_context(user_id: int):
    """Очищает контекст пользователя."""
    if user_id in user_context:
        user_context.pop(user_id)
