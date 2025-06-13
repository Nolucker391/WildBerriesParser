from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import asyncio

from keyboards.keyboards import get_list_rewards
from utils.monitor import get_product_info, get_reviews
from utils.monitoring_manager import monitoring_manager
from settings.config import user_tasks, user_products
from handlers.router import router, db_queries
from settings.config import logger


@router.message(F.text.regexp(r"^\d{6,}$"))
async def handle_article_input(message: Message, state: FSMContext):
    """Функция для обработки артикула юзера."""

    article = message.text.strip()
    user_id = message.chat.id

    logger.info(f"Пользователь ввел номер артикула: {message.text}")

    if await db_queries.is_article_exists(user_id, article):
        await message.answer("⚠️ Вы уже добавляли данный товар в мониторинг.")
        return

    try:
        product = await get_product_info(article)
        saved_product = await db_queries.add_product(
            user_id=user_id,
            article=article,
            name=product["name"],
            root_id=product["root"]
        )

        user_products[user_id] = product

        async def monitor_task():
            seen_ids = set()
            try:
                existing_reviews = await get_reviews(product["root"])
                seen_ids.update(r["id"] for r in existing_reviews)
            except Exception as e:
                await message.answer(f"⚠️ Не удалось получить отзывы: {e}")

            while True:
                try:
                    reviews = await get_reviews(product["root"])
                    new_reviews = [
                        r for r in reviews
                        if r["id"] not in seen_ids and r["rating"] <= 3
                    ]
                    for r in new_reviews:
                        seen_ids.add(r["id"])
                        await db_queries.add_review(saved_product.id, r)
                        dt = r["datetime"].strftime("%Y-%m-%d %H:%M:%S")

                        await message.answer(
                            f"🔴 <b>Новый негативный отзыв</b>\n"
                            f"📦 Товар: {product['name']}\n"
                            f"⭐️ Оценка: {r['rating']}/5\n"
                            f"💬 Отзыв: \"{r['text']}\"\n"
                            f"👤 Автор: {r['author']}\n"
                            f"🕒 Дата: {dt}\n"
                            f"👍 Достоинства: {r['advantages'] or '—'}\n"
                            f"👎 Недостатки: {r['disadvantages'] or '—'}",
                            parse_mode="HTML"
                        )
                except Exception as e:
                    await message.answer(f"⚠️ Ошибка при получении отзывов: {e}")
                await asyncio.sleep(1800)

        task = asyncio.create_task(monitor_task())
        user_tasks[user_id] = task
        monitoring_manager.add_task(user_id, article, task)

        await message.answer(
            f"✅ Товар найден: {product['name']}\nМониторинг успешно запущен.",
            reply_markup=get_list_rewards()
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
