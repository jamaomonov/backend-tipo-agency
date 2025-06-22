from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from admin.api.v1.products_category.schemas import ProductCategoryCreate, ProductCategoryRead, ProductCategoryUpdate
from admin.api.v1.products_category.dependencies import (
    create_category, read_categories, read_category, update_category, delete_category
)
from core.models.db_helper import db_helper

router = APIRouter(tags=["Product Categories"])

@router.post("/categories/", response_model=ProductCategoryRead, status_code=201)
async def create_category_route(category: ProductCategoryCreate, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await create_category(category, db)

@router.get("/categories/", response_model=list[ProductCategoryRead])
async def read_categories_route(db: AsyncSession = Depends(db_helper.session_dependency)):
    result = await read_categories(db)
    if not result:
        raise HTTPException(status_code=404, detail="No categories found")
    return result

@router.get("/categories/{category_id}", response_model=ProductCategoryRead)
async def read_category_route(category_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await read_category(category_id, db)

@router.put("/categories/{category_id}", response_model=ProductCategoryRead)
async def update_category_route(category_id: int, category: ProductCategoryUpdate, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await update_category(category_id, category, db)

@router.delete("/categories/{category_id}")
async def delete_category_route(category_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await delete_category(category_id, db)

