from fastapi import APIRouter
from .v1.products.routes import router as products_router
from .v1.products_category.routes import router as products_category_router
from .v1.products_images.routes import router as products_images_router
from .v1.products_variant.routes import router as products_variants_router

router = APIRouter()

router.include_router(products_router)
router.include_router(products_category_router)
router.include_router(products_images_router)
router.include_router(products_variants_router)



