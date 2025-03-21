from vk_api.longpoll import VkEventType
from vk_api.utils import get_random_id
from keyboard import get_keyboard
from authorize import authorize, longpoll, get_task_id
from script import script
import asyncio
import json
from image import upload_photo

# Функция отправки сообщения
async def write_message(sender, message, bot_attachment, keyboard):
    # Обращение к API
    authorize.method("messages.send", {"user_id": sender, "attachment": bot_attachment, "message": message, "random_id": get_random_id(), "keyboard": keyboard})

# Бесконечный цикл
async def loop():
    # Этап в сценарии
    state = "begin"
    question_id = 0

    # Прослушка на новое сообщение, содержит ли оно информацию
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            # event.text - отправленное сообщение
            # event.user_id - айди пользователя
            message = event.text
            sender = event.user_id
            inputs = event.attachments

            # Сегодняшнее задание
            task_id = await get_task_id(sender)
            with open("tasks.json", "r", encoding="utf-8") as f:
                task = json.load(f)["tasks"][task_id]

            # Продвижение бота по сценарию
            bot_message, state, question_id = await script(state, inputs, question_id, message, sender, task)
            
            # Занесение данных задания в клавиатуру
            keyboard = await get_keyboard(state, question_id, task)

            # Выборка картинки
            if (state != "Начать" and state != "finished"):
                photo_path = f'images\{state}\{task_id}{question_id}.jpg'
            else:
                photo_path = f'images\{state}\img.jpg'
            bot_attachment = upload_photo(photo_path)

            # Отправка сообщения
            await write_message(sender, bot_message, bot_attachment, keyboard.get_keyboard())

asyncio.run(loop())