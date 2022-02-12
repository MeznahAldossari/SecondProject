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
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.Question1 = {
            'question': 'Question1',
            'answer': 'Answer1',
            'difficulty': 1,
            'category': '3'
        }

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
    """
    def test_questions(self):

        Result = self.client().get('/questions')
        Loading = json.loads(Result.data)
        self.assertEqual(Result.status_code, 200)
        self.assertEqual(Loading['success'], True)


    def test_404_valid_page(self):

        Result = self.client().get('/questions?page=3000')
        Output = ['Resouce Not Found',404]
        return Output
        

        
    def test_for_gettingcategories(self):
        Result = self.client().get('/categories')
        Loading = json.loads(Result.data)
        self.assertEqual(Result.status_code, 200)
        self.assertEqual(Loading['success'], True)

        self.assertTrue(len(Loading['categories']))

   
    def test_404(self):

        Result = self.client().get('/categories/3000')
        Loading = json.loads(Result.data)
        self.assertEqual(Result.status_code, 404)
        self.assertEqual(Loading['success'], False)
        self.assertEqual(Loading['message'], 'Resouce Not Found')



    def test_for_insert_newquestion(self):
        
        Result = self.client().post('/questions', json=self.Question1)
        Loading = json.loads(Result.data)
        
        ID = Loading['created']
        Check = Question.query.filter_by(id=ID).one_or_none()
        self.assertEqual(Result.status_code, 200)
        self.assertEqual(Loading['success'], True)
        self.assertIsNotNone(Check)

    def test_for_insert_question(self):

        Result = self.client().post('/questions', json={})
        Output = ['Unprocessable',422]
        return Output
        


    def test_search(self):
        Sample = {'searchTerm': 'What'}
        Result = self.client().post('/questions', json=Sample)
        Loading = json.loads(Result.data)

        self.assertEqual(Result.status_code, 200)
        self.assertEqual(Loading['success'], True)

    def test_search_fails(self):
        Sample = {'searchTerm':'XXXXJJJAAKSOWEEP'
        }
    
        Result = self.client().post('/questions/Searching',json=Sample)
        Output = ['Resouce Not Found',404]
        return Output

        

    def test_for_questions_foreach_category(self):

        Result = self.client().get('/categories/2/questions')
        Loading = json.loads(Result.data)
        
        self.assertEqual(Result.status_code, 200)
        self.assertEqual(Loading['success'], True)
        self.assertTrue(len(Loading['questions']))

    def test_404_questions_for_category(self):
         
        Result = self.client().get('/categories/500/questions')
        Output = ['Bad Request',400]
        return Output



    def test_delete(self):
        Result = self.client().delete('/questions/11')
        self.assertEqual(Result.status_code, 200)

    def test_fails_delete(self):
        Result = self.client().delete('/questions/5555')
        self.assertEqual(Result.status_code, 422)


    
    def test_quiz(self):
        Sample =  {'previous_questions':[4,8],
        'quiz_category':{
            'type':'Sports',
            'id':6
        }}
        Result = self.client().post('/quizzes',json=Sample)
        Loading = json.loads(Result.data)

        self.assertEqual(Result.status_code, 200)
        self.assertEqual(Loading["success"], True)
        self.assertTrue(Loading['question'])
        self.assertEqual(Loading["question"]["category"], 6)

        self.assertNotEqual(Loading['question'],8)
        self.assertNotEqual(Loading['question'],4)

    def test_fails_for_quiz(self):
        
        Result = self.client().post('/quizzes',json={})
        Output = ['Bad Request',400]
        return Output
        

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()