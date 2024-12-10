#user dropped book

from datetime import datetime
from resources import db
from book_model import BookModel
from user_model import UserModel
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask import request,Flask



class DroppedModel(db.Model):
   #brigde between users and books
    dropped_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    usr_id= db.Column(db.Integer, db.ForeignKey('user_model.usr_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.book_id'))
    dropped_on = db.Column(db.DateTime, default=datetime.now())

    connection_user = db.relationship('UserModel', backref=db.backref('dropped_by_users', lazy=True))
    connection_book = db.relationship('BookModel', backref=db.backref('dropped_name_book', lazy=True))
    
    def __repr__(self):
        return f"Dropped books(usr_first_name = {self.connection_user.usr_first_name}, book_name={self.connection_book.book_name})"



dropped_books_args = reqparse.RequestParser()
dropped_books_args.add_argument('book_id', type=int, required=True,
                        help='book id cant be blank bb')
dropped_books_args.add_argument('usr_id', type=int, required=False,
                        help='user id cant be blank bb')



#definitions of user in JSON data
dropped_bookFields = {
    'dropped_id': fields.Integer,
    'book_id': fields.Integer,
    'usr_id':fields.Integer,
    'dropped_on' : fields.DateTime
}

class DroppedBooks(Resource):
    @marshal_with(dropped_bookFields)
    def get(self, usr_id):
        dropped_books = DroppedModel.query.filter_by(usr_id=usr_id).all()
        return dropped_books # when we sent a get request, we should get the books
    
    @marshal_with(dropped_bookFields)
    def post(self, usr_id):
        #args = dropped_books_args.parse_args()
        args=request.get_json()

        if"book_id" not in args:
            abort(400, "no book posted")

        usr = UserModel.query.filter_by(usr_id=usr_id).first()
        book = BookModel.query.get(args["book_id"])
        if not book:
            abort(404, "book not found")

        dropped_books=DroppedModel(book_id=args['book_id'], 
                                   usr_id=usr_id,
                                   dropped_on=datetime.now())
                       
        db.session.add(dropped_books)
        db.session.commit()
        dropped_books=DroppedModel.query.all()
        return dropped_books, 201
    
