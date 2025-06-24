from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from .base import Base
from slugify import slugify  # pip install python-slugify


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), unique=True, index=True)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")  # <--- добавить

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.slug = slugify(name)  # Автоматически создаём slug

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)  # добавлено
    is_active = Column(Boolean, default=True)
    is_new = Column(Boolean, default=False)
    is_discounted = Column(Boolean, default=False)
    

    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    category = relationship("ProductCategory", back_populates="products")

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.slug = slugify(name)  # Автоматически создаём slug


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    color = Column(String(100), nullable=True)
    size = Column(String(100), nullable=True)
    material = Column(String(100), nullable=True)
    stock_quantity = Column(Integer, default=0)
    price = Column(Numeric(18, 2), nullable=False)

    product = relationship("Product", back_populates="variants")
    images = relationship("ProductImage", back_populates="variant", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
    url = Column(String(500), nullable=False)
    is_main = Column(Boolean, default=False)

    variant = relationship("ProductVariant", back_populates="images")

    def __init__(self, url, **kwargs):
        super().__init__(url=url, **kwargs)
        self.is_main = kwargs.get('is_main', False)  # Устанавливаем значение по умолчанию для is_main