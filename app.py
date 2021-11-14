from flask import Flask, request, jsonify
from flask_cors import CORS
from controller.account import BaseAccount
from controller.invitee import BaseInvitee
from controller.room import BaseRoom
from controller.event import BaseEvent

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
        return BaseRoom().addNewRoom(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


@app.route('/redpush/room/<int:room_id>', methods=['GET', 'PUT', 'DELETE'])
def handleRoomById(room_id):
    if request.method == 'GET':
        return BaseRoom().getRoomById(room_id)
    elif request.method == 'PUT':
        return BaseRoom().updateRoom(request.json)
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


@app.route('/redpush/invitee', methods=['GET', 'POST'])
def handleInvitees():
    if request.method == 'GET':
        return BaseInvitee().getAllInvitees()
    elif request.method == 'POST':
        return BaseInvitee().insertInvitee(request.json)
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


# Operation 2: Find an available room (lab, classroom, study space, etc.) at a time frame
@app.route('/redpush/room/find-available-room', methods=['GET'])
def findAvailableRoom():
    if request.method == 'GET':
        return BaseRoom().findAvailableRoom(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 3: Find who appointed a room at a certain time
@app.route('/redpush/room/<room_id>/who-appointed-room', methods=['GET'])
def whoAppointedRoom(room_id):
    if request.method == 'GET':
        role = BaseAccount().getAccountRole(request.json)
        app.logger.info(role)
        if role == 'Department Staff':
            return BaseRoom().whoAppointedRoom(request.json)
        else:
            return jsonify("The server understood the request, but is refusing to authorize it."), 403
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 4: Give an all-day schedule for a room
@app.route('/redpush/room/<room_id>/schedule', methods=['GET'])
def getAllDaySchedule(room_id):
    if request.method == 'GET':
        return BaseRoom().getAllDaySchedule(request.json)
    else:
        return jsonify("Method Not Allowed"), 405

# Operation 5: Give an all-day schedule for a user
@app.route('/redpush/account/<account_id>/schedule', methods=['GET'])
def getUserSchedule(account_id):
    if request.method == 'GET':
        return BaseAccount().getUserSchedule(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


#Operation 6: Create a meeting with 2+ people in a room
@app.route('/redpush/event/<creator_id>/create-meeting', methods=['POST'])
def createMeeting(creator_id):
    if request.method == 'POST':
        BaseInvitee().insertInvitee(request.json)
        
        return BaseEvent().addNewEvent(request.json)
    else:
        return jsonify("Method Not Allowed"), 405 


# Operation 8: Find a time that is free for everyone
@app.route('/redpush/account/find-available-time', methods=['GET'])
def findAvailableTime():
    if request.method == 'GET':
        return BaseAccount().findAvailableTime(request.json)
    else:
        return jsonify("Method Not Allowed"), 405


# Operation 9: Allow user to mark time-space as “Unavailable” / "Available"
@app.route('/redpush/account/set-availability', methods=['POST'])
def setUserAvailability():
    if request.method == 'POST':
        return BaseAccount().setAccountAvailability(request.json)
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

@app.route('/redpush/event/busiest-hours',methods=['GET'])
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

@app.route('/redpush/account/<int:account_id>/bookings-with-user', methods=['GET'])
def getMostBookingWithSelectedUser(account_id):
    if request.method == 'GET':
        return BaseAccount().getMost_Booking_With_User(account_id)
    else:
        return jsonify("Method Not Allowed"), 405



if __name__ == '__main__':
    app.run(debug=True)
