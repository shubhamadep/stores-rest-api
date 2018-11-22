from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

#JWT - json web talk

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	#flask was tracking the our data objects, but now sqlalchemy has its own tracker which it can use, so we turn off this one.
app.secret_key = 'shubham'
api = Api(app)

#To create the tables using sqlalchemy, and not use the script create_tables.py. Use the following.
@app.before_first_request
def create_tables():
	db.create_all()


jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':      # Because we dont want to run the app if we are using app.py for importing stuff.
	from db import db 			# Needs to be here, because of circular imports.
	db.init_app(app)
	app.run(port=5003, debug=True)

