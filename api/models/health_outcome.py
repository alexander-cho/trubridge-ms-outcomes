from typing import Optional

from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from data.database import engine


class Base(DeclarativeBase):
    pass


class HealthOutcome(Base):
    __tablename__ = "health_outcome"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[str] = mapped_column(String(5))
    state_abbr: Mapped[str] = mapped_column(String(2))
    state_desc: Mapped[str] = mapped_column(String(30))
    county_name: Mapped[str] = mapped_column(String(30))
    county_fips: Mapped[str] = mapped_column(String(5))
    data_source: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))
    measure: Mapped[str] = mapped_column(String(100))
    data_value_unit: Mapped[str] = mapped_column(String(30))
    data_value_type: Mapped[str] = mapped_column(String(30))
    data_value: Mapped[float] = mapped_column(Float)
    low_confidence_limit: Mapped[float] = mapped_column(Float)
    high_confidence_limit: Mapped[float] = mapped_column(Float)
    total_population: Mapped[int] = mapped_column(Integer)
    total_adult_population: Mapped[int] = mapped_column(Integer)
    longitude: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)
    census_tract_id: Mapped[str] = mapped_column(String(30))
    category_id: Mapped[str] = mapped_column(String(30))
    measure_id: Mapped[str] = mapped_column(String(30))
    data_value_type_id: Mapped[str] = mapped_column(String(30))
    short_question_text: Mapped[str] = mapped_column(String(100))


Base.metadata.create_all(engine)
