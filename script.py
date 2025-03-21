import json
from authorize import get_task_id
from data_base import new_user

# Реагирование на сообщение
async def script(state, attachments, question_id, message, sender, task):
    # Сегодняшнее задание
    task_id = await get_task_id(sender)
    with open("tasks.json", "r", encoding="utf-8") as f:
        task = json.load(f)["tasks"][task_id]

    # Начать сценария
    if (((state == "begin" or state == "Начать") and message == "Начать")
            or ((state != "begin" or state != "Начать") and message == "Назад")):
        state = "Начать"
        await new_user(sender)
        return ["Привет! Выбери задание на сегодня или зайди в приложение \"Другое дело\"!", state, 0]
    
    # Нажата кнопка "Правила"
    elif (state == "Начать" and message == "Правила"):
        state = "Правила"
        return ["Летний марафон ITeamSpirit - развлекательный, но при этом познавательный марафон, " +
            "в котором каждый день пользователь получает короткое задание, после прохождения которого " +
            "он получает ссылку для получения баллов в мини-приложении Другое Дело в ВК. При этом задания " +
            "проходить дважды нельзя, нужно дождаться следующего дня. Тематика заданий разная, но все они " +
            "как-то связаны с летом.\n\nЧтобы получить максимальное количество баллов заходи в бот каждый " +
            "день, поскольку пропущенные задания пройти ты уже не сможешь. Это не займет много времени, но " +
            "зато за это время ты узнаешь что-то новое и заработаешь баллы.", state, 0]
    
    # Нажата кнопка "Задание дня"
    elif (state == "Начать" and message == "Задание дня"):
        state = task["type"]
        # Занесение данных задания в сценарий
        if task["type"] == "multitest":
            return [task["content"] + "\n" + task["questions"][0], state, 0]
        if task["type"] == "quiz":
            return [task["content"] + "\n" + task["questions"][0], state, 0]
        if task["type"] == "word":
            return [task["content"] + "\n" + task["question"], state, 0]
        elif task["type"] == "photo":
            return [task["content"], state, 0]
    
    # Задание дня - тест
    elif (state == "multitest" and message in task["answers"][question_id]):
        # Занесение данных задания в сценарий
        if task["answers"][question_id].index(message) == task["right"][question_id]:
            question_id += 1
            if (question_id == len(task["questions"])):
                state = "finished"
                return ["Верно! Поздравляю с прохождением теста! Забирай награду в приложении", state, question_id]
            return ["Верно! идем дальше:" + "\n" + task["questions"][question_id], state, question_id]
        else:
            question_id = 0
            return ["Неверно! начнем сначала:" + "\n" + task["questions"][question_id], state, question_id]
        
    # Задание дня - опрос
    elif (state == "quiz" and message in task["answers"][question_id]):
        # Занесение данных задания в сценарий
        question_id += 1
        if (question_id == len(task["questions"])):
            state = "finished"
            return ["Спасибо за прохождение опроса! Забирай награду в приложении" +
                    "\n" + "А пока лови интересную информацию: " + task["dop_content"], state, question_id]
        return ["Идем дальше: " + "\n" + task["questions"][question_id], state, question_id]
    
    # Задание дня - Отдагать слово
    elif (state == "word"):
        # Занесение данных задания в сценарий
        if (message.lower() in task["answers"]):
            state = "finished"
            return ["Ты угадал слово! Забирай награду в приложении" +
                    "\n" + "А пока лови интересную информацию: " + task["dop_content"], state, question_id]
        return ["Неверно! попробуй еще раз", state, question_id]
        
    # Задание дня - фото
    elif (state == "photo"):
        if ("photo" in attachments.values()):
            state = "finished"
            return ["Фото отправлено! Получай баллы за задание!", state, question_id]
        else:
            return ["Чтобы выполнить задание, пришли фото!", state, question_id]
    else:
        return ["Я не знаю такой команды", state, 0]
