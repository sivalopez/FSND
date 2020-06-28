import os
import json
import random
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        formatted_categories = {category.id: category.type
                                for category in categories}

        return jsonify({
          'categories': formatted_categories,
          'success': True
        })

    '''
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id: category.type
                                for category in categories}

        return jsonify({
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': formatted_categories,
            'current_category': None,
            'success': True,
        })

    '''
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).first()
        if question is None:
            abort(404)
        try:
            question.delete()

            return jsonify({
                'success': True,
                'id': question_id
            })
        except:
            abort(422)

    '''
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        if data is None:
            print(sys.exc_info())
            abort(404)

        question = data.get('question', None)
        answer = data.get('answer', None)
        category = data.get('category', None)
        difficulty = data.get('difficulty', None)

        if question is None:
            print(sys.exc_info())
            abort(404)

        try:
            questionObj = Question(question=question,
                                   answer=answer, category=category,
                                   difficulty=difficulty)
            questionObj.insert()

            return jsonify({
                'success': True,
                'id': questionObj.id
            })
        except:
            print(sys.exc_info())
            abort(422)

    '''
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        if data is None:
            print(sys.exc_info())
            abort(404)

        searchTerm = data['searchTerm']

        try:
            questions = Question.query.filter(
                        Question.question.ilike('%' + searchTerm + '%'))\
              .order_by(Question.id).all()
            if not questions:
                abort(404)

            current_questions = paginate_questions(request, questions)
            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': None,
                'success': True,
            })
        except:
            abort(422)

    '''
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def get_by_category(category_id):
        questions = Question.query.filter_by(category=category_id)\
          .order_by(Question.id).all()
        if len(questions) == 0:
            abort(404)

        try:
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(422)

    '''
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/questions/quizzes', methods=['POST'])
    def get_next_question():
        data = request.get_json()
        if data is None:
            abort(404)

        # Get quiz_category from request data.
        # If id is 0, then we need to include all categories.
        quiz_category = data['quiz_category']['id']

        # Fetch questions based on the selected quiz_category
        if quiz_category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=quiz_category).all()

        if questions is None:
            abort(404)

        try:
            previous_questions = data['previous_questions']

            # If previous questions length is the same as questions,
            # then there are no more questions to get.
            if len(questions) == len(previous_questions):
                return jsonify({
                    'success': True
                })

            questionsSize = len(questions)
            randomIndex = random.randrange(questionsSize)
            next_question = questions[randomIndex]

            if len(previous_questions) != 0:
                for i in range(questionsSize):
                    if next_question.id in previous_questions:
                        randomIndex = random.randrange(questionsSize)
                        next_question = questions[randomIndex]

            return jsonify({
                'question': next_question.format(),
                'success': True
            })
        except:
            abort(422)

    '''
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(400)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Not Processable'
        }), 422

    return app
