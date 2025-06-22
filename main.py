from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from core.config import STATIC_DIR, STATIC_MOUNT_PATH
import logging
from core.lifespan import lifespan
from admin.api.routes import router as admin_router

logger = logging.getLogger(__name__)

# Основное приложение
app = FastAPI(
    title="Main API",
    version="1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

# Админское приложение
admin_app = FastAPI(
    title="Admin API",
    version="1.0",
    docs_url="/docs",  # Документация будет доступна по /admin/docs
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# Подключение роутеров
admin_app.include_router(router=admin_router, prefix="/api/v1")  # Префикс внутри admin_app
# app.include_router(router=client_router, prefix="/api/v1")

# Подключение статических файлов
app.mount(STATIC_MOUNT_PATH, StaticFiles(directory=STATIC_DIR), name="images")

app.mount("/admin", admin_app)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)