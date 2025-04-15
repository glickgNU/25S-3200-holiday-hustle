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
@simple_routes.route('/users/complaints', methods = ['POST'])
def create_complaint():
    current_app.logger.info('POST /users/complaints route')
    info = request.json
    txt = info['ComplaintText']
    user_id = info['UserID']
    app_ID = info['AppID']
    id = info['ComplaintID']
    query = '''
    INSERT INTO complaints
    VALUES (%s, %s, %s, %s);
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (txt,user_id ,app_ID ,id))
    db.get_db().commit()
    response = make_response(jsonify({
        "message": "Complaint added succesfully"
    }))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
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
            WHERE p.PresetID = %s AND p.UserID = %s;
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
            WHERE a.AccountID = %s AND a.UserID = %s;
            '''
    data = (acc_id, user_id, is_free, is_pro)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'subscription updated!'

# PERSONA 2 ROUTES 
#2.1-----------------------------------------------------------------
@simple_routes.route('/inputs', methods=['GET'])
def get_made_input():
    cursor = db.get_db().cursor()
    query = '''
   SELECT DISTINCT ps.SuggestionID
   FROM  inputs i JOIN apps a on i.AppID = a.AppID
   JOIN personalizedSuggestions ps on a.AppID = ps.AppID;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#2.2-----------------------------------------------------------------
@simple_routes.route('/inputs/history', methods=['GET'])
def get_persons_input():
    cursor = db.get_db().cursor()
    query = '''
   SELECT DISTINCT ih.InputID
   FROM inputs i JOIN inputHistory ih on i.InputID = ih.inputID;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#2.3-----------------------------------------------------------------
@simple_routes.route('/inputs/history', methods=['DELETE'])
def delete_inputs():
    cursor = db.get_db().cursor()
    query = '''DELETE inputHistory
FROM inputHistory
   WHERE inputHistory.MarkedForRemoval = true;'''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#2.4-----------------------------------------------------------------
@simple_routes.route('/fda', methods=['GET'])
def fda_price_range(price):
    cursor = db.get_db().cursor()
    query = f'''
   SELECT fda.Pricing
   FROM personalizedSuggestions ps JOIN foodDecoActivities fda on ps.SuggestionID = fda.SuggestionID
   WHERE {price - 25} < fda.Pricing < {price + 25};
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#2.5-----------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions', methods=['GET'])
def given_suggestions_popular_fda(cut_off):
    cursor = db.get_db().cursor()
    query = f'''
   SELECT *
   FROM personalizedSuggestions ps JOIN foodDecoActivities f on ps.SuggestionID = f.SuggestionID
   ORDER BY f.Popularity
   LIMIT {cut_off};
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#2.6-----------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions', methods=['GET'])
def get_popular_personalized_suggestions(popularity_amount):
    cursor = db.get_db().cursor()
    query = f'''
    SELECT ps.Popularity
    FROM  personalizedSuggestions ps
    ORDER BY  ps.Popularity
    LIMIT {popularity_amount}; 
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

# PERSONA 3 ROUTES
#-----------------------------------------------------------------
@simple_routes.route('/fda/holiday', methods=['GET'])
def get_holiday_spending():
    cursor = db.get_db().cursor()
    query = '''
        SELECT h.Name AS HolidayName, AVG(f.Pricing) AS AvgSpending, SUM(f.Clicks) AS TotalClicks
        FROM foodDecoActivities f
        JOIN HolidayFDA hf ON f.FDAID = hf.FDAID
        JOIN holidays h ON hf.HolidayID = h.HolidayID
        GROUP BY h.Name
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
    
