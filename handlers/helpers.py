from aiogram import types
import pandas as pd


def today_tomorrow_keyboard():
    """
    Кнопки для получения расписания на сегодня или завтра.
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра", "/help"]]
    )
    return keyboard


def schedule_string(schedule: pd.DataFrame):
    """
    Строка с расписанием, которую отправляет бот.
    ВАЖНО! parse_mode='HTML' - чтобы читалcя измененный шрифт.
    """
    STRING = ""  # "строка" с расписанием, которую отправляем сообщением
    for (
        row
    ) in (
        schedule.iterrows()
    ):  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
        # время пары - жирный + наклонный шрифт, название пары на следующей строке
        string: str = "<b>" + "<i>" + row[0] + "</i>" + "</b>" + "\n" + row[1][0]
        STRING += string + "\n\n"  # между парами пропуск (1 enter)
    return STRING
