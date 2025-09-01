from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    specie_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=True)
    planet: Mapped["Planets"] = relationship(back_populates="characters")
    specie: Mapped["Species"] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "planet_id": self.planet_id,
            "specie_id": self.specie_id
        }
    

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(250), nullable=False)
    population: Mapped[str] = mapped_column(String(250), nullable=False)
    characters: Mapped[List["Characters"]] = relationship(
        back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }


class Species(db.Model):
    __tablename__ = "species"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    designation: Mapped[str] = mapped_column(String(150), nullable=False)
    language: Mapped[str] = mapped_column(String(150), nullable=False)
    characters: Mapped[List["Characters"]] = relationship(
        back_populates="specie")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "designation": self.designation,
            "language": self.language
        }
