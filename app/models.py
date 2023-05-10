
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    owner_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE",
                                 onupdate="NO ACTION"),
                      nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    id = Column(Integer, primary_key=True, index=True, nullable=False)


class Vote(Base):
    __tablename__ = "votes"


    user_id = Column(Integer,
                     ForeignKey("users.id", onupdate="NO ACTION",
                                ondelete="CASCADE"),
                     primary_key=True,
                     nullable=False)

    post_id = Column(Integer,
                     ForeignKey("posts.id", onupdate="NO ACTION",
                                ondelete="CASCADE"),
                     primary_key=True,
                     nullable=False)