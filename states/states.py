from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from settings.config import logger


async def set_user_state(state: FSMContext, new_state: State):
    """Сохраняем новое состояние и обновляем историю"""

    data = await state.get_data()
    history = data.get("history", [])

    if not history or history[-1] != new_state.state:
        history.append(new_state.state)

    await state.update_data(history=history)
    await state.set_state(new_state)

    logger.info(f"[FSM] Переход в состояние: {new_state.state}")
    logger.info(f"[FSM] История: {history}")

class UserState(StatesGroup):
    """Состояние юзера на этапах."""

    start_section = State()
    help_section = State()
    add_article_section = State()
    look_rewards_section = State()

    stop_monitoring_section = State()
    stop_article_section = State()
    confirm_stop_section = State()
