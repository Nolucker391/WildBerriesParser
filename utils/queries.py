from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from database.models import UserProduct, Review
from database.session import async_session


class QueriesDatabase:
    def __init__(self):
        self.session_factory = async_session

    async def is_article_exists(self, user_id: int, article: str) -> bool:
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserProduct).where(
                    UserProduct.user_id == user_id,
                    UserProduct.article == article
                )
            )
            return result.scalar_one_or_none() is not None

    async def add_product(self, user_id: int, article: str, name: str, root_id: int) -> UserProduct:
        async with self.session_factory() as session:
            product = UserProduct(
                user_id=user_id,
                article=article,
                product_name=name,
                root_id=root_id
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product

    async def add_review(self, product_id: int, review_data: dict):
        async with self.session_factory() as session:
            review = Review(
                id=review_data["id"],
                product_id=product_id,
                rating=review_data["rating"],
                text=review_data["text"],
                advantages=review_data["advantages"],
                disadvantages=review_data["disadvantages"],
                author=review_data["author"],
                created_at=review_data["datetime"]
            )
            session.add(review)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def get_reviews_by_root(self, root_id: int) -> list[Review]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserProduct).where(UserProduct.root_id == root_id)
            )
            user_product = result.scalars().first()
            return user_product.reviews if user_product else []

    async def get_products_by_user(self, user_id: int) -> list[UserProduct]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserProduct).where(UserProduct.user_id == user_id)
            )
            return result.scalars().all()

    async def delete_product_by_user_and_article(self, user_id: int, article: str):
        async with self.session_factory() as session:
            result = await session.execute(
                select(UserProduct).where(
                    UserProduct.user_id == user_id,
                    UserProduct.article == article
                )
            )
            product = result.scalar_one_or_none()
            if product:
                await session.delete(product)
                await session.commit()
