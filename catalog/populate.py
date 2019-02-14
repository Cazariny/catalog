from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from catalog.models import Base, Categories

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
        user_id=1
    )
    session.add(category_input)
    session.commit()

print "added categories"