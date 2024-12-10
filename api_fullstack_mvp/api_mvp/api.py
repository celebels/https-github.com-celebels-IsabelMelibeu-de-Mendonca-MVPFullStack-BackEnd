from datetime import datetime
from flask import Flask
from user_model import UserModel, Users, User
from book_model import BookModel, Books, Book
from dropped import DroppedModel, DroppedBooks
from liked import LikedModel,LikedBooks
from resources import db
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#swager 
from flask_swagger_ui import get_swaggerui_blueprint
SWAGGER_URL = '/api/docs'  
API_URL = 'http://petstore.swagger.io/v2/swagger.json'




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


CORS(app, resources={r"/api/*": {" http://127.0.0.1:5000": "*"}})

CORS(app)

api = Api(app)

api.add_resource(Users,'/api/users/')
api.add_resource(User, '/api/user/<int:usr_id>') # find this user on the HTML link

api.add_resource(Books,'/api/books/')
api.add_resource(Book, '/api/book/<int:book_id>') # find this book on the HTML link


#bridge tables - between User and Books
api.add_resource(DroppedBooks,'/api/user/<int:usr_id>/dropped_books') #ALL BOOKS dropped
#api.add_resource(DroppedBook, '/api/user/<int:usr_id>/dropped_books/<int:book_id>') #specific dropped book by user


api.add_resource(LikedBooks,'/api/user/<int:usr_id>/liked_books') #ALL BOOKS liked by specific user
#api.add_resource(LikedBook, '/api/user/<int:usr_id>/liked_books/<int:book_id>') #specific liked book by user



@app.route('/')
def home():
    return 'fucken flask'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)


if __name__ == '__main__':
   app.run(debug=True)

