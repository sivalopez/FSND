import os
import sys
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

    # If no drinks are found throw error 404.
    if len(drinks_list) == 0:
        abort(404)

    try:
        drinks = []
        for drink in drinks_list:
            drinks.append(drink.short())
    except:
        print(sys.exc_info())
        abort(422)

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
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
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
@requires_auth('post:drinks')
def create_drink(payload):
    print('SL create_drink() method.')
    data = request.get_json()
    # If there is no data in the request throw 404 error.
    if data is None:
        abort(404)
    
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    if title is None:
        abort(404)

    if recipe is None:
        abort(404)

    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    except:
        print(sys.exc_info())
        abort(422)

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
@requires_auth('patch:drinks')
def edit_drink(payload, drink_id):
    print('SL edit_drink() drink_id: [' + drink_id + ']')

    data = request.get_json()
    print('SL edit_drink() data: ' + str(data))
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    if drink_id is None:
        abort(404)

    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
    except:
        abort(422)
    
    return jsonify({"success": True, "drinks": [drink.long()]})

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
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    print('SL delete_drink() method for drink_id: [' + drink_id + ']')

    if drink_id is None:
        abort(404)
    
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()
    except:
        abort(422)

    return jsonify({"success": True, "delete": 2})

## Error Handling
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
@app.errorhandler(AuthError)
def auth_error(authError):
    return jsonify({
        "success": False,
        "error": authError.error['code'],
        "message": authError.error['description']
    }), authError.status_code