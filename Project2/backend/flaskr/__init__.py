import os
from unicodedata import category

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={'/': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(Res):
        Res.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        Res.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return Res
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def categ():
        try:
            All_Category = Category.query.all()
            Categories = [category.format() for category in All_Category]

            return jsonify({
                'success': True,
                'categories': Categories

            })
        except BaseException:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.


    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def Pages(Req, Select):
        Page = Req.args.get('page', 1, type=int)
        First = (Page - 1) * 10
        End = First + 10

        All_Questions = [question.format() for question in Select]
        Questions = All_Questions[First:End]

        return Questions

    @app.route('/questions')
    def All_Questions():
        try:
            Questions = Question.query.all()
            var = Pages(request, Questions)
            Categories = Category.query.all()

            List = {}
            for categories in Categories:
                List[categories.id] = categories.type

            return jsonify({
                'success': True,
                'questions': var,
                'total_questions': len(Questions),
                'categories': List

            })
        except BaseException:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:delete_question>', methods=['DELETE'])
    def delete(delete_question):
        try:
            ID = delete_question
            Delete_Question = Question.query.filter(
                Question.id == ID).one_or_none()

            Delete_Question.delete()

            return jsonify({
                'success': True,
                'deleted': ID

            })
        except BaseException:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/questions", methods=['POST'])
    def add_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        question = Question(question=new_question, answer=new_answer,
                            difficulty=new_difficulty, category=new_category)

        question.insert()

        return jsonify({
            'success': True,
            'created': question.id,
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/Seaching', methods=['POST'])
    def Searching_questions():

        Body = request.get_json()
        Search = Body.get('searchTerm', None)

        format = '%{}%'.format(Search)
        Results = Question.query.filter(Question.question.ilike(format)).all()
        print(Results)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in Results]

        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_for_category(id):
        Id_Num = str(id)
        retrive = Question.query.filter(Question.category == Id_Num).all()
        results = [question.format() for question in retrive]

        return jsonify({
            'success': True,
            'questions': results

        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def Play():

        Body = request.get_json()

        if not ('previous_questions' in Body or 'quiz_category' in Body):
            abort(422)

        previous_questions = Body.get('previous_questions')
        quiz_category = Body.get('quiz_category')
        ID = quiz_category['id']

        if (ID != 0):

            AllQuestion = Question.query.filter_by(category=ID).all()

        else:
            AllQuestion = Question.query.all()

        def RandomQuestion():
            RandomVar = AllQuestion[random.randrange(0, len(AllQuestion), 1)]
            return RandomVar

        def UsedQuestion(questionVal):
            Randoms = False
            for var in previous_questions:
                if (var == questionVal.id):
                    Randoms = True

            return Randoms

        Val = RandomQuestion()

        while (UsedQuestion(Val)):
            Val = RandomQuestion()

            if (len(previous_questions) == len(AllQuestion)):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'success': True,
            'question': Val.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(422)
    def Unprocessable(Error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(404)
    def NotFound(Error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resouce Not Found"
        }), 404

    def BadRequest(Error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400

    return app
