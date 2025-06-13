from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.states import set_user_state, UserState
from utils.monitoring_manager import monitoring_manager
from handlers.router import router, db_queries
from keyboards.keyboards import get_builder_back_state, get_confirm_article


@router.callback_query(F.data.startswith("stop_article:"))
async def confirm_stop_article(callback: CallbackQuery, state: FSMContext):
    """Уточнения действия юзера."""
    await set_user_state(state, UserState.stop_article_section)

    article = callback.data.split(":")[1]

    await callback.message.edit_text(
        f"Вы точно хотите остановить мониторинг артикула <b>{article}</b>?",
        parse_mode="HTML",
        reply_markup=get_confirm_article(article)
    )

@router.callback_query(F.data.startswith("confirm_stop:"))
async def confirm_stop(callback: CallbackQuery, state: FSMContext):
    """Удаление  артикула с отслеживания."""
    await set_user_state(state, UserState.confirm_stop_section)

    user_id = callback.from_user.id
    article = callback.data.split(":")[1]

    try:
        monitoring_manager.cancel_task(user_id, article)
        await db_queries.delete_product_by_user_and_article(user_id, article)
        await callback.message.edit_text(f"🛑 Мониторинг артикула <b>{article}</b> остановлен.", parse_mode="HTML", reply_markup=get_builder_back_state())
    except Exception as e:
        await callback.message.edit_text(f"❌ Ошибка при остановке мониторинга: {e}")
