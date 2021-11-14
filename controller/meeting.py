from flask import jsonify
from model.meeting import MeetingDAO

class BaseEvent:

    def build_map_dict(self, row):
        result = {'event_id': row[0], 'title': row[1], 'description': row[2], 'date': row[3]}
        return result

    def build_attr_dict(self, event_id,title,description,date):
        result = {'event_id': event_id, 'title': title, 'description': description, 'date': date}
        return result

    def getAllMeetings(self):
        dao = MeetingDAO()
        room_list = dao.getAllMeetings()
        result_list = []
        for row in room_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list)

    def getMeetingById(self, event_id):
        dao = MeetingDAO()
        event_tuple = dao.getMeetingById(event_id)
        if not event_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(event_tuple)
            return jsonify(result), 200

    def addNewMeeting(self, json):
        title = json['title']
        description = json['description']
        date = json['date']
        dao = MeetingDAO()
        event_id = dao.insertRoom(title,description,date)
        result = self.build_attr_dict(event_id,title,description,date)
        return jsonify(result), 201

    def updateMeeting(self, json):
        title = json['title']
        description = json['description']
        date = json['date']
        event_id = ['event_id']
        dao = MeetingDAO()
        is_updated = dao.updateMeeting(event_id,title,description,date)
        result = self.build_attr_dict(event_id,title,description,date)
        return jsonify(result), 200

    def deleteMeeting(self, event_id):
        dao = MeetingDAO()
        result = dao.deleteRoom(event_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
