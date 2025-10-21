from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    favorites: Mapped["FavoriteList"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False)


class FavoriteList(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(
        back_populates="favorites", single_parent=True
    )
    characters: Mapped[list["Character"]] = relationship(
        secondary="favorite_character", back_populates="favorite_lists"
    )
    vehicles: Mapped[list["Vehicle"]] = relationship(
        secondary="favorite_vehicle", back_populates="favorite_lists"
    )
    planets: Mapped[list["Planet"]] = relationship(
        secondary="favorite_planet", back_populates="favorite_lists"
    )


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_lists: Mapped[list["FavoriteList"]] = relationship(
        secondary="favorite_character", back_populates="characters"
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)


favorite_character = Table(
    "favorite_character",
    db.metadata,
    Column("favoritelist_id", ForeignKey(
        "favorite_list.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_lists: Mapped[list["FavoriteList"]] = relationship(
        secondary="favorite_vehicle", back_populates="vehicles"
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)


favorite_vehicle = Table(
    "favorite_vehicle",
    db.metadata,
    Column("favoritelist_id", ForeignKey(
        "favorite_list.id"), primary_key=True),
    Column("vehicle_id", ForeignKey("vehicle.id"), primary_key=True),
)


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_lists: Mapped[list["FavoriteList"]] = relationship(
        secondary="favorite_planet", back_populates="planets"
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)


favorite_planet = Table(
    "favorite_planet",
    db.metadata,
    Column("favoritelist_id", ForeignKey(
        "favorite_list.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True),
)
