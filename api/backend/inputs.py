from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create a new Blueprint object, which is a collection of 
# routes.
inputs = Blueprint('personalized_suggestions', __name__)

# Get all employees from the system
@inputs.route('/inputs', methods=['GET'])

def get_all_inputs():

    cursor = db.get_db().cursor()
    the_query = '''
    SELECT AppID, Popularity, InputID
    FROM inputs
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response

@inputs.route('/inputs/restrictions', methods=['GET'])

def get_inputs_restrictions(allergies, groupSize, popularity):

    cursor = db.get_db().cursor()
    the_query = f'''
    SELECT DISTINCT ps.SuggestionID
    FROM  inputs i JOIN apps a on i.AppID = a.AppID
    JOIN personalizedSuggestions ps on a.AppID = ps.AppID
    WHERE ps.Allergies = {str(allergies)}
    AND ps.GroupSize = {groupSize}
    AND ps.Popularity  > {popularity - 2}
    AND ps.Popularity <  {popularity + 2};
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response

