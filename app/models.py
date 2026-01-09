from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class WhatsAppMessage(BaseModel):
    product_id: int


# Treatment Models
class TreatmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    duration: Optional[str] = None  # "60 minutos", "5 sesiones", etc
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_active: bool = True


class TreatmentCreate(TreatmentBase):
    pass


class TreatmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    duration: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class Treatment(TreatmentBase):
    id: str  # UUID as string
    stock: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
