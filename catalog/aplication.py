from flask import Flask, render_template, request, redirect,\
    jsonify, url_for, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from catalog import db
from catalog.models import User, Categories, Items
from catalog.helpers import categories_to_json, get_category_list, get_google_authfrom flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "CatalogLand"


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps(
                "Token's client ID does not match app's."), 401)

        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; ' \
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).\
        filter_by(email=login_session['email']).one_or_none()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except Exception:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        redirect(url_for('principal'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        redirect(url_for('principal'))


@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Categories).all()
    for category in categories:
        items = session.query(Items).filter_by(categories_id=category.id).all()
        json_string = json.dumps([items.serialize for i in items])
    return jsonify(category.id, category.name, json_string)


@app.route('/catalog/<string:category_name>/JSON')
def catJSON(category_name):
    category = session.query(Categories)\
        .filter_by(name=category_name).one_or_none()
    items = session.query(Items).filter_by(categories_id=category.id)
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/item/<string:item_name>/JSON')
def menuItemJSON(category_id, item_name):
    category = session.query(Categories)\
        .filter_by(id=category_id).one_or_none()
    items = session.query(Items).filter_by(categories_id=category_id).all()
    return jsonify(Items=items.serialize, categories_id=category_id)


@app.route('/')
@app.route('/home')
def principal():
    categories = session.query(Categories).all()
    items = session.query(Items).order_by(asc(Items.name))
    if 'username' not in login_session:
        return render_template('publicmenu.html',
                               items=items,
                               categories=categories)
    else:
        return render_template('menu.html',
                               items=items,
                               categories=categories)


# Create a new item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Categories)
    if request.method == 'POST':
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        categories_id=request.form['Categories'],
                        user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % newItem.name)
        return redirect(url_for('principal'))
    else:
        return render_template('newitem.html', categories=category)


@app.route("/catalog/<string:category_name>/items")
def items(category_name):
    category = session.query(Categories)\
        .filter_by(name=category_name).one_or_none()
    items = session.query(Items).filter_by(categories_id=category.id)
    return render_template('items.html',
                           categories=category,
                           items=items,
                           category_name=category_name,
                           category_id=category.id)


@app.route('/catalog/<int:cat_id>/<string:item_name>')
def itemInfo(cat_id, item_name):
    category = session.query(Categories)\
        .filter_by(id=cat_id).one_or_none()
    item = session.query(Items)\
        .filter_by(name=item_name,
                   categories_id=cat_id).one_or_none()
    if 'username' not in login_session:
        return render_template('itemInfo.html',
                               categories= category,
                               item=item,
                               category_name=category.name,
                               category_id=cat_id,
                               item_name=item_name,
                               item_description=item.description)
    else:
        return render_template('itemChanges.html',
                               item=item,
                               category_name=category.name,
                               item_name=item_name,
                               item_description=item.description)


# Edit an Item
@app.route('/catalog/<string:items_name>/edit', methods=['GET', 'POST'])
def editItem(items_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items)\
        .filter_by(name=items_name).one_or_none()
    if login_session['user_id'] != editedItem.user_id:
        return "<script>" \
               "function myFunction() {" \
               "alert('Please create your own item...');}" \
               "</script>" \
               "<body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['categories']:
            editedItem.categories_id = request.form['categories']
        return redirect(url_for('itemInfo'))
    else:
        return render_template('editFile.html', item=editedItem)


# Delete an item
@app.route('/catalog/<string:items_name>/delete', methods=['GET', 'POST'])
def deleteItem(items_name):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Items)\
        .filter_by(name=items_name).one_or_none()
    if login_session['user_id'] != itemToDelete.user_id:
        return "<script>" \
               "function myFunction() {" \
               "alert('Please create your own item...');}" \
               "</script>" \
               "<body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('principal'))
    else:
        return render_template('deleteFile.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)