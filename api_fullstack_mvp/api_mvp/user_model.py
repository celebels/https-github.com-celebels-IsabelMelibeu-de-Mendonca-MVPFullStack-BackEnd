from datetime import datetime
from resources import db
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask import Flask



#in order to know the shape of db
class UserModel(db.Model):
    __tablename__="user_model"
    #creating columns of db
    usr_id= db.Column(db.Integer, primary_key = True,autoincrement=True)
    usr_first_name= db.Column(db.String, unique = True, nullable = False)
    email= db.Column(db.String, unique = True, nullable = False)
    is_premium = db.Column(db.Boolean, nullable=True)
    last_time_logged = db.Column(db.DateTime, default=datetime.now())
   
    def __repr__(self):
        return f"User(name = {self.usr_first_name}, email={self.email}, is_premium={self.is_premium}, logged: {self.last_time_logged})"



user_args = reqparse.RequestParser()
user_args.add_argument('usr_first_name', type=str, required=True,
                        help='Name cant be blank')
user_args.add_argument('email', type=str, required=True,
                       help="Email can't be blank")
user_args.add_argument('is_premium', type=bool, required=False,
                       help="Email can't be blank")


#definitions of user in JSON data
userFields = {
    'usr_id': fields.Integer,
    'usr_first_name':fields.String,
    'email': fields.String,
    'is_premium': fields.Boolean,
    'last_time_logged' : fields.DateTime
}
#userField is what is expected to sent back and data is send

#users db
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users= UserModel.query.all()
        return users # when we sent a get request, we should get the users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user=UserModel(usr_first_name=args['usr_first_name'], 
                       email=args['email'], is_premium=args['is_premium'])
        db.session.add(user)
        db.session.commit()
        users=UserModel.query.all()
        return users, 201
    

#specific user based on id
class User(Resource):
    @marshal_with(userFields)
    def get(self,usr_id):
        specific_user=UserModel.query.filter_by(usr_id=usr_id).first() #first found based on id
        if not specific_user:
            abort(404, "No user found, try again")
        return specific_user
