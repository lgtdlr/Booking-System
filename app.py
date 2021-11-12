from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.account import BaseAccount
from controller.room import BaseRoom

app = Flask(__name__)
CORS(app)


@app.route('/redpush/account', methods=['GET', 'POST'])
def handleAccounts():
    if request.method == 'GET':
        return BaseAccount().getAllAccounts()
    elif request.method == 'POST':
        return BaseAccount().insertAccount(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/account/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def handleAccountById(account_id):
    if request.method == 'GET':
        return BaseAccount().getAccountById(account_id)
    elif request.method == 'PUT':
        return BaseAccount().updateAccount(account_id, request.json)
    elif request.method == 'DELETE':
        return BaseAccount().deleteAccount(account_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/room', methods=['GET', 'POST'])
def handleRooms():
    if request.method == 'GET':
        return BaseRoom().getAllRooms()
    elif request.method == 'POST':
        return BaseRoom().insertRoom(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/room/<int:room_id>', methods=['GET', 'PUT', 'DELETE'])
def handleRoomById(room_id):
    if request.method == 'GET':
        return BaseRoom().getRoomById(room_id)
    elif request.method == 'PUT':
        return BaseRoom().updateRoom(room_id, request.json)
    elif request.method == 'DELETE':
        return BaseRoom().deleteRoom(room_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/event', methods=['GET', 'POST'])
def handleEvents():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def handleEventById(event_id):  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event/invitees/<int:event_id>', methods=['GET', 'POST'])
def handleInvitees(event_id):  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event/invitees/<int:event_id>/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def handleInviteeById(event_id, account_id):  # put application's code here
    return 'Hello World!'


# Operation 8: Find a time that is free for everyone
@app.route('/redpush/account/find-available-time', methods=['GET'])
def findAvailableTime():
    if request.method == 'GET':
        return BaseAccount().findAvailableTime(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 9: Allow user to mark time-space as “Unavailable”
@app.route('/redpush/account/set-unavailable', methods=['PUT'])
def setAccountUnavailable():
    if request.method == 'PUT':
        return BaseAccount().setAccountUnavailable(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 9.1: Allow user to mark time-space as “Available”
@app.route('/redpush/account/set-available', methods=['DELETE'])
def setAccountAvailable():
    if request.method == 'DELETE':
        return BaseAccount().setAccountAvailable(request.json)
    else:
        return jsonify("Method Not Allow"), 405


# Operation 10: Only Department Staff can mark time-space as "Unavailable/Available" for any type of room
@app.route('/redpush/room/set-availability', methods=['POST'])
def setRoomAvailability():
    if request.method == 'POST':
        role = BaseAccount().getAccountRole(request.json)
        app.logger.info(role)
        if role == 'Department Staff':
            return BaseRoom().setRoomAvailability(request.json)
        else:
            return jsonify("The server understood the request, but is refusing to authorize it."), 403


if __name__ == '__main__':
    app.run(debug=True)
