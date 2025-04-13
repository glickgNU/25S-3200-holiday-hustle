from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create a new Blueprint object, which is a collection of 
# routes.
fda = Blueprint('fda', __name__)

# Get all employees from the system
@fda.route('/FoodDecorationsActivities', methods=['GET'])

def get_all_fda():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT Popularity, Pricing, Dates, Clicks, FDAID 
    FROM foodDecoActivities
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response


# Gets all the suggestions from the system
@fda.route('/FoodDecorationsActivities/suggestions', methods=['GET'])

def get_all_suggestions():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT SuggestionID, Allergies, GroupSize, AppID, Popularity, Audience
    FROM personalizedSuggestions
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response



# Gets 
@fda.route('/FoodDecorationsActivities', methods=['GET'])

def get_all_suggestions_FDA():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT SuggestionID , FDAID
    FROM suggestions_FDA
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response