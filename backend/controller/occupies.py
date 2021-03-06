from flask import jsonify

from backend.model.occupies import OccupiedTimeslotDAO


class BaseOccupiedTimeslot:

    def build_map_dict(self, row):
        result = {'timeslot_id': row[0], 'event_id': row[1]}
        return result

    def build_map_dict_timeslots(self, row):
        result = {'timeslot_id': row[0], 'start_time': row[1], 'end_time': row[2]}
        return result

    def build_attr_dict(self, timeslot_id, event_id):
        result = {'timeslot_id': timeslot_id, 'event_id': event_id}
        return result

    def getAllTimeslots(self):
        dao = OccupiedTimeslotDAO()
        occupied_list = dao.getAllTimeslots()
        result_list = []
        for row in occupied_list:
            obj = self.build_map_dict_timeslots(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getAllOccupiedTimeslots(self):
        dao = OccupiedTimeslotDAO()
        occupied_list = dao.getAllOccupiedTimeslots()
        result_list = []
        for row in occupied_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getAllOccupiedTimeslotsByEvent(self, event_id):
        dao = OccupiedTimeslotDAO()
        occupied_list = dao.getAllOccupiedTimeslotsByEvent(event_id)
        result_list = []
        for row in occupied_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getOccupiedTimeslotByUniqueId(self, timeslot_id, event_id):
        dao = OccupiedTimeslotDAO()
        occupied_tuple = dao.getOccupiedTimeslotByUniqueId(timeslot_id, event_id)
        if not occupied_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(occupied_tuple)
            return jsonify(result), 200

    def insertOccupiedTimeslot(self, event_id, json):
        start_time_id = json['start_time_id']
        end_time_id = json['end_time_id']
        dao = OccupiedTimeslotDAO()
        result = dao.insertMultipleOccupiedTimeslots(start_time_id, end_time_id, event_id)
        return jsonify("Inserted row(s): " + str(result))

        return jsonify("Inserted row(s): " + str(result))

    def updateOccupiedTimeslot(self, timeslot_id, event_id, json):
        new_timeslot_id = json['timeslot_id']
        new_event_id = json['event_id']
        dao = OccupiedTimeslotDAO()
        is_updated = dao.updateOccupiedTimeslot(timeslot_id, event_id, new_timeslot_id, new_event_id)
        result = self.build_attr_dict(new_timeslot_id, new_event_id)
        return jsonify(is_updated)

    def deleteOccupiedTimeslot(self, timeslot_id, event_id):
        dao = OccupiedTimeslotDAO()
        result = dao.deleteOccupiedTimeslot(timeslot_id, event_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
