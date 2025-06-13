from datetime import datetime, timedelta
from settings.config import user_products, logger
from utils.monitor import get_reviews


async def get_negative_reviews(chat_id: int, days: int = 3):
    product = user_products.get(chat_id)
    if not product:
        return None, "⚠️ Сначала добавьте артикул.", None

    try:
        all_reviews = await get_reviews(product["root"])
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return None, f"❌ Ошибка при получении отзывов: {e}", None

    cutoff = datetime.now() - timedelta(days=days)
    negative_reviews = [
        r for r in all_reviews if r["rating"] <= 3 and r["datetime"] >= cutoff
    ]

    if not negative_reviews:
        return None, "За последние 3 дня негативных отзывов не найдено.", product

    return negative_reviews, None, product


def format_review_text(review: dict, product: dict) -> str:
    dt = review["datetime"].strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"🔴 <b>Негативный отзыв</b>\n"
        f"📦 Товар: {product['name']}\n"
        f"⭐️ Оценка: {review['rating']}/5\n"
        f"💬 Отзыв: \"{review['text']}\"\n"
        f"👤 Автор: {review['author']}\n"
        f"🕒 Дата: {dt}\n"
        f"👍 Достоинства: {review['advantages'] or '—'}\n"
        f"👎 Недостатки: {review['disadvantages'] or '—'}"
    )
