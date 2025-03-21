from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# Занесение данных задания в клавиатуру
async def get_keyboard(state, question_id, task):
    
    keyboard = VkKeyboard()
    # Начало сценария
    if state == "begin":
        keyboard.add_button("Начать")
    if state == "Начать":
        keyboard.add_button("Задание дня")
        keyboard.add_line()
        keyboard.add_openlink_button(label='\"Другое дело\"', link="https://vk.com/app7785085")
        keyboard.add_line()
        keyboard.add_button("Правила")

    # Правила
    if state == "Правила":
        keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

    # Задание дня - тест
    if state == "multitest" and task["type"] == "multitest":
        for answer_id in range(len(task["answers"][question_id])):
            keyboard.add_button(task["answers"][question_id][answer_id])
            if answer_id != len(task["answers"][question_id])-1:
                keyboard.add_line()
    
    # Задание дня - опрос
    elif state == "quiz" and task["type"] == "quiz":
        for answer_id in range(len(task["answers"][question_id])):
            keyboard.add_button(task["answers"][question_id][answer_id])
            if answer_id != len(task["answers"][question_id])-1:
                keyboard.add_line()
    
    # Задание завершено
    elif state == "finished":
        keyboard.add_openlink_button(label='Забрать баллы', link="https://vk.com/app7785085")

    # Кнопка назад, если сценарий не в начале:
    if (state not in ["Начать", "begin", "Правила"]):
        keyboard.add_line()
        keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

    return keyboard