from flask import Flask, render_template,url_for, jsonify, abort, redirect, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Category, User, CatalogItem
from json import dumps
from datetime import datetime, timedelta
from flask import session as login_session
import random, string
import os
import jwt
from functools import wraps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
  open('client_secrets.json','r').read())['web']['client_id']
GOOGLE_SECRET = json.loads(
  open('client_secrets.json','r').read())['web']['client_secret']
TOKEN_SECRET = "1234secret"

app = Flask(__name__)
#engine = create_engine('postgresql+psycopg2://lolitschen:xxxxxxx@localhost/lolitschen')
engine = create_engine('postgresql+psycopg2:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Application Routes
@app.route("/")
def main():
	return render_template('index.html')


# API Routes

#USER ROUTES
@app.route("/api/v1.0/user/<int:user_id>/", methods=['GET'])
def get_user_profile(user_id):
  #get session
  DBSession = sessionmaker(bind = engine)
  session = DBSession()
  try:
    #try to query for user
    result = session.query(User).filter_by(id=user_id).first()
    #find all items belonging to this user
    listings = session.query(CatalogItem).filter_by(owner_id=user_id).all()
    data = []
    #organize data
    for item in listings:
      data.append(item.serialize())
    #return json
    return jsonify({'user': result.to_json(),'items':data})
  except NoResultFound:
    abort(401)
  finally:
    session.close()


#CATALOG_ITEM ROUTES
@app.route("/api/v1.0/item/", methods = ['GET','POST'])
def new_item():
  if request.method == 'POST':
    #null check
    if not request.json or not 'name' in request.json:
      abort(400)
    DBSession = sessionmaker(bind = engine)
    session = DBSession()

    #if creating item and category does not yet exist, create it.
    try:
        categ = session.query(Category).filter_by(name=request.json['category_name']).one()
    except NoResultFound:
        categ = Category(name = request.json['category_name'], description="")
        session.add(categ)
        session.commit()
    #create new item and persist it
    newItem = CatalogItem(name = request.json['name'], price=request.json['price'], description=request.json.get('description',""), owner_id=request.json['owner_id'], image=request.json['image'],category_id=categ.id)
    session.add(newItem)
    session.commit()
    session.close()
    return jsonify({'status':'success'})
  elif request.method == 'GET':
    #return all catalog items
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    items = session.query(CatalogItem).all()
    data = []
    for item in items:
        print item
        data.append(item.serialize())
    session.close()
    return jsonify({'items':data})
  else:
    abort(400)

@app.route("/api/v1.0/item/<int:item_id>/", methods = ['GET','PUT', 'DELETE'])
def test(item_id):
  if request.method == 'PUT':
    #PUT request for modifying existing item
    DBSession = sessionmaker(bind = engine)
    session = DBSession()


    try:
      #find item
      item = session.query(CatalogItem).filter_by(id=item_id).one()
      #replace item values with new values
      item.name = request.json['name']
      item.price = request.json['price']
      item.description = request.json['description']
      item.image = request.json['image']

      #check if category exists
      try:
        categ = session.query(Category).filter_by(name=request.json['category_name']).one()
      except NoResultFound:
      #create new category if not exist
        categ = Category(name = request.json['category_name'], description="")
        session.add(categ)

      #assign category id
      item.category_id = categ.id
      session.commit()
      return 'success'
    except NoResultFound:
        abort(404)
    finally:
        session.close()

  elif request.method == 'GET':
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    try:
      item = session.query(CatalogItem).filter_by(id=item_id).one()
      return jsonify({'item': item.to_json()})
    except NoResultFound:
      abort(404)
    finally:
      session.close()

  elif request.method == 'DELETE':
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    try:
      item = session.query(CatalogItem).filter_by(id=item_id).one()
      session.delete(item)
      session.commit()
    except NoResultFound:
        abort(404)
    finally:
        session.close()
  else:
    abort(400)


#CATEGORY ROUTES
@app.route("/api/v1.0/categories/", methods=['GET'])
def get_categories():
    #return all categories in db
    if request.method == 'GET':
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		categories = session.query(Category).all()
		data = []
		for c in categories:
			data.append(c.serialize())

		#print data
		session.close()
		return jsonify({'categories':data})
    else:
        abort(400)

@app.route("/api/v1.0/categories/new/", methods = ['GET', 'POST'])
def new_category():
  #create new category
	if request.method == 'POST':
		#print 'name' in request.form
		if not request.form or not 'name' in request.form:
			abort(400)
		newCategory = Category(name = request.form['name'], description=request.form.get('description',""))
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		session.add(newCategory)
		session.commit()
		session.close()
		#print 'closing session'
		return redirect(url_for('get_categories'), code=302)
	elif request.method == 'GET':
    #page for testing purposes
		return render_template('new_category_form.html')
	else:
		abort(400)

@app.route("/api/v1.0/categories/<int:category_id>/", methods=['GET'])
def get_category(category_id):
	DBSession = sessionmaker(bind = engine)
	session = DBSession()
	try:
		result = session.query(Category).filter_by(id=category_id).one()
		return jsonify({'category':result.serialize()})
	except NoResultFound:
		abort(404)
	finally:
		session.close()
		#print 'closing session'
@app.route("/api/v1.0/categories/<int:category_id>/edit/", methods=['GET', 'POST'])
def edit_category(category_id):
	if request.method == 'GET':
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		try:
			result = session.query(Category).filter_by(id=category_id).one()
			return render_template('edit_category.html', category = result)
		except NoResultFound:
			abort(404)
		finally:
			session.close()
	elif request.method == 'POST':
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		try:
			result = session.query(Category).filter_by(id=category_id).one()
			result.name = request.form['name']
			result.description = request.form['description']
			session.add(result)
			session.commit()
			return redirect(url_for('get_category',category_id=category_id),code=302)
		except NoResultFound:
			abort(404)
		finally:
			session.close()

		return 'test'
	else:
		abort(400)

#AUTH ROUTES
@app.route('/api/v1.0/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict(client_id=request.json['clientId'],
                   redirect_uri=request.json['redirectUri'],
                   client_secret=GOOGLE_SECRET,
                   code=request.json['code'],
                   grant_type='authorization_code')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    try:
    	user = session.query(User).filter_by(google=profile['sub']).first()
    finally:
    	session.close()
    if user:
        token = create_token(user)
        return jsonify(token=token)

    #create user object
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    u = User(google=profile['sub'],
             name=profile['name'],
             email=profile['email'],
             picture=profile['picture'])
    session.add(u)
    session.commit()
    token = create_token(u)

    return jsonify(token=token)

def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    # token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    token = jwt.encode(payload, TOKEN_SECRET)
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    # return jwt.decode(token, app.config['TOKEN_SECRET'])
    return jwt.decode(token, TOKEN_SECRET)

#helper functions

#error handling
@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error':'Not Found'}), 404)

if __name__ == "__main__":
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'

  app.debug = True
  app.run(host='0.0.0.0',port=8080)

#parse object to json
def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    json = {}
    json['fields'] = {}
    json['pk'] = getattr(model, 'id')

    for col in model._sa_class_manager.mapper.mapped_table.columns:
        json['fields'][col.name] = getattr(model, col.name)

    return dumps([json])
