import unittest
import json
from app import  app

class TestBookAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.books = []

    def test_post_book(self):
        book_data = {
            'title': 'sample_book',
            'author': 'test author',
            'publication_year': 2024,
            'ISBN': '12345'
        }
        response = self.app.post('/books', data=json.dumps(book_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], book_data['title'])
        self.assertEqual(data['author'], book_data['author'])


    def test_get_all_books(self):
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_book_by_id(self):
        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)


    def test_get_non_existent_book_by_id(self):
        response = self.app.get('/books/100')
        self.assertEqual(response.status_code, 404)

    def test_update_book_by_id(self):
        updated_data  = {
            'title': 'updated title',
            'author': 'updated author',
            'publication_year': 2023,
            'ISBN': '987456'
        }
        response = self.app.put('/books/1', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], updated_data['title'])


    def test_update_non_existent_book_by_id(self):
        updated_data = {
            'title': 'updated title',
            'author': 'updated author',
            'publication_year': 2023,
            'ISBN': '987456'
        }
        response = self.app.put('/books/100', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)


    def test_delete_book_by_id(self):
        response = self.app.delete('books/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual((data['message'], 'Book Deleted'))
    def test_delete_non_existent_book_by_id(self):
        response = self.app.delete('/books/100')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
