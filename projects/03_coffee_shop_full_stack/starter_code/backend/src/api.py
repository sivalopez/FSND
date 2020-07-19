import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN 
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    print('SL get_drinks() method.')
    drinks_list = Drink.query.all()
    print('SL get_drinks() query result: ' + str(len(drinks_list)))

    # If no drinks are found throw error 404.
    if len(drinks_list) == 0:
        abort(404)

    drinks = []
    for drink in drinks_list:
        print('SL get_drinks() - drink.recipe: [' + str(drink.recipe) + ']')
        drinks.append(drink.short())

    return jsonify({"success": True, "drinks": drinks})

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
def get_drinks_detail():
    print('SL get_drinks_detail() method.')
    drinks_list = Drink.query.all()

    # If no drinks are found throw error 404.
    if len(drinks_list) == 0:
        abort(404)

    drinks = []
    for drink in drinks_list:
        drinks.append(drink.long())
    return jsonify({"success": True, "drinks": drinks})

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
def create_drink():
    print('SL create_drink() method.')
    data = request.get_json()
    # If there is no data in the request throw 404 error.
    if data is None:
        abort(404)

    drink = [{
            'id': 1,
            'title': 'Chai',
            'recipe': [
                {'color': '#CCDDFF', 'name': 'grey', 'parts': '2'},
                {'color': '#8800FF', 'name': 'blue', 'parts': '1'}
            ]
        }]
    return jsonify({"success": True, "drinks": drink})

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['PATCH'])
def edit_drink(drink_id):
    print('SL edit_drink() drink_id: [' + drink_id + ']')
    drink = [{
        'id': 1,
        'title': 'Chai',
        'recipe': [
            {'color': '#CCDDFF', 'name': 'grey', 'parts': '2'},
            {'color': '#8800FF', 'name': 'blue', 'parts': '1'}
        ]
    }]
    return jsonify({"success": True, "drinks": drink})

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    print('SL delete_drink() method for drink_id: [' + drink_id + ']')
    return jsonify({"success": True, "delete": 2})

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({                    
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404  

@app.errorhandler(500)
def resource_not_found(error):
    return jsonify({                    
        "success": False, 
        "error": 500,
        "message": "internal server error"
    }), 500 

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''