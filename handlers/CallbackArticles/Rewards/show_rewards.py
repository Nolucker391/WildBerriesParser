from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from utils.review_formatted import format_review_text, get_negative_reviews
from states.states import set_user_state, UserState
from settings.config import ITEMS_PER_PAGE, logger
from handlers.router import router
from keyboards.keyboards import get_builder_back_state, get_builder_page


@router.callback_query(F.data == 'look_rewards_latest')
async def look_rewards_latest(callback: CallbackQuery, state: FSMContext):
    await set_user_state(state, UserState.look_rewards_section)
    chat_id = callback.message.chat.id

    logger.info(f"Пользователь выбрал раздел: Просмотр отзывов.")

    negative_reviews, error_msg, product = await get_negative_reviews(chat_id)
    if error_msg:
        await callback.message.edit_text(error_msg, reply_markup=get_builder_back_state())
        return

    review_text = format_review_text(negative_reviews[0], product)
    total_pages = (len(negative_reviews) - 1) // ITEMS_PER_PAGE + 1

    await callback.message.edit_text(
        review_text,
        parse_mode="HTML",
        reply_markup=get_builder_page(total_pages, current_page=0)
    )


@router.callback_query(F.data.startswith("look_reviews_page:"))
async def paginated_reviews(callback: CallbackQuery):
    """Пагинация отображения списка отзывов."""
    chat_id = callback.message.chat.id

    negative_reviews, error_msg, product = await get_negative_reviews(chat_id)
    if error_msg:
        await callback.message.edit_text(error_msg, reply_markup=get_builder_back_state())
        return

    try:
        page = int(callback.data.split(":")[1])
    except ValueError:
        page = 0

    total_pages = (len(negative_reviews) - 1) // ITEMS_PER_PAGE + 1
    page = max(0, min(page, total_pages - 1))
    r = negative_reviews[page * ITEMS_PER_PAGE]

    review_text = format_review_text(r, product)

    try:
        await callback.message.edit_text(
            review_text,
            parse_mode="HTML",
            reply_markup=get_builder_page(total_pages, current_page=page)
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise
