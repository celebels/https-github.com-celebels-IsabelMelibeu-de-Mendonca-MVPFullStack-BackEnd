#user dropped book

from datetime import datetime
from resources import db
from book_model import BookModel
from user_model import UserModel
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask import request, Flask



class LikedModel(db.Model):
   #brigde between users and books
    liked_id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    usr_id= db.Column(db.Integer, db.ForeignKey('user_model.usr_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.book_id'))
    liked_on = db.Column(db.DateTime, default=datetime.now())

    connection_user = db.relationship('UserModel', backref=db.backref('liked_by_users', lazy=True))
    connection_book = db.relationship('BookModel', backref=db.backref('liked_name_book', lazy=True))
    
    def __repr__(self):
        return f"Liked books(usr_first_name = {self.connection_user.usr_first_name}, book_name={self.connection_book.book_name})"



liked_books_args = reqparse.RequestParser()
liked_books_args.add_argument('book_id', type=int, required=True,
                        help='book id cant be blank bb')
liked_books_args.add_argument('usr_id', type=int, required=True,
                        help='user id cant be blank bb')



#definitions of user in JSON data
liked_bookFields = {
    'liked_id': fields.Integer,
    'book_id': fields.Integer,
    'usr_id':fields.Integer,
    'liked_on' : fields.DateTime
}

    

#specific book based on id
class LikedBooks(Resource):
    @marshal_with(liked_bookFields)
    def get(self, usr_id):
        liked = LikedModel.query.filter_by(usr_id=usr_id).all()
        return liked # when we sent a get request, we should get the books
    
    @marshal_with(liked_bookFields)
    def post(self, usr_id):
        #args = dropped_books_args.parse_args()
        args=request.get_json()

        if"book_id" not in args:
            abort(400, "no book posted")

        usr = UserModel.query.filter_by(usr_id=usr_id).first()
        book = BookModel.query.get(args["book_id"])
        if not book:
            abort(404, "book not found")

        liked=LikedModel(book_id=args['book_id'], 
                                   usr_id=usr_id,
                                   liked_on=datetime.now())
                       
        db.session.add(liked)
        db.session.commit()
        liked=LikedModel.query.all()
        return liked, 201
    
