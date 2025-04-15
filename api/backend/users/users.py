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


@users.route('/users/delete', methods=['DELETE'])

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

@users.route('/users/subscription', methods = ['PUT'])
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

@users.route('/users', methods=['DELETE'])
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

@users.route('/users/subscription', methods=['POST'])
def add_monetization():
    current_app.logger.info('POST /users/subscription route')
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

@users.route('/users/complaints', methods=['GET'])
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

@users.route('/users/complaints', methods = ['POST'])
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
