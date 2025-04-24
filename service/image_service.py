# service/image_service.py
from typing import List, Optional
from repository.image_repository import ImageRepository
from models.schemas import ImageOut, ImageCreate
from models.db_models import Image


class ImageService:
    def __init__(self):
        self.repo = ImageRepository()

    def get_image(self, image_id: int) -> Optional[ImageOut]:
        image = self.repo.get_by_id(image_id)
        if image:
            return self._to_schema(image)
        return None

    def list_images(self, author: Optional[str], tag: Optional[str]) -> List[ImageOut]:
        images = self.repo.list(author, tag)
        return [self._to_schema(img) for img in images]

    def update_image(self, image_id: int, new_title: str) -> Optional[ImageOut]:
        updated = self.repo.update_title(image_id, new_title)
        if updated:
            return self._to_schema(updated)
        return None

    def delete_image(self, image_id: int) -> bool:
        return self.repo.delete(image_id)

    def _to_schema(self, image: Image) -> ImageOut:
        return ImageOut(
            id=image.id,
            title=image.title,
            image=image.image,
            author=image.author.name,
            tags=[tag.name for tag in image.tags],
            created_at=image.created_at
        )
    
    def create_image(self, payload: ImageCreate) -> ImageOut:
        image = self.repo.create(payload)
        return self._to_schema(image)