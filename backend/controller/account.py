from flask import jsonify

from backend.model.account import AccountDAO


class BaseAccount:

    def build_map_dict(self, row):
        result = {'account_id': row[0], 'username': row[1], 'password': row[1], 'full_name': row[3], 'role': row[4]}
        return result

    def build_map_dict_booked_users(self, row):
        result = {'account_id': row[0],
                  'username': row[1],
                  'password': row[2],
                  'full_name': row[3],
                  'role': row[4],
                  'number_of_bookings': row[5]}
        return result

    def build_map_dict_user_events(self, row):
        result = {'title': row[0],
                  'start': row[1],
                  'end': row[2]}
        return result

    def build_attr_dict(self, account_id, username, full_name, role):
        result = {'account_id': account_id, 'username': username, 'full_name': full_name, 'role': role}
        return result

    def build_attr_dict_schedule(self, row):
        result = {'timeslot_id': row[0], 'start_time': row[1], 'end_time': row[2], 'available': row[3]}
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

    def getAccountByUsername(self, username):
        dao = AccountDAO()
        account_tuple = dao.getAccountByUsername(username)
        if not account_tuple:
            return None
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
        result_list = []
        for row in result:
            obj = self.build_attr_dict_schedule(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def setAccountAvailability(self, json):
        account_id = json['account_id']
        date = json['date']
        start_time = json['start_time']
        end_time = json['end_time']
        is_available = json['is_available']
        dao = AccountDAO()
        if is_available:
            result = dao.setAccountAvailable(account_id, date, start_time, end_time)
        else:
            result = dao.setAccountUnavailable(account_id, date, start_time, end_time)
        return jsonify(result), 200

    def getUserSchedule(self, username, json):
        date = json['date']
        dao = AccountDAO()
        result = dao.getUserSchedule(username, date)
        result_list = []
        for row in result:
            obj = self.build_attr_dict_schedule(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getMostBookedUser(self):

        dao = AccountDAO()
        user_list = dao.getMostBookedUser()
        result_list = []
        for row in user_list:
            obj = self.build_map_dict_booked_users(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getMost_Booking_With_User(self, account_id):

        dao = AccountDAO()
        user_list = dao.getMostBooking_with_selected_User(account_id)
        result_list = []
        for row in user_list:
            obj = self.build_map_dict_booked_users(row)
            result_list.append(obj)
        return jsonify(result_list), 200

    def getUserEvents(self, username):
        dao = AccountDAO()
        event_list = dao.getUserEvents(username)
        unavailable_times_list = dao.getUserUnavailableTimes(username)
        result_list = []
        for row in event_list:
            obj = self.build_map_dict_user_events(row)
            result_list.append(obj)
        for row in unavailable_times_list:
            obj = self.build_map_dict_user_events(row)
            result_list.append(obj)
        return jsonify(result_list), 200

