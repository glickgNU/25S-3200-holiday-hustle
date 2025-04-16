from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


# Create a new Blueprint object, which is a collection of 
# routes.
personal_suggestions = Blueprint('personal_suggestions', __name__)

@personal_suggestions.route('/fda/personal_suggestions/presets', methods = ['PUT'])
def save_preset():
    current_app.logger.info('PUT /fda/personal_suggestions/presets route')
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
  
@personal_suggestions.route('/fda/personal_suggestions', methods=['GET'])
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

@personal_suggestions.route('/fda/personal_suggestions/popular', methods=['GET'])
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

@personal_suggestions.route('/fda/personal_suggestions', methods=['GET'])
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

@personal_suggestions.route('/fda/personal_suggestions/presets', methods=['GET'])
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


@personal_suggestions.route('/fda/personal_suggestions/export', methods=['GET'])
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

@personal_suggestions.route('/fda/personal_suggestions/presets', methods=['POST'])
def add_searches():
    current_app.logger.info('POST /fda/personal_suggestions/presets route')
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
    response.status_code = 201
    response.mimetype = 'application/json'
    return response

