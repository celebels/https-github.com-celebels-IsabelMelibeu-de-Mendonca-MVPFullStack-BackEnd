from datetime import datetime
from resources import db
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask import Flask



#in order to know the shape of db
class BookModel(db.Model):
    __tablename__ = 'book_model'
    #creating columns of db
    book_id= db.Column(db.Integer, primary_key = True,autoincrement=True)
    book_name= db.Column(db.String, unique = True, nullable = False)
    book_author= db.Column(db.String, unique = False, nullable = False)
    book_genre = db.Column(db.String(1), nullable=False)
    interactive_type= db.Column(db.String, nullable=False)
    last_time_posted = db.Column(db.DateTime, default=datetime.now())
   


    def __repr__(self):
        return f"Book(name = {self. book_name}, book_author={self.book_author}, book_genre={self. book_genre},   interactive_type={self.interactive_type}, logged: {self.last_time_posted})"



book_args = reqparse.RequestParser()
book_args.add_argument('book_name', type=str, required=True,
                        help='Name cant be blank')
book_args.add_argument('book_author', type=str, required=True,
                       help="author can't be blank")
book_args.add_argument('book_genre', type=str, required=True,
                       help="genre can't be blank")
book_args.add_argument('interactive_type', type=str, required=True,
                       help="this can't be blank")


#definitions of user in JSON data
bookFields = {
    'book_id': fields.Integer,
    'book_name':fields.String,
    'book_author': fields.String,
    'book_genre': fields.String(1),
    'interactive_type': fields.String,
    'last_time_posted' : fields.DateTime
}
#userField is what is expected to sent back and data is send

#users db
class Books(Resource):
    @marshal_with(bookFields)
    def get(self):
        books= BookModel.query.all()
        return books # when we sent a get request, we should get the books
    
    @marshal_with(bookFields)
    def post(self):
        args = book_args.parse_args()

        interactive_books_accepted=["ebook", "audiobook", "podcast","physical"]
        if args['interactive_type'] not in  interactive_books_accepted:
            abort(400, "invalid input baby")

        book=BookModel(book_name=args['book_name'], 
                       book_author=args['book_author'],
                        book_genre=args['book_genre'],
                        interactive_type=args['interactive_type'])
        db.session.add(book)
        db.session.commit()
        books=BookModel.query.all()
        return books, 201
    

#specific book based on id
class Book(Resource):
    @marshal_with(bookFields)
    def get(self,book_id):
        specific_book=BookModel.query.filter_by(book_id=book_id).first() #first found based on id
        if not specific_book:
            abort(404, "No book found, try again")
        return specific_book
