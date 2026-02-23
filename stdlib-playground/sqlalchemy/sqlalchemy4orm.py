# SQLAlchemy ORM - part 4 - reflection + queries

from sqlalchemy import create_engine, Table, Integer, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy1 import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False) # 'debug'

class Base(DeclarativeBase):
    pass

# class User(Base):
#     __table__ = Table('user', Base.metadata, autoload_with=engine)
# alternative approach - all at once
# Base.metadata.reflect(engine) 
# class User(Base):
#     __table__ = Base.metadata.tables['user']

# with mixin, mapping is delayed until DeferredReflection.prepare() method is called
class Reflected(DeferredReflection): 
    __abstract__ = True

class User(Reflected, Base):
    __tablename__ = 'user'

    def __repr__(self): # used to be automatic, now need to do myself
        return f'User({self.id=}, {self.username=}, {self.email=}, {self.full_name=} )'

Reflected.prepare(engine) # engine can be in another file now

# INSERT - row by row
dadi = User(username='Dadi', full_name='Bali')
dadi2 = User(username='Dadi2', full_name='Bali2')

session = Session(engine) # with Session(engine) as session, session.begin():
session.add(dadi) # add_all([])
session.add(dadi2) # add_all([])
print('to be added:', dadi)

stmt = select(User).filter_by(username='admin1')
user1 = session.execute(stmt).scalars().first() # .scalar_one()
print('to be added:', dadi) # selects autoflush, so dadi now has an id
# Use flush when you need to simulate a write, for example to get a pkey ID from an autoincrementing counter.
print('queried:', user1)
user1.full_name = 'Deni' # UPDATE is simple
print(session.dirty) # session.new, .dirty, 
# same as
some_user = session.get(User, 1)
print('.get:', some_user, some_user in session)

session.delete(dadi) # DELETE
session.commit() # pushes to DB
session.close()

