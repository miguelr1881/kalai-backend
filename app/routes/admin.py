from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.database import get_db
from app.models import (
    Product, 
    ProductCreate, 
    ProductUpdate,
    Treatment,
    TreatmentCreate,
    TreatmentUpdate,
    AdminLogin, 
    AdminToken
)
from app.auth import verify_admin, create_access_token, verify_token
from datetime import datetime

router = APIRouter()


@router.post("/login", response_model=AdminToken)
async def admin_login(credentials: AdminLogin):
    """Admin login endpoint"""
    if not verify_admin(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/products", response_model=List[Product])
async def get_all_products(token: dict = Depends(verify_token)):
    """Get all products including inactive ones (admin only)"""
    try:
        db = get_db()
        response = db.table("products").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, token: dict = Depends(verify_token)):
    """Create a new product (admin only)"""
    try:
        db = get_db()
        
        product_data = product.model_dump()
        product_data["created_at"] = datetime.utcnow().isoformat()
        product_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = db.table("products").insert(product_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create product")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")


@router.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int, 
    product: ProductUpdate, 
    token: dict = Depends(verify_token)
):
    """Update a product (admin only)"""
    try:
        db = get_db()
        
        # Check if product exists
        check_response = db.table("products").select("*").eq("id", product_id).execute()
        if not check_response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update only provided fields
        update_data = {k: v for k, v in product.model_dump(exclude_unset=True).items()}
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow().isoformat()
            response = db.table("products").update(update_data).eq("id", product_id).execute()
            
            if not response.data:
                raise HTTPException(status_code=500, detail="Failed to update product")
            
            return response.data[0]
        
        return check_response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, token: dict = Depends(verify_token)):
    """Delete a product (admin only)"""
    try:
        db = get_db()
        
        # Check if product exists
        check_response = db.table("products").select("*").eq("id", product_id).execute()
        if not check_response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.table("products").delete().eq("id", product_id).execute()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")


@router.patch("/products/{product_id}/toggle-active", response_model=Product)
async def toggle_product_active(product_id: int, token: dict = Depends(verify_token)):
    """Toggle product active status (admin only)"""
    try:
        db = get_db()
        
        # Get current status
        response = db.table("products").select("*").eq("id", product_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        current_status = response.data[0]["is_active"]
        
        # Toggle status
        update_response = db.table("products").update({
            "is_active": not current_status,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", product_id).execute()
        
        return update_response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error toggling product status: {str(e)}")


@router.patch("/products/{product_id}/stock", response_model=Product)
async def update_stock(
    product_id: int, 
    new_stock: int, 
    token: dict = Depends(verify_token)
):
    """Update product stock (admin only)"""
    try:
        if new_stock < 0:
            raise HTTPException(status_code=400, detail="Stock cannot be negative")
        
        db = get_db()
        
        response = db.table("products").update({
            "stock": new_stock,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating stock: {str(e)}")


# ============= TREATMENTS ADMIN ENDPOINTS =============

@router.get("/treatments")
async def get_all_treatments(token: dict = Depends(verify_token)):
    """Get all treatments including inactive ones (admin only)"""
    try:
        db = get_db()
        response = db.table("treatments").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching treatments: {str(e)}")


@router.post("/treatments", status_code=status.HTTP_201_CREATED)
async def create_treatment(treatment: TreatmentCreate, token: dict = Depends(verify_token)):
    """Create a new treatment (admin only)"""
    try:
        db = get_db()
        
        treatment_data = treatment.model_dump()
        treatment_data["stock"] = 999  # Tratamientos siempre disponibles
        treatment_data["created_at"] = datetime.utcnow().isoformat()
        treatment_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = db.table("treatments").insert(treatment_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create treatment")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating treatment: {str(e)}")


@router.put("/treatments/{treatment_id}")
async def update_treatment(
    treatment_id: str, 
    treatment: TreatmentUpdate, 
    token: dict = Depends(verify_token)
):
    """Update a treatment (admin only)"""
    try:
        db = get_db()
        
        # Check if treatment exists
        check_response = db.table("treatments").select("*").eq("id", treatment_id).execute()
        if not check_response.data:
            raise HTTPException(status_code=404, detail="Treatment not found")
        
        # Update only provided fields
        update_data = {k: v for k, v in treatment.model_dump(exclude_unset=True).items()}
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow().isoformat()
            response = db.table("treatments").update(update_data).eq("id", treatment_id).execute()
            
            if not response.data:
                raise HTTPException(status_code=500, detail="Failed to update treatment")
            
            return response.data[0]
        
        return check_response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating treatment: {str(e)}")


@router.delete("/treatments/{treatment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_treatment(treatment_id: str, token: dict = Depends(verify_token)):
    """Delete a treatment (admin only)"""
    try:
        db = get_db()
        
        # Check if treatment exists
        check_response = db.table("treatments").select("*").eq("id", treatment_id).execute()
        if not check_response.data:
            raise HTTPException(status_code=404, detail="Treatment not found")
        
        db.table("treatments").delete().eq("id", treatment_id).execute()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting treatment: {str(e)}")


@router.patch("/treatments/{treatment_id}/toggle-active")
async def toggle_treatment_active(treatment_id: str, token: dict = Depends(verify_token)):
    """Toggle treatment active status (admin only)"""
    try:
        db = get_db()
        
        # Get current status
        response = db.table("treatments").select("*").eq("id", treatment_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Treatment not found")
        
        current_status = response.data[0]["is_active"]
        
        # Toggle status
        update_response = db.table("treatments").update({
            "is_active": not current_status,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", treatment_id).execute()
        
        return update_response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error toggling treatment status: {str(e)}")
