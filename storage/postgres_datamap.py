from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import get_type_hints

class Base(DeclarativeBase):
  pass

class News(Base):
  __tablename__ = "cfa_news"
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  title: Mapped[str]
  url: Mapped[str] = mapped_column(unique=True)
  #publish_time: Mapped[datetime] = mapped_column(index=True)
  publish_time: Mapped[str] = mapped_column(index=True)
  publisher_name: Mapped[str]
  scraper: Mapped[str]

  def __repr__(self) -> str:
    cls_level_attrs = get_type_hints(self).keys()
    repr_str = ', '.join(f"{attr}={getattr(self, attr)!r}" for attr in cls_level_attrs)
    return f"{self.__class__.__name__}({repr_str})"
