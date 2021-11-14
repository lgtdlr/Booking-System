from flask import jsonify
from model.event import EventDAO


class BaseEvent:

    def build_map_dict(self, row):
        result = {'event_id': row[0], 'title': row[1], 'description': row[2], 'date': row[3], 'creator_id': row[4], 'room_id': row[5]}
        return result

    def build_attr_dict(self, event_id, title, description, date, room_id):
        result = {'event_id': event_id, 'title': title, 'description': description, 'date': date, 'room_id': room_id}
        return result


    def build_map_dict_timeslot(self, row):
        result = {'timeslot_id': row[0],
                  'start_time': row[1],
                  'end_time': row[2],
                  'busiest_30_min': row[3]}
        return result

    def getAllEvents(self):
        dao = EventDAO()
        room_list = dao.getAllEvents()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getEventById(self, event_id):
        dao = EventDAO()
        event_tuple = dao.getEventById(event_id)
        if not event_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(event_tuple)
            return jsonify(result), 200

    def addNewEvent(self, json):
        title = json['title']
        description = json['description']
        date = json['date']
        creator_id = json['creator_id']
        room_id = json['room_id']
        dao = EventDAO()
        event_id = dao.createEvent(title, description, date, creator_id, room_id)
        result = self.build_attr_dict(event_id, title, description, date, room_id)
        return jsonify(result), 201

    def updateEvent(self, event_id, json):
        title = json['title']
        description = json['description']
        date = json['date']
        room_id = json['room_id']
        dao = EventDAO()
        is_updated = dao.updateEvent(event_id, title, description, date, room_id)
        result = self.build_attr_dict(event_id, title, description, date, room_id)
        return jsonify(result), 200

    def deleteEvent(self, event_id):
        dao = EventDAO()
        result = dao.deleteEvent(event_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404


    def getBusiestTimesSlots(self):
        dao = EventDAO()
        times_list = dao.getMostBusiestTimes()
        result_list = []
        for row in times_list:
            obj = self.build_map_dict_timeslot(row)
            result_list.append(obj)
        return jsonify(result_list), 200

