import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	
	parser = reqparse.RequestParser()
	parser.add_argument('username',
			type = str,
			required = True,
			help = "This field cannot be blank."
	)
	parser.add_argument('password',
			type = str,
			required = True,
			help = "This field cannot be blank."
	)

	def post(self):


		data = UserRegister.parser.parse_args()
		if UserModel.find_by_username(data['username']) :
			return {"message" : "User with that username already exists."}, 400

		user = UserModel(**data)	#unpacking same thing : data['username'], data['password']. We are sure because we are using a parser. And we will be having this and nothing else. 
		user.save_to_db()

		return {"message" : "User has been added successfully!"}, 201