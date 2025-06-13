from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


from states.states import set_user_state, UserState
from handlers.router import router, db_queries
from settings.config import logger


@router.callback_query(F.data == 'first_block')
async def article_cmd(callback: CallbackQuery, state: FSMContext):
    await set_user_state(state, UserState.add_article_section)
    await callback.message.delete()

    logger.info(f"Пользователь выбрал раздел: Добавление артикула")

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="назад", callback_data="back"))

    await callback.message.answer("Введите артикул для мониторинга:", reply_markup=builder.as_markup())

#
# @router.message()
# async def invalid_article_input(message: Message):
#     if message.text and not message.text.startswith('/'):
#         await message.answer("❌ Неверный формат артикула.\nПожалуйста, введите артикул из 6 и более цифр.")



@router.callback_query(F.data == 'second_block')
async def stop_monitoring_cmd(callback: CallbackQuery, state: FSMContext):
    await set_user_state(state, UserState.stop_monitoring_section)

    user_id = callback.message.chat.id
    products = await db_queries.get_products_by_user(user_id)

    await callback.message.delete()

    builder = InlineKeyboardBuilder()

    builderback = InlineKeyboardBuilder()
    builderback.row(types.InlineKeyboardButton(text="назад", callback_data="back"))

    if not products:
        await callback.message.answer("❌ У вас нет активных товаров в мониторинге.", reply_markup=builderback.as_markup())
        return

    for product in products:
        builder.row(types.InlineKeyboardButton(text=product.product_name, callback_data=f"stop_article:{product.article}"))

    builder.row(types.InlineKeyboardButton(text="назад", callback_data="back"))

    await callback.message.answer("Выберите товар для остановки мониторинга:", reply_markup=builder.as_markup())


