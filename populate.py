from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from models import Base, Categories, Items
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

category_json = json.loads("""{
"all_categories": [
  {
    "name": "Soccer"
  },
  {
    "name": "Football"
  },
  {
    "name": "Snowboard"
  },
  {
    "name": "TaeKwonDo"
  },
  {
    "name": "Wu-shu"
  },
  {
    "name": "Swimming"
  },
  {
    "name": "Basketball"
  },
  {
    "name": "Baseball"
  },
  {
    "name": "Skating"
  }
]
}""")


for e in category_json['all_categories']:
    category_input = Categories(
        name=str(e['name']),
        id=str(e['id']),
        user_id= 1
  )
session.add(category_input)
session.commit()
# cat1 = Categories(name="Soccer")
#
# session.add(cat1)
# session.commit()
#
# cat2 = Categories(name="Football")
#
# session.add(cat2)
# session.commit()
#
# cat3 = Categories(name="Snowboard")
#
# session.add(cat3)
# session.commit()
#
# cat4 = Categories(name="TaeKwonDo")
#
# session.add(cat4)
# session.commit()
#
# cat5 = Categories(name="Wu-shu")
#
# session.add(cat5)
# session.commit()
#
# cat8 = Categories(name="Swimming")
#
# session.add(cat8)
# session.commit()
#
# cat6 = Categories(name="Basketball")
#
# session.add(cat6)
# session.commit()
#
# cat7 = Categories(name="Baseball")
#
# session.add(cat7)
# session.commit()
#
# cat9 = Categories(name="Skating")
#
# session.add(cat9)
# session.commit()
#
# itm1 = Items(name="SoccerBall", description="Ball used for play Soccer", categories_id=1, user_id=1)
# session.add(itm1)
# session.commit()
#
# itm2 = Items(name="Dobok", description="Uniform of TaeKwonDo", categories_id=4, user_id=1)
# session.add(itm2)
# session.commit()
#
# itm3 = Items(name="Budosaga Shoes", description="Wu-shu tennis shoes of the Budosaga mark", categories_id=3, user_id=1)
# session.add(itm3)
# session.commit()
#
# itm4 = Items(name="Basket Ball", description="Basketball", categories_id=7, user_id=1)
# session.add(itm4)
# session.commit()
#
# itm5 = Items(name="Skateboard", description="Skateboard", categories_id=9, user_id=1)
# session.add(itm5)
# session.commit()
#
# itm6 = Items(name="Goggles", description="Goggles used for swimming", categories_id=6, user_id=1)
# session.add(itm6)
# session.commit()

print "added categories"