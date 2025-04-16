from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


# Create a new Blueprint object, which is a collection of 
# routes.
employees = Blueprint('employees', __name__)

@employees.route('/fda', methods=['GET'])
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


@employees.route('/fda/holiday', methods=['GET'])
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

@employees.route('/fda', methods=['GET'])
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

@employees.route('/fda/visuals', methods=['PUT'])
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

@employees.route('/fda', methods=['POST'])
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