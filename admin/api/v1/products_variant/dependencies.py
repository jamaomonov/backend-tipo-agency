from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from core.models.models import ProductVariant, Product
from admin.api.v1.products_variant.schemas import ProductVariantCreate, ProductVariantRead, ProductVariantUpdate

async def create_variant(variant: ProductVariantCreate, db: AsyncSession) -> ProductVariant:
    product_result = await db.execute(select(Product).where(Product.id == variant.product_id))
    if not product_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Product with id: {variant.product_id} does not exist")
    db_variant = ProductVariant(**variant.dict())
    db.add(db_variant)
    await db.commit()
    await db.refresh(db_variant)
    # Явно подгружаем product, category и images для ответа
    result = await db.execute(
        select(ProductVariant)
        .options(
            selectinload(ProductVariant.product).selectinload(Product.category),
            selectinload(ProductVariant.images)
        )
        .where(ProductVariant.id == db_variant.id)
    )
    return result.scalar_one()

async def read_variants(skip: int, limit: int, db: AsyncSession) -> list[ProductVariant]:
    result = await db.execute(
        select(ProductVariant)
        .options(
            selectinload(ProductVariant.product).selectinload(Product.category),
            selectinload(ProductVariant.images)
        )
        .offset(skip).limit(limit)
    )
    return result.scalars().all()

async def read_variant_by_product_id(product_id: int, db: AsyncSession) -> list[ProductVariant]:
    result = await db.execute(
        select(ProductVariant)
        .options(
            selectinload(ProductVariant.product).selectinload(Product.category),
            selectinload(ProductVariant.images)
        )
        .where(ProductVariant.product_id == product_id)
    )
    variant = result.scalars().all()
    if not variant:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    return variant

async def update_variant(variant_id: int, variant: ProductVariantUpdate, db: AsyncSession) -> ProductVariant:
    result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
    db_variant = result.scalar_one_or_none()
    if not db_variant:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    if variant.product_id is not None:
        product_result = await db.execute(select(Product).where(Product.id == variant.product_id))
        if not product_result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"Product with id: {variant.product_id} does not exist")
    for key, value in variant.dict(exclude_unset=True).items():
        setattr(db_variant, key, value)
    await db.commit()
    await db.refresh(db_variant)
    # Явно подгружаем product, category и images для ответа
    result = await db.execute(
        select(ProductVariant)
        .options(
            selectinload(ProductVariant.product).selectinload(Product.category),
            selectinload(ProductVariant.images)
        )
        .where(ProductVariant.id == db_variant.id)
    )
    return result.scalar_one()

async def delete_variant(variant_id: int, db: AsyncSession) -> dict:
    result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
    db_variant = result.scalar_one_or_none()
    if not db_variant:
        raise HTTPException(status_code=404, detail="ProductVariant not found")
    await db.delete(db_variant)
    await db.commit()
    return {"ok": True}






