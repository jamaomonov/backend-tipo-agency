from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from core.models.db_helper import db_helper
from core.models.models import Product, ProductVariant, ProductCategory, ProductImage


async def get_products_with_variants(session: AsyncSession, limit: int = 100, offset: int = 0):
    """
    Получает все активные продукты с их вариантами и изображениями
    """
    # Подзапрос для подсчета общего количества продуктов
    count_query = select(func.count(Product.id)).where(Product.is_active == True)
    total_count = await session.scalar(count_query)
    
    # Основной запрос для получения продуктов с вариантами
    query = (
        select(Product)
        .where(Product.is_active == True)
        .options(
            # Загружаем связанные данные
            selectinload(Product.category),
            selectinload(Product.variants).selectinload(ProductVariant.images)
        )
        .limit(limit)
        .offset(offset)
        .order_by(Product.id.desc())
    )
    
    result = await session.execute(query)
    products = result.scalars().unique().all()
    
    return products, total_count


async def get_products_by_category(session: AsyncSession, category_slug: str, limit: int = 100, offset: int = 0):
    """
    Получает продукты определенной категории с их вариантами и изображениями
    """
    # Подзапрос для подсчета общего количества продуктов в категории
    count_query = (
        select(func.count(Product.id))
        .join(ProductCategory, Product.category_id == ProductCategory.id)
        .where(Product.is_active == True, ProductCategory.slug == category_slug)
    )
    total_count = await session.scalar(count_query)
    
    # Основной запрос для получения продуктов категории с вариантами
    query = (
        select(Product)
        .join(ProductCategory, Product.category_id == ProductCategory.id)
        .where(Product.is_active == True, ProductCategory.slug == category_slug)
        .options(
            selectinload(Product.category),
            selectinload(Product.variants).selectinload(ProductVariant.images)
        )
        .limit(limit)
        .offset(offset)
        .order_by(Product.id.desc())
    )
    
    result = await session.execute(query)
    products = result.scalars().unique().all()
    
    return products, total_count


async def get_all_categories(session: AsyncSession):
    """
    Получает все категории продуктов
    """
    query = select(ProductCategory).order_by(ProductCategory.name)
    result = await session.execute(query)
    categories = result.scalars().all()
    
    return categories
