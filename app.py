import logging
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_restful_swagger import swagger
import jwt

app = Flask(__name__)
# api = Api(app)
api = swagger.docs(Api(app), apiVersion='2.0', api_spec_url='/docs')

books = []
logging.basicConfig(filename='apilog', level=logging.INFO)

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True)
parser.add_argument('author', type=str, required=True)
parser.add_argument('publication_year', type=str, required=True)
parser.add_argument('ISBN', type=str, required=True)


class BookResource(Resource):
    @swagger.operation(
        notes='GET a book by id' ,
        responseClass=dict(id=int, title=str, author=str, publication_year=int,ISBN=str),
        nickname='get'
    )
    def get(self, book_id):
        book = next((b for b in books if b['id'] == book_id), None)
        if book:
            return book, 200
        else:
            return {'message': 'Book not found'}, 404

    @swagger.operation(
        notes='update a book by id',
        parameters = [
            {'name':"body",
             'description':'updated book',
             'required':True,
             'type':"Book",
             'param Type':'body',},
            {'name': 'book_id',
             'description': 'id of the book ',
             'required': True,
             'type': 'integer',
             'paramtype':'path'},
        ],
        responseClass=dict(id=int, title=str, author=str, publication_year=int, ISBN=str),
        nickname='put'
    )


    def put(self, book_id):
        args = parser.parse_args()
        book = next((b for b in books if b['id'] == book_id), None)
        if book:
            book.update(args)
            return book, 200
        else:
            return {'message': 'Book not found'}, 404

    @swagger.operation(
        notes='update a book by id',
        parameters=[
            {'name': "book_id",
             'description': 'ID of the book',
             'required': True,
             'type': "integer",
             'param Type': 'path', },
        ],
        responseClass=dict(id=int, title=str, author=str, publication_year=int, ISBN=str),
        nickname='delete'
    )
    def delete(self, book_id):
        global books
        books = [b for b in books if b['id'] != book_id]
        return {'message': 'Book deleted'}, 200

class BooksResource(Resource):
    @swagger.operation(
        notes='GET all books',
        responseClass=dict(id=int, title=str, author=str, publication_year=int, ISBN=str),
        nickname='get'
    )
    def get(self):
        return books, 200

    @swagger.operation(
        notes='update a book by id',
        parameters=[
            {'name': "body",
             'description': 'New book data',
             'required': True,
             'type': "Book",
             'param Type': 'body', },
        ],
        responseClass=dict(id=int, title=str, author=str, publication_year=int, ISBN=str),
        nickname='psot'
    )
    def post(self):
        args = parser.parse_args()
        new_book = {
            'id' : len(books) + 1,
            'title': args['title'],
            'author': args['author'],
            'publication_year': args['publication_year'],
            'ISBN': args['ISBN']

        }
        books.append(new_book)
        return new_book, 200

api.add_resource(BookResource,'/books/<int:book_id>')
api.add_resource(BooksResource, '/books')

def is_valid_isbn(isbn):
    if isinstance((isbn, str)):
        return True
    else:
        return False
def validate_token(token):
    try:
        payload = jwt.decode(token, algorithms=['HS256'])
        return  payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.before_request
def before_request():
    if request.endpoint == 'POST' or request.endpoint == 'PUT':
        isbn = request.json.get('ISBN')
        if not is_valid_isbn(isbn):
            return {'message': 'invalid ISBN format'}, 400


@app.before_request
def chcck_authentication():
    if request.endpoint != 'get':
        token = request.headers.get('Authorization')
        if token != f'Bearer {auth_token}':
            return {'message': 'Unauthorized'}



if __name__ == '__main__':
    app.run(debug=True)