# models/db_models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many: Image <-> Tag
image_tag_table = Table(
    'image_tag',
    Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship("Image", back_populates="author")

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(Text, nullable=False)  # URL or base64 content
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="images")

    tags = relationship("Tag", secondary=image_tag_table, back_populates="images")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    images = relationship("Image", secondary=image_tag_table, back_populates="tags")
