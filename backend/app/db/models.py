"""
Modelos SQLAlchemy 2.0 para rally.db.

Esquema identico a los CSVs existentes para que la migracion
sea directa y los endpoints no necesiten cambios.
"""

from __future__ import annotations

from sqlalchemy import (
    Column, Float, ForeignKey, Index, Integer, String,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "events"

    event_id    = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    status      = Column(String, default="Completed")
    country     = Column(String, default="")
    country_iso = Column(String, default="")
    date_start  = Column(String, default="")
    date_finish = Column(String, default="")


class Stage(Base):
    __tablename__ = "stages"
    __table_args__ = (
        Index("ix_stages_event_id", "event_id"),
    )

    stage_id    = Column(Integer, primary_key=True)
    event_id    = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    stage_code  = Column(String, nullable=False)
    name        = Column(String, default="")
    distance_km = Column(Float, default=0.0)
    surface     = Column(String, default="Tarmac")
    leg_name    = Column(String, default="")
    status      = Column(String, default="Completed")


class Entry(Base):
    __tablename__ = "entries"
    __table_args__ = (
        Index("ix_entries_event_id", "event_id"),
        Index("ix_entries_entry_id", "entry_id"),
    )

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    entry_id           = Column(Integer, nullable=False)
    event_id           = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    driver_name        = Column(String, default="")
    driver_code        = Column(String, default="")
    driver_nationality = Column(String, default="")
    codriver_name      = Column(String, default="")
    manufacturer       = Column(String, default="")
    car_number         = Column(String, default="")
    car_model          = Column(String, default="")
    group              = Column(String, default="")


class StageTime(Base):
    __tablename__ = "stage_times"
    __table_args__ = (
        Index("ix_stage_times_event_id", "event_id"),
        Index("ix_stage_times_stage_id", "stage_id"),
        Index("ix_stage_times_entry_id", "entry_id"),
    )

    id            = Column(Integer, primary_key=True, autoincrement=True)
    event_id      = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    stage_id      = Column(Integer, ForeignKey("stages.stage_id"), nullable=False)
    entry_id      = Column(Integer, nullable=False)
    position      = Column(Integer, nullable=False)
    time_ms       = Column(Integer, nullable=True)
    time_s        = Column(Float,   nullable=True)
    time_str      = Column(String,  nullable=True)
    diff_first_ms = Column(Integer, nullable=True)
    diff_first_s  = Column(Float,   nullable=True)
    diff_prev_ms  = Column(Integer, nullable=True)
    diff_prev_s   = Column(Float,   nullable=True)
    status        = Column(String, default="Completed")
    stage_code    = Column(String, default="")


class OverallResult(Base):
    __tablename__ = "overall_results"
    __table_args__ = (
        Index("ix_overall_event_id", "event_id"),
        Index("ix_overall_entry_id", "entry_id"),
        Index("ix_overall_stage_id", "stage_id"),
    )

    id               = Column(Integer, primary_key=True, autoincrement=True)
    event_id         = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    stage_id         = Column(Integer, nullable=False)
    entry_id         = Column(Integer, nullable=False)
    position         = Column(Integer, nullable=False)
    total_time_ms    = Column(Integer, nullable=True)
    total_time_s     = Column(Float,   nullable=True)
    total_time_str   = Column(String,  nullable=True)
    diff_first_ms    = Column(Integer, nullable=True)
    diff_first_s     = Column(Float,   nullable=True)
    status           = Column(String, default="Completed")
    stage_code       = Column(String, default="")
    retirement_stage = Column(String, nullable=True)