#-----------------------------------------------------------------
@simple_routes.route('/fda', methods=['GET'])
def get_popular_fda():
    cursor = db.get_db().cursor()
    query = '''
        SELECT f.FDAID, f.Popularity, f.Pricing, f.Dates, f.Clicks
        FROM foodDecoActivities f
        ORDER BY f.Popularity DESC, f.Clicks DESC
        LIMIT 10
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions', methods=['GET'])
def get_personalized_suggestions_analytics():
    cursor = db.get_db().cursor()
    query = '''
        SELECT s.GroupSize,
               AVG(f.Pricing) AS AvgBudget,
               CASE
                   WHEN s.GroupSize <= 5 THEN 'Casual Host'
                   ELSE 'Professional Planner'
               END AS HostType,
               AVG(f.Pricing) AS AvgSpending
        FROM personalizedSuggestions s
        JOIN SuggestionsFDA sf ON s.SuggestionID = sf.SuggestionID
        JOIN foodDecoActivities f ON sf.FDAID = f.FDAID
        GROUP BY s.GroupSize, HostType
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions/presets', methods=['GET'])
def get_presets_monthly():
    cursor = db.get_db().cursor()
    query = '''
        SELECT MONTH(p.Date) AS Month, COUNT(p.SuggestionID) AS TotalSuggestions
        FROM presets p
        GROUP BY MONTH(p.Date)
        ORDER BY Month
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions/export', methods=['GET'])
def export_user_selections():
    cursor = db.get_db().cursor()
    query = '''
        SELECT u.UserID, u.Name AS UserName, a.AppID, s.SuggestionID, s.Allergies, s.GroupSize, s.Popularity
        FROM users u
        JOIN accounts ac ON u.UserID = ac.UserID
        JOIN apps a ON ac.AppID = a.AppID
        JOIN personalizedSuggestions s ON s.AppID = a.AppID
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------------
@simple_routes.route('/fda/analysis', methods=['GET'])
def get_host_type_spending():
    """
    [Carlos-6] Return average spending grouped by host type:
    - 'Casual Host' if GroupSize <= 5
    - 'Professional Planner' otherwise
    """
    cursor = db.get_db().cursor()
    query = '''
        SELECT 
            CASE 
                WHEN s.GroupSize <= 5 THEN 'Casual Host'
                ELSE 'Professional Planner'
            END AS HostType,
            AVG(f.Pricing) AS AvgSpending
        FROM personalizedSuggestions s
        JOIN SuggestionsFDA sf ON s.SuggestionID = sf.SuggestionID
        JOIN foodDecoActivities f ON sf.FDAID = f.FDAID
        GROUP BY HostType;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
#-----------------------------------------------------------------------

# PERSONA 4 ROUTES
#-----------------------------------------------------------------
@simple_routes.route('/users', methods=['DELETE'])
def remove_users():
    current_app.logger.info('DELETE /users route')
    cursor = db.get_db().cursor()

    delete_query = '''
                DELETE u FROM users u
                JOIN accounts a ON u.UserID = a.UserID
                WHERE u.LastSeen < DATE_SUB(NOW(), INTERVAL 3 YEAR);
                '''
    cursor.execute(delete_query)
    db.get_db().commit()
    response = make_response(jsonify({"inactive users removed."}))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------------
@simple_routes.route('/fda/visuals', methods=['PUT'])
def update_interface():
    current_app.logger.info('PUT /app/visuals route')
    visual_info = request.json
    visual_id = visual_info['id']
    color = visual_info['color']
    shape = visual_info['shape']
    cursor = db.get_db().cursor()

    update_query = '''
                UPDATE visuals
                SET Color = %s, Shape = %s
                WHERE VisualID = %s;
                '''
    cursor.execute(update_query, (color, shape, visual_id))
    db.get_db().commit()
    response = make_response(jsonify({
        "message": "Visual updated successfully!",
        "visual_id": visual_id,
        "new_color": color,
        "new_shape": shape
    }))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#-----------------------------------------------------------------------
@simple_routes.route('/fda/personalized_suggestions/presets', methods=['POST'])
def add_searches():
    current_app.logger.info('POST /fda/personalized_suggestions/presets route')
    search_info = request.json
    field_name = search_info['field']
    search_type = search_info['type']
    suggestion_id = search_info['suggestion_id']
    user_id = search_info['user_id']  
    cursor = db.get_db().cursor()

    post_query = '''
                INSERT INTO presets (DATE, NAME, USERID, SUGGESTIONID)
                VALUES (NOW(), %s, %s, %s);
                '''
    cursor.execute(post_query, (field_name, user_id, suggestion_id))
    db.get_db().commit()
    response = make_response(jsonify({
        "message": "Search preset added successfully!",
        "field": field_name,
        "type": search_type,
        "suggestion_id": suggestion_id
    }))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#------------------------------------------------------------------------
@simple_routes.route('/user/subscription', methods=['POST'])
def add_monetization():
    current_app.logger.info('POST /user/subscription route')
    subscription_info = request.json
    pro_subscription = subscription_info['pro']
    free_subscription = subscription_info['free']
    account_id = subscription_info['account_id']
    cursor = db.get_db().cursor()

    post_query = '''
                INSERT INTO subscription (Pro, Free, AccountID)
                VALUES (%s, %s, %s);
                '''
    cursor.execute(post_query, (pro_subscription, free_subscription, account_id))
    db.get_db().commit()
    response = make_response(jsonify({
        "message": "Subscription added successfully!",
        "pro_subscription": pro_subscription,
        "free_subscription": free_subscription,
        "account_id": account_id
    }))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#------------------------------------------------------------------------
@simple_routes.route('/fda', methods=['POST'])
def display_events():
    current_app.logger.info('POST /fda route')
    event_info = request.json
    popularity = event_info['popularity']
    pricing = event_info['pricing']
    clicks = event_info['clicks']
    suggestion_id = event_info['suggestion_id']
    holiday_id = event_info['holiday_id']
    cursor = db.get_db().cursor()

    post_query = '''
                INSERT INTO foodDecoActivities (Popularity, Pricing, Dates, Clicks, SuggestionID, HolidayID)
                VALUES (%s, %s, NOW(), %s, %s, %s);
                '''
    cursor.execute(post_query, (popularity, pricing, clicks, suggestion_id, holiday_id))
    db.get_db().commit()

    select_query = '''
                SELECT * FROM foodDecoActivities
                ORDER BY Popularity DESC
                LIMIT 5;
                '''
    cursor.execute(select_query)
    top_events = cursor.fetchall()
    response = make_response(jsonify({
        "message": "Popular events",
        "top_events": top_events
    }))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response

#---------------------------------------------------------------------
@simple_routes.route('/users/complaints', methods=['GET'])
def track_complaints():
    current_app.logger.info('GET /users/complaints route')
    cursor = db.get_db().cursor()

    get_query = '''
            SELECT complaints.ComplaintText, COUNT(*) AS Frequency
            FROM complaints
            GROUP BY complaints.ComplaintText
            ORDER BY Frequency DESC;
            '''
    cursor.execute(get_query)
    complaint_data = cursor.fetchall()

    response = make_response(jsonify({
        "message": "Most common complaints",
        "complaints": complaint_data
    }))
    response.status_code = 200
    response.mimetype = 'application/json'
    return response
#-----------------------------------------------------------------------
