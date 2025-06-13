from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from states.states import UserState
from handlers.router import router
from handlers.DefaultCommands.start import start_command
from handlers.CallbackArticles.Rewards.show_rewards import look_rewards_latest
from handlers.handl import article_cmd, stop_monitoring_cmd
from settings.config import logger


@router.callback_query(F.data == 'back')
async def back_to_previous_state(callback: CallbackQuery, state: FSMContext):
    """Возвращает пользователя к предыдущему состоянию"""

    data = await state.get_data()
    history = data.get("history", [])
    if len(history) > 1:
        history.pop()
        previous_state_name = history[-1]
        previous_state = getattr(UserState, previous_state_name.split(":")[-1], UserState.start_section)
    else:
        previous_state = UserState.start_section
        previous_state_name = UserState.start_section.state

    await state.update_data(history=history)
    await state.set_state(previous_state)
    logger.info(f"[FSM] Назад к состоянию: {previous_state_name}")

    if previous_state == UserState.start_section:
        await callback.message.delete()
        await start_command(callback.message, state)
    elif previous_state == UserState.add_article_section:
        await article_cmd(callback, state)
    elif previous_state == UserState.look_rewards_section:
        await look_rewards_latest(callback, state)

    elif previous_state == UserState.stop_monitoring_section:
        await stop_monitoring_cmd(callback, state)
    elif previous_state == UserState.stop_article_section:
        await stop_monitoring_cmd(callback, state)

    elif previous_state == UserState.confirm_stop_section:
        await callback.message.delete()
        await start_command(callback.message, state)
