from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from core.models.models import Product, ProductCategory
from admin.api.v1.products.schemas import ProductCreate, ProductRead, ProductUpdate

async def create_product(product: ProductCreate, db: AsyncSession) -> Product:
    category_result = await db.execute(select(ProductCategory).where(ProductCategory.id == product.category_id))
    if not category_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Category with id: {product.category_id} does not exist")
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    # Явно подгружаем category для ответа
    result = await db.execute(
        select(Product).options(selectinload(Product.category)).where(Product.id == db_product.id)
    )
    return result.scalar_one()

async def read_products(skip: int, limit: int, db: AsyncSession) -> list[Product]:
    result = await db.execute(
        select(Product).options(selectinload(Product.category)).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def read_product(product_id: int, db: AsyncSession) -> Product:
    result = await db.execute(
        select(Product).options(selectinload(Product.category)).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def update_product(product_id: int, product: ProductUpdate, db: AsyncSession) -> Product:
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.category_id is not None:
        category_result = await db.execute(select(ProductCategory).where(ProductCategory.id == product.category_id))
        if not category_result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"Category with id: {product.category_id} does not exist")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    await db.commit()
    await db.refresh(db_product)
    # Явно подгружаем category для ответа
    result = await db.execute(
        select(Product).options(selectinload(Product.category)).where(Product.id == db_product.id)
    )
    return result.scalar_one()

async def delete_product(product_id: int, db: AsyncSession) -> dict:
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return {"ok": True}





