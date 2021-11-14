from flask import jsonify

from model.account import AccountDAO


class BaseAccount:

    def build_map_dict(self, row):
        result = {'account_id': row[0], 'username': row[1], 'full_name': row[2], 'role': row[3]}
        return result

    def build_attr_dict(self, account_id, username, full_name, role):
        result = {'account_id': account_id, 'username': username, 'full_name': full_name, 'role': role}
        return result

    def getAllAccounts(self):
        dao = AccountDAO()
        account_list = dao.getAllAccounts()
        result_list = []
        for row in account_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getAccountById(self, account_id):
        dao = AccountDAO()
        account_tuple = dao.getAccountById(account_id)
        if not account_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(account_tuple)
            return jsonify(result), 200

    def insertAccount(self, json):
        username = json['username']
        password = json['password']
        full_name = json['full_name']
        role = json['role']
        dao = AccountDAO()
        account_id = dao.insertAccount(username, password, full_name, role)
        result = self.build_attr_dict(account_id, username, full_name, role)
        return jsonify(result), 201

    def updateAccount(self, account_id, json):
        username = json['username']
        password = json['password']
        full_name = json['full_name']
        role = json['role']
        dao = AccountDAO()
        is_updated = dao.updateAccount(account_id, username, password, full_name, role)
        result = self.build_attr_dict(account_id, username, full_name, role)
        return jsonify(result), 200

    def deleteAccount(self, account_id):
        dao = AccountDAO()
        result = dao.deleteAccount(account_id)
        if result:
            return jsonify("DELETED"), 200
        else:
            return jsonify("NOT FOUND"), 404

    def getAccountRole(self, json):
        account_id = json['account_id']
        dao = AccountDAO()
        account_tuple = dao.getAccountById(account_id)
        if not account_tuple:
            return jsonify("Not Found"), 404
        else:
            result = self.build_map_dict(account_tuple)
            return result['role']

    def findAvailableTime(self, json):
        account_ids = json['account_ids']
        dates = json['dates']
        dao = AccountDAO()
        result = dao.findAvailableTime(account_ids, dates)
        return jsonify(result), 200

    def setAccountUnavailable(self, json):
        account_id = json['account_id']
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        dao = AccountDAO()
        result = dao.setUnavailable(account_id, date, start_time, end_time)
        return jsonify(result), 200

    def setAccountAvailable(self, json):
        account_id = json['account_id']
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        dao = AccountDAO()
        result = dao.setAvailable(account_id, date, start_time, end_time)
        return jsonify(result), 200