# SQLAlchemy Core - part 2

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy1 import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
metadata_obj = MetaData()
"""
Having a single MetaData object for an entire application is the most common case, represented as a 
module-level variable in a single place in an application, often in a “models” or “dbschema” type of package. 
"""

fruits_table = Table(
    "fruit",
    metadata_obj, # manual metadata passing, implicitly handled in ORM (DeclarativeBase)
    Column('id', Integer, primary_key=True), # usual way to declare
    Column('name', String(30)),
    Column('taste', String), # instantiation not needed
)
# MetaData -> Tables -> Columns, indexes etc.

print(fruits_table.primary_key)
print([item for item in fruits_table.c])

continents_table = Table(
    'continent',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('fruit_id', ForeignKey('fruit.id'), nullable=False),
    Column('name', String(30)),
)

engine.logger.info(vars(metadata_obj))

if False:
    metadata_obj.create_all(engine) # does the work
    metadata_obj.drop_all(engine) # usually done with migration tools like Alembic

