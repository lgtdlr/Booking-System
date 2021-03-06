import flask
from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt

from backend.controller.account import BaseAccount
from backend.controller.invitee import BaseInvitee
from backend.controller.room import BaseRoom
from backend.controller.event import BaseEvent
from backend.controller.occupies import BaseOccupiedTimeslot

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "ak1dd32jk4798khj&$#*H(jnd(N(#HNDDN999#RH9asd#nn5q"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)

CORS(app)


@app.route('/redpush/account', methods=['GET', 'POST'])
def handleAccounts():
    if request.method == 'GET':
        return BaseAccount().getAllAccounts()
    elif request.method == 'POST':
        result = BaseAccount().insertAccount(request.json)
        if result is None:
            return jsonify("Not registered"), 405
        return result
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
        return BaseRoom().addNewRoom(request.json)
    elif request.method == 'DELETE':
        return BaseRoom().deleteRoom(request.json['room_id'])
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
def handleEvents():
    if request.method == 'GET':
        return BaseEvent().getAllEvents()
    elif request.method == 'POST':
        return BaseEvent().addNewEvent(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/event/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def handleEventById(event_id):
    if request.method == 'GET':
        return BaseEvent().getEventById(event_id)
    elif request.method == 'PUT':
        return BaseEvent().updateEvent(event_id, request.json)
    elif request.method == 'DELETE':
        return BaseEvent().deleteEvent(event_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/event/delete-event', methods=['POST'])
def deleteEvent():
    if request.method == 'POST':
        return BaseEvent().deleteEvent(request.json['event_id'])
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/invitee', methods=['GET', 'POST'])
def handleInvitees():
    if request.method == 'GET':
        return BaseInvitee().getAllInvitees()
    elif request.method == 'POST':
        return BaseInvitee().insertInviteeWithJson(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/invitee/<int:event_id>', methods=['GET'])
def handleInviteesByEvent(event_id):
    if request.method == 'GET':
        return BaseInvitee().getAllInviteesByEvent(event_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/invitee/<int:event_id>/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def handleInviteeByUniqueId(event_id, account_id):
    if request.method == 'GET':
        return BaseInvitee().getInviteeByUniqueId(account_id, event_id)
    if request.method == 'PUT':
        return BaseInvitee().updateInvitee(account_id, event_id, request.json)
    if request.method == 'DELETE':
        return BaseInvitee().deleteInvitee(account_id, event_id)
    return jsonify("Method Not Allowed"), 405


@app.route('/redpush/invitee/delete-invitees', methods=['POST'])
def handleInviteesByUniqueId():
    if request.method == 'POST':
        return BaseInvitee().deleteInviteeWithJson(request.json)
    return jsonify("Method Not Allowed"), 405


@app.route('/redpush/timeslot', methods=['GET'])
def handleTimeslots():
    if request.method == 'GET':
        return BaseOccupiedTimeslot().getAllTimeslots()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/occupies', methods=['GET'])
def handleOccupiedTimeslots():
    if request.method == 'GET':
        return BaseOccupiedTimeslot().getAllOccupiedTimeslots()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/occupies/<int:event_id>', methods=['GET', 'POST'])
def handleOccupiedTimeslotsByEvent(event_id):
    if request.method == 'GET':
        return BaseOccupiedTimeslot().getAllOccupiedTimeslotsByEvent(event_id)
    elif request.method == 'POST':
        return BaseOccupiedTimeslot().insertOccupiedTimeslot(event_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/occupies/<int:event_id>/<int:timeslot_id>', methods=['GET', 'PUT', 'DELETE'])
def handleOccupiedTimeslotByUniqueId(event_id, timeslot_id):
    if request.method == 'GET':
        return BaseOccupiedTimeslot().getOccupiedTimeslotByUniqueId(timeslot_id, event_id)
    if request.method == 'PUT':
        return BaseOccupiedTimeslot().updateOccupiedTimeslot(timeslot_id, event_id, request.json)
    if request.method == 'DELETE':
        return BaseOccupiedTimeslot().deleteOccupiedTimeslot(timeslot_id, event_id)
    return jsonify("Method Not Allowed"), 405

@app.route('/redpush/account/login', methods=['GET', 'POST'])
def login():
    usernameInput = request.json['username']
    passwordInput = request.json['password']
    user = BaseAccount().getAccountByUsername(usernameInput)
    if user:
        password = user[0].json['password']
        if passwordInput == password:
            return jsonify(
                access_token=create_access_token(identity=user[0].json['account_id'],
                                                 additional_claims={"name": user[0].json['full_name'],
                                                                    "username": usernameInput,
                                                                    "role": user[0].json['role']}))
    return jsonify({"msg": "Incorrect username or password"}), 401


@app.route('/redpush/account/edit', methods=['PUT'])
@jwt_required()
def editInfo():
    user_id = get_jwt_identity()
    user_role = BaseAccount().getAccountById(user_id)

    return BaseAccount().updateAccount(user_id, request.json, user_role[0].json['role'])


@app.route('/redpush/account/edit-room', methods=['PUT'])
@jwt_required()
def editRoom():
   claims = get_jwt()
   role = claims["role"]
   if role != "Department Staff":
         return jsonify("The server understood the request, but is refusing to authorize it."), 403
   else:
        room_id = BaseRoom().getRoomIdByName(request.json['oldname'])
        return BaseRoom().updateRoom(room_id[0].json['room_id'], request.json)

@app.route('/redpush/account/delete-room', methods=['POST'])
@jwt_required()
def deleteRoom():
    claims = get_jwt()
    role = claims["role"]
    if role != "Department Staff":
        return jsonify("The server understood the request, but is refusing to authorize it."), 403
    else:
        room_id = BaseRoom().getRoomIdByName(request.json['name'])
        return BaseRoom().deleteRoom(room_id[0].json['room_id'])



# Operation 2: Find an available room (lab, classroom, study space, etc.) at a time frame
@app.route('/redpush/room/find-available-room', methods=['POST'])
def findAvailableRoom():
    if request.method == 'POST':
        return BaseRoom().findAvailableRoom(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 3: Find who appointed a room at a certain time
@app.route('/redpush/room/<room_name>/who-appointed-room', methods=['POST'])
def whoAppointedRoom(room_name):
    if request.method == 'POST':
        role = BaseAccount().getAccountRole(request.json)
        app.logger.info(role)
        if role == 'Department Staff':
            return BaseRoom().whoAppointedRoom(room_name, request.json)
        else:
            return jsonify("The server understood the request, but is refusing to authorize it."), 403
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 4: Give an all-day schedule for a room
@app.route('/redpush/room/<room_name>/schedule', methods=['POST'])
def getAllDaySchedule(room_name):
    if request.method == 'POST':
        role = BaseAccount().getAccountRole(request.json)
        app.logger.info(role)
        if role == 'Department Staff':
            return BaseRoom().getAllDaySchedule(room_name, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 5: Give an all-day schedule for a user
@app.route('/redpush/account/<username>/schedule', methods=['POST'])
def getUserSchedule(username):
    if request.method == 'POST':
        return BaseAccount().getUserSchedule(username, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Give all events and unavailable times of user
@app.route('/redpush/account/events', methods=['GET'])
@jwt_required()
def getUserEvents():
    if request.method == 'GET':
        account_id = get_jwt_identity()
        return BaseAccount().getUserEvents(account_id)
    else:
        return jsonify("Method Not Allowed"), 405

# Give all events and unavailable times of room
@app.route('/redpush/room/<int:room_id>/events', methods=['GET'])
def getRoomEvents(room_id):
    if request.method == 'GET':
        return BaseRoom().getRoomEvents(room_id)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 6: Create a meeting with 2+ people in a room
@app.route('/redpush/event/create-meeting', methods=['POST'])
@jwt_required()
def createMeeting():
    if request.method == 'POST':
        creator_id = get_jwt_identity()
        result = BaseEvent().addNewEvent(creator_id, request.json)
        BaseInvitee().insertInvitee(result[0].json['event_id'], creator_id, request.json)
        BaseOccupiedTimeslot().insertOccupiedTimeslot(result[0].json['event_id'], request.json)
        return BaseEvent().getEventById(result[0].json['event_id'])
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 8: Find a time that is free for everyone
@app.route('/redpush/account/find-available-time', methods=['POST'])
@jwt_required()
def findAvailableTime():
    if request.method == 'POST':
        creator_id = get_jwt_identity()
        return BaseAccount().findAvailableTime(request.json, creator_id)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 9: Allow user to mark time-space as ???Unavailable??? / "Available"
@app.route('/redpush/account/set-availability', methods=['POST'])
@jwt_required()
def setUserAvailability():
    if request.method == 'POST':
        account_id = get_jwt_identity()
        return BaseAccount().setAccountAvailability(account_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 9: Allow user to mark time-space as ???Unavailable??? / "Available"
@app.route('/redpush/account/set-availability-true', methods=['POST'])
@jwt_required()
def setUserAvailabilityTrue():
    if request.method == 'POST':
        account_id = get_jwt_identity()
        return BaseAccount().setAccountAvailabilityTime(account_id, request.json)
    else:
        return jsonify("Method Not Allowed"), 405


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
    else:
        return jsonify("Method Not Allow"), 405


@app.route('/redpush/event/busiest-hours', methods=['GET'])
def getBusyTimes():
    if request.method == 'GET':
        return BaseEvent().getBusiestTimesSlots()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/room/most-booked', methods=['GET'])
def getMostBookedRooms():
    if request.method == 'GET':
        return BaseRoom().geMostBookedRooms()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/account/booked-users', methods=['GET'])
def getMostBookedUsers():
    if request.method == 'GET':
        return BaseAccount().getMostBookedUser()
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/account/bookings-with-user', methods=['GET'])
@jwt_required()
def getMostBookingWithSelectedUser():
    if request.method == 'GET':
        account_id = get_jwt_identity()
        return BaseAccount().getMost_Booking_With_User(account_id)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/room/most-booked-room-by-user', methods=['GET'])
@jwt_required()
def getMostBookingInRoomWithSelectedUser():
    if request.method == 'GET':
        account_id = get_jwt_identity()
        return BaseRoom().geMostBookedRooms_by_user(account_id)
    else:
        return jsonify("Method Not Allowed"), 405


if __name__ == '__main__':
    app.run(debug=True)
