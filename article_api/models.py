

from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Article(Base):
    __tablename__ = "articles"
    ID = Column(Integer, primary_key=True, index=True)
    TITLE = Column(String(100), nullable=False)
    DESCRIPTION = Column(String(255), nullable=False)

    # Relationship to fetch comments and votes
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="article", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"
    ID = Column(Integer, primary_key=True, index=True)
    USER_NAME = Column(String(100), unique=True, index=True, nullable=False)
    PASSWORD = Column(String(200), nullable=False)

    # Relationship to fetch comments and votes by user
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"
    ID = Column(Integer, primary_key=True, index=True)
    COMMENT_TXT = Column(String(255), nullable=False)
    TITLE = Column(String(70), nullable=False)
    # Foreign keys
    ARTICLE_ID = Column(Integer, ForeignKey("articles.ID", ondelete="CASCADE"), nullable=False)
    USER_ID = Column(Integer, ForeignKey("users.ID", ondelete="CASCADE"), nullable=False)

    # Relationships
    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")


class Vote(Base):
    __tablename__ = "votes"
    ID = Column(Integer, primary_key=True, index=True)
    VOTE_TYPE = Column(String(20), nullable=False)
    # Foreign keys
    ARTICLE_ID = Column(Integer, ForeignKey("articles.ID", ondelete="CASCADE"), nullable=False)
    USER_ID = Column(Integer, ForeignKey("users.ID", ondelete="CASCADE"), nullable=False)

    # Relationships
    article = relationship("Article", back_populates="votes")
    user = relationship("User", back_populates="votes")



