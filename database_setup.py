#db configuration 
import sys
from sqlalchemy import Column, ForeignKey, Integer, Float, String, LargeBinary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

#class definitions
class Category(Base):
	__tablename__ = 'categories'
	name = Column(String(90), nullable = False)
	description = Column(String(255))
	id = Column(Integer, primary_key = True)

	def serialize(self):
    	#Returns object data in easily serializable format.
	    return {
	        'name': self.name,
	        'id': self.id,
	        'description': self.description,
	    }

class User(Base):
	__tablename__ = 'users'
	name = Column(String(90))
	email = Column(String(50))
	phone_number = Column(String(20))
	id = Column(Integer, primary_key = True)
	password = Column(String(120))
	google = Column(String(120))
	facebook = Column(String(120))
	github = Column(String(120))
	linkedin = Column(String(120))
	twitter = Column(String(120))
	picture = Column(String(120))

	def __init__(self, email=None, password=None, name=None, facebook=None, github=None, google=None, linkedin=None, twitter=None, picture=None):
		if email:
			self.email = email.lower()
		if password:
			self.set_password(password)
		if name:
			self.name = name
		if facebook:
			self.facebook = facebook
		if google:
			self.google = google
		if linkedin:
			self.linkedin = linkedin
		if twitter:
			self.twitter = twitter
		if picture:
			self.picture = picture

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def to_json(self):
		return dict(id=self.id, email=self.email, name=self.name,
			facebook=self.facebook, google=self.google,linkedin=self.linkedin, 
			twitter=self.twitter, picture=self.picture)

	def serialize(self):
    	#Returns object data in easily serializable format.
	    return {
	        'name': self.name,
	        'id': self.id,
	        'email': self.email,
	        'phone_number': self.phone_number
	    }

class CatalogItem(Base):
	__tablename__ = 'catalog_item'
	id = Column(Integer, primary_key = True)
	name = Column(String(90), nullable = False)
	price = Column(Float)
	description = Column(String(255))
	category_id = Column(Integer, ForeignKey('categories.id'))
	owner_id = Column(Integer, ForeignKey('users.id'))
	image = Column(LargeBinary)
	category = relationship(Category)
	user = relationship(User)

	def to_json(self):
		return dict(id=self.id, name=self.name, price=self.price, 
			description=self.description, category_id=self.category_id, 
			owner_id=self.owner_id, image=self.image)

	def serialize(self):
    	#Returns object data in easily serializable format.
	    return {
	    	'id': self.id,
	        'name': self.name,
	   		'price': self.price,
	   		'description': self.description,
	   		'category_id': self.category_id,
	   		'owner_id': self.owner_id,
	   		'image': self.image
	    }

#run db engine
#engine = create_engine('postgresql+psycopg2://lolitschen:xxxxxx@localhost/lolitschen')
engine = create_engine('postgresql+psycopg2:///catalog')
Base.metadata.create_all(engine)