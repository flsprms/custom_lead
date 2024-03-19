from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_cancel_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Отмена')
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)
