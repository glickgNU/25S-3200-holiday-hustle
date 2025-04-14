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
@simple_routes.route('/fda/personalized_suggestions/presets', methods = ['PUT'])
def save_preset():
    current_app.logger.info('PUT /fda/personalized_suggestions/presets route')
    info = request.json
    preset_id = info['PresetID']
    name = info['Name']
    date = info['Date']
    user_id = info['UserID']
    suggestion_id = info['SuggestionID']

    query = '''
            UPDATE presets p
            JOIN personalizedSuggestions ps ON p.SuggestionID = ps.SuggestionID
            SET ps.GroupSize = %s
            WHERE p.PresetID = %s AND p.UserID = %s
            '''
    data = (name,date, user_id, suggestion_id, preset_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'preset saved!'
# ------------------------------------------------------------
@simple_routes.route('/users/subscription', methods = ['PUT'])
def update_subscription():
    current_app.logger.info('PUT /users/subscription route')
    user_info = request.json
    acc_id = user_info['AccountID']
    user_id = user_id['UserID']
    is_free = user_info['Free']
    is_pro = user_info['Pro']

    query = '''
            UPDATE subscription s
            JOIN accounts a ON s.AccountID = a.AccountID
            SET s.Pro = %s, s.Free = %s
            WHERE a.AccountID = %s AND a.UserID = %s
            '''
    data = (acc_id, user_id, is_free, is_pro)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'subscription updated!'

# PERSONA 4 ROUTES
#-----------------------------------------------------------------
@simple_routes.route('/users', methods=['DELETE'])
def remove_users():
    cursor = db.get_db().cursor()
    delete_query = '''
                UPDATE users u JOIN accounts on u.UserID = a.UserID
                SET u.MarkedForRemoval = TRUE
                WHERE u.LastSeen < DATE_SUB(NOW(), INTERVAL 3 YEARS);
                SELECT * FROM users WHERE users.MarkedForRemoval = TRUE;

                UPDATE users u JOIN accounts a on u.UserID = a.USERID
                SET u.MarkedForRemoval = FALSE
                WHERE u.UserID = 1;
                DELETE FROM users  WHERE users.MarkedForRemoval = TRUE;

                '''
    cursor.execute(delete_query)
    db.get_db().commit()
    response = make_response(jsonify({"message inactive users removed."}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------------
@simple_routes.route('/app/visuals', methods=['PUT'])
def update_interface():
    current_app.logger.info('PUT /app/visuals route')
    visual_info = request.json
    visual_id = visual_info['id']
    color = visual_info['color']
    shape = visual_info['shape']
    cursor = db.get_db().cursor()

    put_query = '''
                INSERT INTO visuals (VisualID, Color, Shape, IsWritable, Length, Width, SuggestionID)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                SELECT * FROM visuals;

                UPDATE visuals
                SET Color = %s, Shape = %s
                WHERE VisualID = %s;
                DELETE FROM visuals WHERE VisualID = %s;

                '''
    cursor.execute(put_query, (color, shape, visual_id))
    db.get_db().commit()

    response = make_response(jsonify({"message": f"Visual {visual_id} updated to color {color} and shape {shape}."}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions/presets', methods=['POST'])
def add_searches():
    



    