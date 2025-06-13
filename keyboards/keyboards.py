from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='🆕 Добавить артикул', callback_data='first_block'),
        types.InlineKeyboardButton(text='🛑 Остановить мониторинг', callback_data='second_block')
    )
    builder.row(
        types.InlineKeyboardButton(text='ℹ️ Помощь', callback_data='third_block')
    )
    return builder.as_markup()


def get_list_rewards():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='Посмотреть отзывы за последние 3 дня', callback_data='look_rewards_latest')
    )

    return builder.as_markup()


def get_builder_back_state():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="назад", callback_data="back"))

    return builder.as_markup()


def get_confirm_article(article):
    builder = InlineKeyboardBuilder()

    builder.button(text="🛑 Остановить", callback_data=f"confirm_stop:{article}")
    builder.button(text="🔙 назад", callback_data="back")

    return builder.as_markup()


def get_builder_page(total_pages, current_page=0):
    builder = InlineKeyboardBuilder()
    for i in range(total_pages):
        text = f">{i + 1}<" if i == current_page else f"{i + 1}"
        builder.button(text=text, callback_data=f"look_reviews_page:{i}")
    builder.row(types.InlineKeyboardButton(text="назад", callback_data="back"))

    return builder.as_markup()
