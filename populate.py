from catalog import db
from catalog.models import Categories


def new_category(name):
    """
    new_category creates a new Category object given the name
    """
    category = Categories()
    category.name = name
    return category


def main():
    # list of category names
    categories = [
        'Soccer', 'Football', 'Snowboard',
        'Wu-shu', 'Swimming', 'Basketball',
        'Baseball', 'Skating']
    for c in categories:
        db.session.add(new_category(c))
    # save all categories to db
    db.session.commit()


if __name__ == '__main__':
    main()
