from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import get_type_hints
from datetime import datetime

class Base(DeclarativeBase):
  pass

class News(Base):
  __tablename__ = "cfa_news_content"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  title: Mapped[str]
  url: Mapped[str] = mapped_column(unique=True)
  publish_time: Mapped[datetime] = mapped_column(index=True)
  #publish_time: Mapped[str] = mapped_column(index=True)
  publisher_name: Mapped[str]
  body_text: Mapped[str] = mapped_column(nullable=True)
  summarized_body_text: Mapped[str] = mapped_column(nullable=True) 
  scraper: Mapped[str]

  def __repr__(self) -> str:
    cls_level_attrs = get_type_hints(self).keys()
    repr_str = ', '.join(f"{attr}={getattr(self, attr)!r}" for attr in cls_level_attrs)
    return f"{self.__class__.__name__}({repr_str})"

class Releases(Base):
  __tablename__ = "cfa_releases_content"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  platform_name: Mapped[str]
  url: Mapped[str] = mapped_column(unique=True)
  release_time: Mapped[datetime]
  title: Mapped[str]
  pdf_text: Mapped[str] = mapped_column(nullable=True)
  cfa_count: Mapped[str] = mapped_column(nullable=True)
  cfa_price: Mapped[str] = mapped_column(nullable=True)
  coupon_period: Mapped[str] = mapped_column(nullable=True)
  date_time_placement_start: Mapped[str] = mapped_column(nullable=True)
  date_time_placement_end: Mapped[str] = mapped_column(nullable=True)
  cfa_repayment_date_time: Mapped[str] = mapped_column(nullable=True)
  cfa_repayment_method: Mapped[str] = mapped_column(nullable=True)

  def __repr__(self) -> str:
    cls_level_attrs = get_type_hints(self).keys()
    repr_str = ', '.join(f"{attr}={getattr(self, attr)!r}" for attr in cls_level_attrs)
    return f"{self.__class__.__name__}({repr_str})"

class Users(Base):
  __tablename__ = 'bot_users'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  telegram_user_id: Mapped[int]
  add_time: Mapped[datetime]
  update_time: Mapped[datetime]
  telegram_username: Mapped[str]
  telegram_first_name: Mapped[str]

class RegularNewsSubscribers(Base):
  __tablename__ = 'regular_news_subscribers'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  telegram_user_id: Mapped[int]
  add_time: Mapped[datetime]

class NewsPosts(Base):
  __tablename__ = 'news_posts'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  bot_post_id: Mapped[str]
  news_id: Mapped[int]

class ReleasesPosts(Base):
  __tablename__ = 'releases_posts'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  bot_post_id: Mapped[str]
  release_id: Mapped[int]

