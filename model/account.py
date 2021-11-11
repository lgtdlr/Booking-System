from werkzeug.security import generate_password_hash

from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class AccountDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'],
                                                                              pg_config['password'],
                                                                              pg_config['dbport'], pg_config['dbhost'])
        self.conn = psycopg2.connect(connection_url)

    def getAllAccounts(self):
        cursor = self.conn.cursor()
        query = "SELECT account_id, username, full_name, role FROM account;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAccountById(self, account_id):
        cursor = self.conn.cursor()
        query = "SELECT account_id, username, full_name, role from account WHERE account_id = %s;"
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        return result

    def insertAccount(self, username, password, full_name, role):
        hashed_password = generate_password_hash(password, method='sha256')
        cursor = self.conn.cursor()
        query = "INSERT INTO account (username, password ,full_name, role) VALUES (%s,%s,%s,%s) RETURNING account_id;"
        try:
            cursor.execute(query, (username, hashed_password, full_name, role,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return None
        else:
            account_id = cursor.fetchone()[0]
            self.conn.commit()
            return account_id

    def updateAccount(self, account_id, username, password, full_name, role):
        hashed_password = generate_password_hash(password, method='sha256')
        cursor = self.conn.cursor()
        query = "UPDATE account SET username = %s, password = %s, full_name = %s, role = %s WHERE account_id=%s;"
        try:
            cursor.execute(query, (username, hashed_password, full_name, role, account_id,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def deleteAccount(self, account_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM account WHERE account_id=%s;"
        try:
            cursor.execute(query, (account_id,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows != 0

    def findAvailableTime(self, account_ids, dates):
        cursor = self.conn.cursor()
        accounts = tuple(account_ids)
        if len(dates) < 2:
            date1 = dates[0]
            date2 = dates[0]
        else:
            date1 = dates[0]
            date2 = dates[1]
        query = "SELECT t.timeslot_id FROM timeslot t WHERE timeslot_id NOT IN " \
                "(SELECT t.timeslot_id FROM account a INNER JOIN is_invited ii on a.account_id = ii.account_id " \
                "INNER JOIN event e on e.event_id = ii.event_id INNER JOIN occupies o on e.event_id = o.event_id " \
                "INNER JOIN timeslot t on t.timeslot_id = o.timeslot_id WHERE a.account_id IN %s AND e.date " \
                "BETWEEN %s::date AND %s::date UNION SELECT t.timeslot_id FROM account a " \
                "INNER JOIN is_account_unavailable iau on a.account_id = iau.account_id " \
                "INNER JOIN timeslot t on t.timeslot_id = iau.timeslot_id " \
                "WHERE a.account_id IN %s AND iau.date BETWEEN %s::date AND %s::date);"
        cursor.execute(query, (accounts, date1, date2, accounts, date1, date2,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def setUnavailable(self, account_id, date, start_time, end_time):
        cursor = self.conn.cursor()
        query = "INSERT INTO is_account_unavailable SELECT %s as account_id, t.timeslot_id, %s as date " \
                "FROM timeslot t WHERE (t.start_time >= %s::time AND t.end_time <= %s::time) " \
                "AND (t.end_time-t.start_time >= '00:00:00'::time) ON CONFLICT DO NOTHING;"
        try:
            cursor.execute(query, (account_id, date, start_time, end_time,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def setAvailable(self, account_id, date, start_time, end_time):
        cursor = self.conn.cursor()
        query = "DELETE FROM is_account_unavailable WHERE account_id IN " \
                "(SELECT iau.account_id FROM is_account_unavailable iau " \
                "INNER JOIN timeslot t on t.timeslot_id = iau.timeslot_id " \
                "WHERE account_id = %s AND date = %s " \
                "AND (t.start_time >= %s::time AND t.end_time <= %s::time) " \
                "AND (t.end_time-t.start_time >= '00:00:00'::time));"
        try:
            cursor.execute(query, (account_id, date, start_time, end_time,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows != 0

