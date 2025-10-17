from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def serialize(self):
        return dict(
            id=self.id,
            email=self.email,
        )


class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites")
    characters: Mapped[list["Character"]] = relationship(
        back_populates="favorite",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    vehicles: Mapped[list["Vehicle"]] = relationship(
        back_populates="favorite",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    planets: Mapped[list["Planet"]] = relationship(
        back_populates="favorite",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=False)
    favorite_id: Mapped[int | None] = mapped_column(
        ForeignKey("favorite.id"), nullable=True)
    favorite: Mapped["Favorite"] = relationship(back_populates="characters")

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=False)
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorite.id"))
    favorite: Mapped["Favorite"] = relationship(back_populates="vehicles")

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
        )


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=False)
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorite.id"))
    favorite: Mapped["Favorite"] = relationship(back_populates="planets")

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
        )
