from typing import List, Optional
from sqlalchemy.orm import Session
from models.db_models import Image, Author, Tag
from db.database import Database
from sqlalchemy.orm import joinedload
from models.schemas import ImageCreate

class ImageRepository:
    def __init__(self):
        self.db: Session = Database.get_instance().get_session()

    def get_by_id(self, image_id: int) -> Optional[Image]:
        return self.db.query(Image).options(joinedload(Image.author), joinedload(Image.tags)).filter(Image.id == image_id).first()

    def list(self, author: Optional[str], tag: Optional[str]) -> List[Image]:
        query = self.db.query(Image).options(joinedload(Image.author), joinedload(Image.tags))

        if author:
            query = query.join(Image.author).filter(Author.name == author)

        if tag:
            query = query.join(Image.tags).filter(Tag.name == tag)

        return query.all()

    def update_title(self, image_id: int, new_title: str) -> Optional[Image]:
        image = self.db.query(Image).filter(Image.id == image_id).first()
        if image:
            image.title = new_title
            self.db.commit()
            self.db.refresh(image)
        return image

    def delete(self, image_id: int) -> bool:
        image = self.db.query(Image).filter(Image.id == image_id).first()
        if image:
            self.db.delete(image)
            self.db.commit()
            return True
        return False
    
    def create(self, payload: ImageCreate) -> Image:
        # Get or create author
        author = self.db.query(Author).filter_by(name=payload.author).first()
        if not author:
            author = Author(name=payload.author)
            self.db.add(author)
            self.db.commit()
            self.db.refresh(author)

        # Get or create tags
        tags = []
        for tag_name in payload.tags:
            tag = self.db.query(Tag).filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                self.db.add(tag)
                self.db.commit()
                self.db.refresh(tag)
            tags.append(tag)

        # Create image
        image = Image(
            image=payload.image,
            title=payload.title,
            author_id=author.id,
            tags=tags
        )

        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image