from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_id_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Мой telegram ID')
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)
