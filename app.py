from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.account import BaseAccount


app = Flask(__name__)
CORS(app)


@app.route('/redpush/account', methods=['GET', 'POST'])
def handleAccounts():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/account/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def handleAccountById():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/room', methods=['GET', 'POST'])
def handleRooms():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/room/<int:room_id>', methods=['GET', 'PUT', 'DELETE'])
def handleRoomById():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event', methods=['GET', 'POST'])
def handleEvents():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def handleEventById():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event/invitees/<int:event_id>', methods=['GET', 'POST'])
def handleInvitees():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/event/invitees/<int:event_id>/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def handleInviteeById():  # put application's code here
    return 'Hello World!'


@app.route('/redpush/account/find-available-time', methods=['GET'])
def findAvailableTime():
    if request.method == 'GET':
        return BaseAccount().findAvailableTime(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == '__main__':
    app.run()
