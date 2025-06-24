from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from admin.api.v1.products_variant.schemas import ProductVariantCreate, ProductVariantRead, ProductVariantUpdate
from admin.api.v1.products_variant.dependencies import (
    create_variant, read_variants, read_variants_by_product_id, update_variant, delete_variant, read_variant_by_id
)
from core.models.db_helper import db_helper

router = APIRouter(tags=["Product Variants"])

@router.post("/variants/", response_model=ProductVariantRead, status_code=201)
async def create_variant_route(variant: ProductVariantCreate, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await create_variant(variant, db)

@router.get("/variants/", response_model=list[ProductVariantRead])
async def read_variants_route(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(db_helper.session_dependency)):
    result = await read_variants(skip, limit, db)
    if not result:
        raise HTTPException(status_code=404, detail="No variants found")
    return result

@router.get("/variant/{variant_id}", response_model=ProductVariantRead)
async def read_variant_route(variant_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    variant = await read_variant_by_id(variant_id, db)
    if not variant:
        raise HTTPException(status_code=404, detail=f"ProductVariant with {variant_id} not found")
    return variant

@router.get("/variants/{product_id}", response_model=list[ProductVariantRead])
async def read_variant_route(product_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    variant = await read_variants_by_product_id(product_id, db)
    if not variant:
        raise HTTPException(status_code=404, detail=f"ProductVariant with {product_id} not found")
    return variant

@router.put("/variants/{variant_id}", response_model=ProductVariantRead)
async def update_variant_route(variant_id: int, variant: ProductVariantUpdate, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await update_variant(variant_id, variant, db)

@router.delete("/variants/{variant_id}")
async def delete_variant_route(variant_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await delete_variant(variant_id, db)
