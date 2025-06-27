from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models.db_helper import db_helper
from .dependencies import get_products_with_variants, get_products_by_category, get_all_categories
from .schemas import ProductRead, ProductsResponse, CategoriesResponse, ProductCategoryRead

router = APIRouter(tags=["snovidenie"])


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Получает все категории продуктов
    """
    categories = await get_all_categories(session)
    
    return CategoriesResponse(
        categories=[ProductCategoryRead.model_validate(category) for category in categories]
    )


@router.get("/products", response_model=ProductsResponse)
async def get_all_products(
    limit: int = Query(default=100, ge=1, le=1000, description="Количество продуктов на странице"),
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Получает все активные продукты с их вариантами и изображениями
    """
    products, total_count = await get_products_with_variants(session, limit, offset)
    
    return ProductsResponse(
        products=[ProductRead.model_validate(product) for product in products],
        total=total_count
    )


@router.get("/categories/{category_slug}/products", response_model=ProductsResponse)
async def get_products_by_category_slug(
    category_slug: str,
    limit: int = Query(default=100, ge=1, le=1000, description="Количество продуктов на странице"),
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Получает продукты определенной категории с их вариантами и изображениями
    """
    products, total_count = await get_products_by_category(session, category_slug, limit, offset)
    
    return ProductsResponse(
        products=[ProductRead.model_validate(product) for product in products],
        total=total_count
    )


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    """
    Получает конкретный продукт по ID с его вариантами и изображениями
    """
    from sqlalchemy.orm import selectinload
    from sqlalchemy import select
    from core.models.models import Product, ProductVariant
    
    query = (
        select(Product)
        .where(Product.id == product_id, Product.is_active == True)
        .options(
            selectinload(Product.category),
            selectinload(Product.variants).selectinload(ProductVariant.images)
        )
    )
    
    result = await session.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    return ProductRead.model_validate(product)
