from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    specie_id: Mapped[int] = mapped_column(ForeignKey("species.id"))
    vehicles: Mapped[List["Vehicles"]] = relationship(back_populates="owner")
    planet: Mapped["Planets"] = relationship(back_populates="characters")
    specie: Mapped["Species"] = relationship(back_populates="characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "planet_id": self.planet_id,
            "specie_id": self.specie_id
        }
    

class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    max_speed: Mapped[str] = mapped_column(nullable=False)
    charac_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    owner: Mapped["Characters"] = relationship(back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "max_speed": self.max_speed,
            "charac_id": self.charac_id
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    characters: Mapped[List["Characters"]] = relationship(back_populates="planet")
    species: Mapped[List["Species"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Species(db.Model):
    __tablename__ = "species"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    characters: Mapped[List["Characters"]] = relationship(back_populates="specie")
    planet: Mapped["Planets"] = relationship(back_populates="species")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "planet_id": self.planet_id
        }
