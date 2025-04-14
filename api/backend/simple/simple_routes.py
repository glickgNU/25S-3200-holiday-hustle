from flask import Blueprint, request, jsonify, make_response, current_app, redirect, url_for
import json
from backend.db_connection import db
from backend.simple.playlist import sample_playlist_data

# This blueprint handles some basic routes that you can use for testing
simple_routes = Blueprint('simple_routes', __name__)


# ------------------------------------------------------------
# / is the most basic route
# Once the api container is started, in a browser, go to 
# localhost:4000/playlist
@simple_routes.route('/')
def welcome():
    current_app.logger.info('GET / handler')
    welcome_message = '<h1>Welcome to the CS 3200 Project Template REST API'
    response = make_response(welcome_message)
    response.status_code = 200
    return response

# ------------------------------------------------------------
# /playlist returns the sample playlist data contained in playlist.py
# (imported above)
@simple_routes.route('/playlist')
def get_playlist_data():
    current_app.logger.info('GET /playlist handler')
    response = make_response(jsonify(sample_playlist_data))
    response.status_code = 200
    return response

# ------------------------------------------------------------ 
@simple_routes.route('/niceMessage', methods = ['GET'])
def affirmation():
    message = '''
    <H1>Think about it...</H1>
    <br />
    You only need to be 1% better today than you were yesterday!
    '''
    response = make_response(message)
    response.status_code = 200
    return response

@simple_routes.route("/hello")
def hello():
    message = "<H1>Hellow CS 3200</H1>"
    response = make_response(message)
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Demonstrates how to redirect from one route to another. 
@simple_routes.route('/message')
def mesage():
    return redirect(url_for(affirmation))
# PERSONA 1 ROUTES
# ------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions', methods = ['GET'])
def get_personalized_suggestions():
    cursor = db.get_db().cursor()
    the_query = '''
    SELECT ps.SuggestionID, ps.GroupSize, FDA.pricing
    FROM personalizedSuggestions ps
    JOIN foodDecoActivities FDA on ps.SuggestionID = FDA.SuggestionID
    WHERE ps.GroupSize >= %s
    AND FDA.Pricing <= %s
    '''
    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response

# ------------------------------------------------------------
@simple_routes.route('/complaints', methods = ['POST'])
def create_complaint():
    return 
# ------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions/ presets', methods = ['PUT'])
def save_preset():
    return 
# ------------------------------------------------------------
@simple_routes.route('/users/subscription', methods = ['PUT'])
def update_subscription():
    current_app.logger.info('PUT /users/subscription route')
    user_info = request.json
    user_id = user_info['id']
    sub = user_info['subscription']

    query = '''
            UPDATE subscription s 
            JOIN accounts a ON s.AccountID = a.AccountID 
            SET s.Pro = TRUE, s.Free = FALSE
            WHERE a.AccountID = %s AND a.UserID = %s
            '''
    data = (sub, user_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'subscription updated!'