from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states.states import set_user_state, UserState
from ..router import router
from keyboards.keyboards import get_builder_back_state


@router.callback_query(F.data == 'third_block')
async def help_cmd(callback: CallbackQuery, state: FSMContext):

    await set_user_state(state, UserState.help_section)
    await callback.message.delete()

    await callback.message.answer(
        "/start — запустить бота\n"
        "/article — добавить артикул для мониторинга\n"
        "/stop_monitoring — остановить мониторинг\n"
        "/help — помощь",
        reply_markup=get_builder_back_state()
    )
