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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','1234','localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question={
            'question': 'what is the name of the app',
            'answer': 'trivia',
            'difficulty': '3',
            'category': '3'
        
        }
        self.search={
            'searchTerm': 'what'               
        }
        self.space_search={
            'searchTerm': '   '               
        }
        self.quizzes={
            'previous_questions': ["9"],
            'quiz_category': {'type': 'Science', 'id': '1'}
                          
        }        
        self.error_quizzes={
            'previous_questions': [],
            'quiz_category': {'type': 'biology', 'id': ''}
                          
        }   
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

  


    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")


    def test_delete_questions(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter_by(id="2").one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Successfully deleted")
        self.assertEqual(question, None)

    def test_404_if_question_exists(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Cannot be processed")

    
    def test_add_questions(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Successfully added")

    def test_405_if_question_exists(self):
        res = self.client().post('/questions/32', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method is not allowed")

    

    def test_search_questions(self):
        res = self.client().post('/questions/search', json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertFalse(data['currentCategory'])

    def test_404_if_empty_space_is_searched(self):
        res = self.client().post('/questions/search', json=self.space_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")


    def test_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['currentCategory'])    

    def test_404_if_requested_beyond_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")        

    def test_quizzes(self):
        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))
        self.assertTrue(data['totalQuestions'])

    def test_422_if_quiz_category_does_not_exist(self):
        res = self.client().post('/quizzes', json=self.error_quizzes)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Cannot be processed")
            



    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()