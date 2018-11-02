from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Categories, Items
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


cat1 = Categories(name="Soccer")

session.add(cat1)
session.commit()

cat2 = Categories(name="Football")

session.add(cat2)
session.commit()

cat3 = Categories(name="Snowboard")

session.add(cat3)
session.commit()

cat4 = Categories(name="TaeKwonDo")

session.add(cat4)
session.commit()

cat5 = Categories(name="Wu-shu")

session.add(cat5)
session.commit()

cat8 = Categories(name="Swimming")

session.add(cat8)
session.commit()

cat6 = Categories(name="Basketball")

session.add(cat6)
session.commit()

cat7 = Categories(name="Baseball")

session.add(cat7)
session.commit()

cat9 = Categories(name="Skating")

session.add(cat9)
session.commit()


print "added categories"