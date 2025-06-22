from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, UploadFile
from core.models.models import ProductImage, ProductVariant
from admin.api.v1.products_images.schemas import ProductImageCreate, ProductImageRead, ProductImageUpdate
from core.config import STATIC_DIR, STATIC_MOUNT_PATH
import os
from uuid import uuid4

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def validate_and_save_image(file: UploadFile, variant_id: int) -> str:
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: jpg, jpeg, png")
    filename = f"{uuid4().hex}.{ext}"
    variant_folder = os.path.join(STATIC_DIR, str(variant_id))
    os.makedirs(variant_folder, exist_ok=True)
    file_path = os.path.join(variant_folder, filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    url = f"{STATIC_MOUNT_PATH}/{variant_id}/{filename}"
    return url

async def create_image(variant_id: int, file: UploadFile, db: AsyncSession) -> ProductImage:
    variant_result = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
    variant = variant_result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=400, detail=f"ProductVariant with id: {variant_id} does not exist")
    url = validate_and_save_image(file, variant_id)
    db_image = ProductImage(variant_id=variant_id, url=url)
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image

async def read_images(skip: int, limit: int, db: AsyncSession) -> list[ProductImage]:
    result = await db.execute(
        select(ProductImage).options(selectinload(ProductImage.variant)).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def read_image(image_id: int, db: AsyncSession) -> ProductImage:
    result = await db.execute(
        select(ProductImage).options(selectinload(ProductImage.variant)).where(ProductImage.id == image_id)
    )
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="ProductImage not found")
    return image

async def update_image(image_id: int, file: UploadFile, db: AsyncSession) -> ProductImage:
    result = await db.execute(select(ProductImage).where(ProductImage.id == image_id))
    db_image = result.scalar_one_or_none()
    if not db_image:
        raise HTTPException(status_code=404, detail="ProductImage not found")
    url = validate_and_save_image(file, db_image.variant_id)
    db_image.url = url
    await db.commit()
    await db.refresh(db_image)
    return db_image

async def delete_image(image_id: int, db: AsyncSession) -> dict:
    result = await db.execute(select(ProductImage).where(ProductImage.id == image_id))
    db_image = result.scalar_one_or_none()
    if not db_image:
        raise HTTPException(status_code=404, detail="ProductImage not found")
    # Удаляем файл физически
    file_path = os.path.join(STATIC_DIR, str(db_image.variant_id), os.path.basename(db_image.url))
    if os.path.exists(file_path):
        os.remove(file_path)
    await db.delete(db_image)
    await db.commit()
    return {"ok": True}
