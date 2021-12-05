from flask import jsonify

from model.invitee import InviteeDAO


class BaseInvitee:

    def build_map_dict(self, row):
        result = {'account_id': row[0], 'event_id': row[1]}
        return result

    def build_attr_dict(self, account_id, event_id):
        result = {'account_id': account_id, 'event_id': event_id}
        return result

    def getAllInvitees(self):
        dao = InviteeDAO()
        invitee_list = dao.getAllInvitees()
        result_list = []
        for row in invitee_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getAllInviteesByEvent(self, event_id):
        dao = InviteeDAO()
        invitee_list = dao.getAllInviteesByEvent(event_id)
        result_list = []
        for row in invitee_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getInviteeByUniqueId(self, account_id, event_id):
        dao = InviteeDAO()
        invitee_tuple = dao.getInviteeByUniqueId(account_id, event_id)
        if not invitee_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(invitee_tuple)
            return jsonify(result), 200

    def insertInviteeWithJson(self, json):
        account_id = json['account_id']
        event_id = json['event_id']
        dao = InviteeDAO()
        if not isinstance(account_id, int):
            account_id = tuple(account_id)
            if len(account_id) > 1:
                result = dao.insertMultipleInvitees(account_id, event_id)
                return jsonify("Inserted row(s): " + str(result))

        result = dao.insertInvitee(account_id, event_id)

        return jsonify("Inserted row(s): " + str(result))

    def insertInvitee(self, event_id, json):
        account_id = json['account_id']
        dao = InviteeDAO()
        if not isinstance(account_id, int):
            account_id = tuple(account_id)
            if len(account_id) > 1:
                result = dao.insertMultipleInvitees(account_id, event_id)
                return jsonify("Inserted row(s): " + str(result))

        result = dao.insertInvitee(account_id, event_id)

        return jsonify("Inserted row(s): " + str(result))

    def updateInvitee(self, account_id, event_id, json):
        new_account_id = json['account_id']
        new_event_id = json['event_id']
        dao = InviteeDAO()
        is_updated = dao.updateInvitee(account_id, event_id, new_account_id, new_event_id)
        result = self.build_attr_dict(new_account_id, new_event_id)
        return jsonify(is_updated)

    def deleteInvitee(self, account_id, event_id):
        dao = InviteeDAO()
        result = dao.deleteInvitee(account_id, event_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404
