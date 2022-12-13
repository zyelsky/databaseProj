from flask import Blueprint, jsonify, make_response, request
from src import db

user_blueprint = Blueprint('user_blueprint', __name__)


# Get all the dependents that the user oversees
@user_blueprint.route('/user/<id>', methods=['GET'])
def get_dependents(id):
    cursor = db.get_db().cursor()

    cursor.execute('SELECT d.userID, d.hasBalance FROM Individual i JOIN Dependents d ON i.userID =\
      d.parentID WHERE d.parentID = {0}'.format(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    data = cursor.fetchall()
    for row in data:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get requests to display the current funds
@user_blueprint.route('/user/funds/<userID>', methods=['GET'])
def get_dependents(userID):
    cursor = db.get_db().cursor()

    cursor.execute('SELECT i.hasBalance FROM Individual i WHERE i.userID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    data = cursor.fetchall()
    for row in data:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# get request for budget

@user_blueprint.route('/user/budget/<userID>', methods=['GET'])
def get_budget(userID):
    cursor = db.get_db().cursor()

    cursor.execute('SELECT b.category, bal.currentFunds FROM Individual i JOIN Balance bal\
     ON i.hasBalance = bal.balanceID JOIN Budget b ON b.budgetID = bal.balanceID\
      WHERE i.userID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    data = cursor.fetchall()
    for row in data:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# post requests to add funds to a particular budget for independent and dependent
# (ex. post request for an independent to add that they just spent x dollars on groceries)

