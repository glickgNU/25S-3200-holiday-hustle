from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)

# Get all employees from the system
@users.route('/users', methods=['GET'])

def get_all_users():

    cursor = db.get_db().cursor()
    the_query = '''SELECT UserID,
    Name, LastSeen, MarkedForRemoval FROM users
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response


@users.route('/users', methods=['DELETE'])

def remove_users():
    cursor = db.get_db().cursor()
    the_query = '''UPDATE users u JOIN accounts a on u.UserID = a.UserID
    SET u.MarkedForRemoval = TRUE
    WHERE u.LastSeen < DATE_SUB(NOW(), INTERVAL 3 YEAR);
    SELECT * FROM users WHERE users.MarkedForRemoval = TRUE;
    DELETE FROM users u
    WHERE u.MarkedForRemoval = true;
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response