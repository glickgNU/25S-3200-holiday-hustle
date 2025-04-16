from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Create a new Blueprint object, which is a collection of 
# routes.
data_analysis = Blueprint('analysis', __name__)

@data_analysis.route('/fda/analysis', methods=['GET'])
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