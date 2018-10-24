from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def principal():
    categories = session.query(Categories)
    creator = getUserInfo(categories.user_id)
    items = session.query(Items).order_by(desc(Items.name))
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', items=items, categories=categories, creator=creator)
    else:
        return render_template('menu.html', items=items, categories=categories, creator=creator)


@app.route('/catalog/<string:categories_name>/items')
def itemMenu(categories_name):
    if 'username' not in login_session:
        return redirect('/login')
    categories= session.query(Categories)


# Create a new menu item
@app.route('/restaurant/<int:categories_id>/menu/new/', methods=['GET', 'POST'])
def newItem(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Categories).filter_by(id=categories_id).one()
    if login_session['user_id'] != categories.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add menu items to this restaurant. Please create your own restaurant in order to add items.');}</script><body onload='myFunction()'>"
        if request.method == 'POST':
            newItem = Items(name=request.form['name'], description=request.form['description'], categories_id=categories_id, user_id=categories.user_id)
            session.add(newItem)
            session.commit()
            flash('New Menu %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showMenu', categories_id=categories_id))
    else:
        return render_template('newitem.html', categories_id=categories_id)

# Edit a menu item


@app.route('/restaurant/<int:categories_id>/menu/<int:items_id>/edit', methods=['GET', 'POST'])
def editMenuItem(categories_id, items_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items).filter_by(id=items_id).one()
    categories = session.query(Categories).filter_by(id=categories_id).one()
    if login_session['user_id'] != categories.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit menu items to this restaurant. Please create your own restaurant in order to edit items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', categories_id=categories_id))
    else:
        return render_template('editmenuitem.html', categories_id=categories_id, items=items_id, item=editedItem)


# Delete a menu item
@app.route('/restaurant/<int:categories_id>/menu/<int:items.id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(categories_id, items_id):
    if 'username' not in login_session:
        return redirect('/login')
    categories = session.query(Categories).filter_by(id=categories_id).one()
    itemToDelete = session.query(Items).filter_by(id=items_id).one()
    if login_session['user_id'] != categories.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete menu items to this restaurant. Please create your own restaurant in order to delete items.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', categories_id=categories_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)