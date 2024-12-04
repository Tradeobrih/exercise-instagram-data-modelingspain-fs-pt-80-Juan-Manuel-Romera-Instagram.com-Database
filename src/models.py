import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    
    # Relaciones
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers = relationship(
        "Follower", 
        foreign_keys="[Follower.user_to_id]", 
        back_populates="user_to"
    )
    following = relationship(
        "Follower", 
        foreign_keys="[Follower.user_from_id]", 
        back_populates="user_from"
    )

class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    
    # Relaciones
    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    
    # Relaciones
    post = relationship("Post", back_populates="media")

class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id'), nullable=False)
    
    # Relaciones
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Follower(Base):
    __tablename__ = 'Follower'
    user_from_id = Column(Integer, ForeignKey('User.id'), primary_key=True, nullable=False)
    user_to_id = Column(Integer, ForeignKey('User.id'), primary_key=True, nullable=False)
    
    # Relaciones
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

## Generar el esquema
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Consulta el archivo diagram.png")
except Exception as e:
    print("Hubo un problema generando el diagrama.")
    raise e