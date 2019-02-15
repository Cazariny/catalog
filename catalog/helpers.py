from catalog.models import Categories, Items

def categories_to_json(categories):
    """
    categories_to_json converts categories SQLAlchemy object to json object
    works by simply looping over collection of objects and manually mapping
    each Object key to a native Python dict
    """
    main = {}
    main['categories'] = []
    for cat in categories:
        catDict = {}
        catDict['id'] = cat.id
        catDict['name'] = cat.name
        catDict['items'] = []
        for item in cat.items:
            itemDict = {}
            itemDict['id'] = item.id
            itemDict['title'] = item.title
            itemDict['description'] = item.description
            catDict['items'].append(itemDict)
        main['categories'].append(catDict)
    return main


def get_category_list():
    """
    get_category_list returns list of all categories
    """
    return [c.name for c in Categories.query.all()]