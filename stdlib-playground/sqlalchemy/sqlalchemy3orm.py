# SQLAlchemy ORM - part 3

from sqlalchemy import create_engine, ForeignKey, String, MetaData, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy1 import DATABASE_URL


class Base(DeclarativeBase): # has .metadata and .registry
    pass

print('metadata.tables:', Base.metadata.tables)
print('registry.mappers:', Base.registry.mappers)


class Fruit(Base):
    __tablename__ = 'fruit'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    taste: Mapped[Optional[str]]

    continents: Mapped[List['Continent']] = relationship(back_populates='fruit')

    def __repr__(self): # emulate dataclass repr
        return f'Fruit({self.id=}, {self.name=}, {self.taste=})'


class Continent(Base):
    __tablename__ = 'continent'

    id: Mapped[int] = mapped_column(primary_key=True)
    fruit_id = mapped_column(ForeignKey('fruit.id'))
    name: Mapped[str] = mapped_column(String(30))

    fruit: Mapped[Fruit] = relationship(back_populates='continents')

    def __repr__(self):
        return f'Continent({self.id=}, {self.name=})'

print('metadata.tables:', Base.metadata.tables, sep='\n')
print('registry.mappers:', Base.registry.mappers, sep='\n')

engine = create_engine(DATABASE_URL, echo=False)
# Base.metadata.create_all(engine)


fruit = Fruit(name='pear', taste='good') # does nothing like this yet
print(fruit)

# most basic Core reflection
metadata_obj = MetaData()
user = Table('user', metadata_obj, autoload_with=engine)
print('User (repr):', repr(user), sep='\n')
