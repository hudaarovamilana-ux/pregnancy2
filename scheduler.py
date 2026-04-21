import asyncio
from datetime import datetime, timedelta
from database import get_users_for_notification, update_last_notification, get_user
from bot import bot, show_week_info  # Импортируем бота и функцию показа недели
from weeks_data import WEEKS_INFO

async def check_week_updates():
    """Проверяет, не наступила ли новая неделя у пользователей"""
    while True:
        try:
            # Получаем пользователей для уведомления
            users = get_users_for_notification()
            
            for user_id, current_week, last_notification in users:
                try:
                    # Отправляем уведомление
                    await bot.send_message(
                        user_id,
                        f"🌸 Новая неделя! 🌸\n\n"
                        f"Поздравляю! У тебя началась {current_week} неделя беременности!\n"
                        f"👇 Смотри что нового:"
                    )
                    
                    # Показываем информацию о новой неделе
                    # Нам нужно создать fake message или вызвать функцию по-другому
                    # Проще отправить информацию напрямую
                    week_data = WEEKS_INFO.get(current_week, {})
                    
                    text = f"🌸 **{current_week} неделя беременности**\n\n"
                    if week_data.get('fruit'):
                        text += f"🍎 Размер плода: {week_data['fruit']}\n\n"
                    if week_data.get('description'):
                        text += f"{week_data['description']}\n\n"
                    if week_data.get('mom_feeling'):
                        text += f"🤰 **Ощущения мамы:**\n{week_data['mom_feeling']}\n\n"
                    
                    await bot.send_message(user_id, text, parse_mode="Markdown")
                    
                    if week_data.get('fact'):
                        await bot.send_message(
                            user_id,
                            f"✨ **Интересный факт:**\n{week_data['fact']}",
                            parse_mode="Markdown"
                        )
                    
                    # Обновляем последнее уведомление
                    update_last_notification(user_id, current_week)
                    
                except Exception as e:
                    print(f"Ошибка при отправке пользователю {user_id}: {e}")
            
            # Проверяем каждый час
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"Ошибка в планировщике: {e}")
            await asyncio.sleep(60)

async def on_startup():
    """Запускается при старте бота"""
    asyncio.create_task(check_week_updates())
    print("✅ Планировщик уведомлений запущен")