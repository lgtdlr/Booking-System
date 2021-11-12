from flask import jsonify
from model.room import RoomsDAO

class BaseRoom:

    def build_map_dict(self, row):
        result = {'room_id': row[0], 'name': row[1], 'capacity': row[2], 'type': row[3]}
        return result

    def build_attr_dict(self, room_id,name, capacity, type):
        result = {'room_id': room_id, 'name': name, 'capacity': capacity, 'type': type}
        return result

    def getAllRooms(self):
        dao = RoomsDAO()
        room_list = dao.getAllRooms()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getRoomById(self, pid):
        dao = RoomsDAO()
        room_tuple = dao.getRoomById(pid)
        if not room_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(room_tuple)
            return jsonify(result), 200

    def addNewRoom(self, json):
        rname = json['rname']
        rcapacity = json['rcapacity']
        rtype = json['rtype']
        dao = RoomsDAO()
        rid = dao.insertRoom(rname,rcapacity,rtype)
        result = self.build_attr_dict(rid,rname,rcapacity,rtype)
        return jsonify(result), 201

    def updateRoom(self, json):
        rname = json['rname']
        rcapacity = json['rcapacity']
        rtype = json['rtype']
        rid = json['rid']
        dao = RoomsDAO()
        updated_code = dao.updateRoom(rid,rname,rcapacity,rtype)
        result = self.build_attr_dict(rid,rname,rcapacity,rtype)
        return jsonify(result), 200

    def deleteRoom(self, rid):
        dao = RoomsDAO()
        result = dao.deleteRoom(rid)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def findAvailableRoom(self,json):
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        dao = RoomsDAO
        result = dao.findAvailableRoom(date,start_time,end_time)
        return jsonify(result), 200
