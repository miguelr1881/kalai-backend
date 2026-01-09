from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.database import get_db
from app.models import Product, Treatment
from app.config import settings
import urllib.parse

router = APIRouter()


@router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    active_only: bool = True
):
    """Get all active products (public endpoint)"""
    try:
        db = get_db()
        query = db.table("products").select("*")
        
        if active_only:
            query = query.eq("is_active", True)
        
        if category:
            query = query.eq("category", category)
        
        query = query.order("created_at", desc=True)
        
        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a single product by ID"""
    try:
        db = get_db()
        response = db.table("products").select("*").eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@router.get("/categories")
async def get_categories():
    """Get all unique product categories"""
    try:
        db = get_db()
        response = db.table("products").select("category").execute()
        
        categories = list(set([item["category"] for item in response.data if item.get("category")]))
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")


@router.get("/whatsapp-link/{product_id}")
async def get_whatsapp_link(product_id: int):
    """Generate WhatsApp link for product inquiry"""
    try:
        db = get_db()
        response = db.table("products").select("*").eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product = response.data[0]
        message = f"Hola! Me interesa el producto: *{product['name']}*\nPrecio: ₡{product['price']:,.0f}"
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_link = f"https://wa.me/{settings.WHATSAPP_NUMBER.replace('+', '')}?text={encoded_message}"
        
        return {
            "whatsapp_link": whatsapp_link,
            "product_name": product['name'],
            "phone_number": settings.WHATSAPP_NUMBER
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating WhatsApp link: {str(e)}")


# ============= TREATMENTS ENDPOINTS =============

@router.get("/treatments")
async def get_treatments(
    category: Optional[str] = None,
    active_only: bool = True
):
    """Get all active treatments (public endpoint)"""
    try:
        db = get_db()
        query = db.table("treatments").select("*")
        
        if active_only:
            query = query.eq("is_active", True)
        
        if category:
            query = query.eq("category", category)
        
        query = query.order("created_at", desc=True)
        
        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching treatments: {str(e)}")


@router.get("/treatments/categories")
async def get_treatment_categories():
    """Get all unique treatment categories"""
    try:
        db = get_db()
        response = db.table("treatments").select("category").execute()
        
        categories = list(set([item["category"] for item in response.data if item.get("category")]))
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching treatment categories: {str(e)}")


@router.get("/treatments/{treatment_id}")
async def get_treatment(treatment_id: str):
    """Get a single treatment by ID"""
    try:
        db = get_db()
        response = db.table("treatments").select("*").eq("id", treatment_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Treatment not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching treatment: {str(e)}")


@router.get("/whatsapp-treatment/{treatment_id}")
async def get_whatsapp_treatment_link(treatment_id: str):
    """Generate WhatsApp link for treatment reservation"""
    try:
        db = get_db()
        response = db.table("treatments").select("*").eq("id", treatment_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Treatment not found")
        
        treatment = response.data[0]
        message = f"Hola! Me interesa reservar: *{treatment['name']}*\nPrecio: ₡{treatment['price']:,.0f}"
        
        encoded_message = urllib.parse.quote(message)
        whatsapp_link = f"https://wa.me/{settings.WHATSAPP_NUMBER.replace('+', '')}?text={encoded_message}"
        
        return {
            "whatsapp_link": whatsapp_link,
            "treatment_name": treatment['name'],
            "phone_number": settings.WHATSAPP_NUMBER
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating WhatsApp link: {str(e)}")
