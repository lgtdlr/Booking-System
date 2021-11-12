from flask import jsonify

from model.room import RoomDAO


class BaseRoom:

    def build_map_dict(self, row):
        result = {'room_id': row[0], 'name': row[1], 'type': row[2], 'role': row[3]}
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
        return jsonify(result_list), 200

    def getRoomById(self, room_id):
        dao = RoomDAO()
        room_tuple = dao.getRoomById(room_id)
        if not room_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200

    def insertRoom(self, json):
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
