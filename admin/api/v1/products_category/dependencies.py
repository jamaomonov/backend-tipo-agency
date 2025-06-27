from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from core.models.models import ProductCategory
from admin.api.v1.products_category.schemas import ProductCategoryCreate, ProductCategoryUpdate

async def create_category(category: ProductCategoryCreate, db: AsyncSession) -> ProductCategory:
    # Проверяем на дубликат по name
    existing_category = await db.execute(select(ProductCategory).where(ProductCategory.name == category.name))
    if existing_category.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Category with name '{category.name}' already exists")
    
    db_category = ProductCategory(**category.dict())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def read_categories(db: AsyncSession) -> list[ProductCategory]:
    result = await db.execute(select(ProductCategory))
    return result.scalars().all()

async def read_category(category_id: int, db: AsyncSession) -> ProductCategory:
    result = await db.execute(select(ProductCategory).where(ProductCategory.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

async def update_category(category_id: int, category: ProductCategoryUpdate, db: AsyncSession) -> ProductCategory:
    result = await db.execute(select(ProductCategory).where(ProductCategory.id == category_id))
    db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def delete_category(category_id: int, db: AsyncSession) -> dict:
    result = await db.execute(select(ProductCategory).where(ProductCategory.id == category_id))
    db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(db_category)
    await db.commit()
    return {"ok": True}



