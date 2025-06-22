from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from admin.api.v1.products.schemas import ProductCreate, ProductRead, ProductUpdate
from core.models import db_helper
from .dependencies import create_product, read_products, read_product, update_product, delete_product

router = APIRouter(tags=["Products"])

@router.post("/products/", response_model=ProductRead, status_code=201)
async def create(product: ProductCreate, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await create_product(product=product, db=db)

@router.get("/products/", response_model=list[ProductRead])
async def read(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(db_helper.session_dependency)):
    results = await read_products(skip=skip, limit=limit, db=db)
    if not results:
        raise HTTPException(status_code=404, detail="No products found")
    return results

@router.get("/products/{product_id}", response_model=ProductRead)
async def read_one(product_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    product = await read_product(product_id=product_id, db=db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductRead)
async def update(product: ProductUpdate, product_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    return await update_product(product=product, product_id=product_id, db=db)

@router.delete("/products/{product_id}")
async def delete(product_id: int, db: AsyncSession = Depends(db_helper.session_dependency)):
    result = await delete_product(product_id=product_id, db=db)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


