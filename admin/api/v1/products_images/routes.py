from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from admin.api.v1.products_images.schemas import ProductImageCreate, ProductImageRead, ProductImageUpdate
from admin.api.v1.products_images.dependencies import (
    create_image, read_images, read_image, update_image, delete_image
)
from core.models.db_helper import db_helper

router = APIRouter(tags=["Product Images"])

@router.post("/images/", response_model=ProductImageRead, status_code=201)
async def create_image_route(variant_id: int, is_main: bool, file: UploadFile = File(...), db: AsyncSession = Depends(db_helper.session_dependency)):
    return await create_image(variant_id, is_main, file, db)

@router.get("/images/", response_model=list[ProductImageRead])
async def read_images_route(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await read_images(skip, limit, db)

@router.get("/images/{image_id}", response_model=ProductImageRead)
async def read_image_route(image_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await read_image(image_id, db)

@router.put("/images/{image_id}", response_model=ProductImageRead)
async def update_image_route(
    image_id: int,
    is_main: bool | None = None,
    file: UploadFile | None = File(None),
    db: AsyncSession = Depends(db_helper.session_dependency)
):
    if is_main is None:
        is_main = False
    return await update_image(image_id, is_main, file, db)

@router.delete("/images/{image_id}")
async def delete_image_route(image_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await delete_image(image_id, db)
