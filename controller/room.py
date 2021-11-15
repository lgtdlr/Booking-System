from flask import jsonify

from model.room import RoomDAO


class BaseRoom:

    def build_map_dict(self, row):
        result = {'room_id': row[0], 'name': row[1], 'capacity': row[2], 'type': row[3]}
        return result

    def build_map_dict_most_bookings_in_room(self, row):
        result = {'room_id': row[0],
                  'name': row[1],
                  'capacity': row[2],
                  'type': row[3],
                  'room_uses': row[4]}
        return result

    def build_alt_map_dict(self, row):
        result = {'room_id': row[0], 'name': row[1], 'capacity': row[2], 'type': row[3], 'start_time': row[4],
                  'end_time': row[5], 'available': row[6]}
        return result

    def build_attr_dict(self, room_id, name, capacity, type):
        result = {'room_id': room_id, 'name': name, 'capacity': capacity, 'type': type}
        return result

    def getAllRooms(self):
        dao = RoomDAO()
        room_list = dao.getAllRooms()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getRoomById(self, room_id):
        dao = RoomDAO()
        room_tuple = dao.getRoomById(room_id)
        if not room_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200

    def addNewRoom(self, json):
        name = json['name']
        capacity = json['capacity']
        type = json['type']
        dao = RoomDAO()
        room_id = dao.insertRoom(name, capacity, type)
        result = self.build_attr_dict(room_id, name, capacity, type)
        return jsonify(result), 201

    def updateRoom(self, room_id, json):
        name = json['name']
        capacity = json['capacity']
        type = json['type']
        dao = RoomDAO()
        is_updated = dao.updateRoom(room_id, name, capacity, type)
        result = self.build_attr_dict(room_id, name, capacity, type)
        return jsonify(result), 200

    def deleteRoom(self, room_id):
        dao = RoomDAO()
        result = dao.deleteRoom(room_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def setRoomAvailability(self, json):
        room_id = json['room_id']
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        is_available = json['is_available']
        dao = RoomDAO()
        if is_available:
            result = dao.setRoomAvailable(room_id, date, start_time, end_time)
        else:
            result = dao.setRoomUnavailable(room_id, date, start_time, end_time)
        return jsonify(result), 200

    def findAvailableRoom(self, json):
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        dao = RoomDAO()
        result = dao.findAvailableRoom(start_time, end_time, date)
        return jsonify(result), 200

    def whoAppointedRoom(self, room_name, json):
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        dao = RoomDAO()
        result = dao.whoAppointedRoom(room_name, date, start_time, end_time)
        return jsonify(result), 200

    def getAllDaySchedule(self, room_name, json):
        date = json['date']
        dao = RoomDAO()
        result = dao.getAllDaySchedule(room_name, date)
        return jsonify(result), 200

    def geMostBookedRooms(self):
        dao = RoomDAO()
        rooms_list = dao.getMostBookedRooms()
        result_list = []
        for row in rooms_list:
            obj = self.build_map_dict_most_bookings_in_room(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def geMostBookedRooms_by_user(self, account_id):
        dao = RoomDAO()
        rooms_list = dao.get_most_bookings_in_room_by_user(account_id)
        result_list = []
        for row in rooms_list:
            obj = self.build_map_dict_most_bookings_in_room(row)
            result_list.append(obj)
        return jsonify(result_list), 200
