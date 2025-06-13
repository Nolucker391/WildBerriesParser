from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.filters import Command

from keyboards.keyboards import get_main_menu
from states.states import set_user_state, UserState
from settings.config import media_file
from ..router import router
from settings.config import logger


@router.message(Command("start"))
async def start_command(message_or_callback: types.Message | types.CallbackQuery, state: FSMContext):
    await state.update_data(history=[])
    await set_user_state(state, UserState.start_section)

    logger.info(f"Нажата комманда /start")

    if isinstance(message_or_callback, types.CallbackQuery):
        user = message_or_callback.from_user
        message = message_or_callback.message
    else:
        user = message_or_callback.from_user
        message = message_or_callback

    logger.info(f"Данные пользователя: ID: {user.id}, Username: {user.username}, First Name: {user.first_name}")

    await message.answer_video(
        video=FSInputFile(media_file()),
        caption="Привет 👋, Я - БОТ🤖\n\ntext text text",
        reply_markup=get_main_menu(),
    )
