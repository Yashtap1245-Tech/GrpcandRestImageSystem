# api/rest/image_router.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import ImageOut, ImageUpdate
from service.image_service import ImageService
from models.schemas import ImageCreate

router = APIRouter()
service = ImageService()

@router.get("/", response_model=List[ImageOut])
def list_images(author: Optional[str] = None, tag: Optional[str] = None):
    return service.list_images(author, tag)

@router.post("/", response_model=ImageOut)
def create_image(payload: ImageCreate):
    return service.create_image(payload)

@router.get("/{image_id}", response_model=ImageOut)
def get_image(image_id: int):
    image = service.get_image(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.put("/{image_id}", response_model=ImageOut)
def update_image(image_id: int, update: ImageUpdate):
    updated = service.update_image(image_id, update.title)
    if not updated:
        raise HTTPException(status_code=404, detail="Image not found")
    return updated

@router.delete("/{image_id}")
def delete_image(image_id: int):
    success = service.delete_image(image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}
