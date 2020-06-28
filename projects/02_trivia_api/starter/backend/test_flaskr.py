import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    # """
    def test_get_categories(self):
        res = self.client().get('/categories')
        rjson = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(rjson['success'], True)
        self.assertGreater(len(rjson['categories']), 0)

    def test_get_questions(self):
        res = self.client().get('/questions')
        rjson = res.json
        self.assertEqual(res.status_code, 200)
        self.assertEqual(rjson['success'], True)
        self.assertGreaterEqual(rjson['total_questions'], len(rjson['questions']))

    def test_delete_question(self):
        #Add a question and then delete it.
        newQuestion = {'question': 'What is the currency in Japan?',\
            'answer': 'Japanese Yen', 'category': 3, 'difficulty': 1}
        res = self.client().post('/questions', data=json.dumps(newQuestion),\
            headers={'Content-Type': 'application/json'})
        del_res = self.client().delete('/questions/' + str(res.json['id']))
        self.assertEqual(del_res.status_code, 200)
        self.assertEqual(del_res.json['success'], True)
        self.assertEqual(del_res.json['id'], str(res.json['id']))


    def test_add_question(self):
        newQuestion = {'question': 'Where is Opera House?', 'answer': 'Sydney', 'category': 2, 'difficulty': 1}
        res = self.client().post('/questions', data=json.dumps(newQuestion), \
            headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'], True)
        # Assert that question is persisted by checking the id is present.
        self.assertIsNotNone(res.json['id'])

    def test_search_questions(self):
        searchTerm = {'searchTerm': 'Who'}
        res = self.client().post('/questions/search', data=json.dumps(searchTerm),\
            headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'], True)
        self.assertGreater(res.json['total_questions'], 1)

    def test_search_questions_wrong_method(self):
        searchTerm = {'searchTerm': 'Who'}
        res = self.client().get('/questions/search', data=json.dumps(searchTerm),\
            headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['message'], 'Method Not Allowed')

    def test_search_questions_error(self):
        searchTerm = {'searchTerm': 'Who'}
        res = self.client().post('/questions/search', \
            headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['message'], 'Bad Request')

    def test_search_questions_not_found(self):
        searchTerm = {'searchTerm': 'Siva'}
        res = self.client().post('/questions/search', data=json.dumps(searchTerm),\
            headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['message'], 'Not Processable')
    
    def test_questions_by_category(self):
        category = 3
        res = self.client().get('/categories/{}/questions'.format(category))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'], True)
        self.assertGreater(res.json['total_questions'], 1)

    def test_questions_by_category_not_found(self):
        category = 9
        res = self.client().get('/categories/{}/questions'.format(category))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json['success'], False)
        self.assertEqual(res.json['message'], 'Resource Not Found')

    def test_get_next_question(self):
        quizCriteria = {
            "quiz_category": {"type": "Science", "id":"1"}, \
                "previous_questions": [13]\
                    }
        res = self.client().post('/questions/quizzes', \
            headers={'Content-Type': 'application/json'}, \
                data=json.dumps(quizCriteria))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['success'], True)
        self.assertGreater(len(res.json['question']), 0)

    def test_bad_request(self):
        res = self.client().post('/questions', data="question=something&answer=theanswer",\
            headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 400)

    def test_resource_not_found(self):
        res = self.client().get('/category')
        self.assertEqual(res.status_code, 404)

    def test_method_not_allowed(self):
        res = self.client().get('/questions/search')
        self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()