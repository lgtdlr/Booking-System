from werkzeug.security import generate_password_hash

from backend.config.dbconfig import pg_config
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
        query = "SELECT account_id, username, password, full_name, role FROM account;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAccountById(self, account_id):
        cursor = self.conn.cursor()
        query = "SELECT account_id, username, password, full_name, role from account WHERE account_id = %s;"
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        return result

    def getAccountByUsername(self, username):
        cursor = self.conn.cursor()
        query = "SELECT account_id, username, password, full_name, role from account WHERE username = %s;"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        return result

    def insertAccount(self, username, password, full_name, role):
        hashed_password = generate_password_hash(password, method='sha256')
        cursor = self.conn.cursor()
        query = "INSERT INTO account (username, password ,full_name, role) VALUES (%s,%s,%s,%s) " \
                "ON CONFLICT DO NOTHING RETURNING account_id;"
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
        cursor.execute(query, (account_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0
        # try:
        #     cursor.execute(query, (account_id,))
        # except psycopg2.IntegrityError:
        #     self.conn.rollback()
        # else:
        #     affected_rows = cursor.rowcount
        #     self.conn.commit()
        #     return affected_rows != 0

    def findAvailableTime(self, account_ids, dates):
        cursor = self.conn.cursor()
        accounts = tuple(account_ids)
        if len(dates) < 2:
            date1 = dates[0]
            date2 = dates[0]
        else:
            date1 = dates[0]
            date2 = dates[1]
        query = '''SELECT t.timeslot_id, t.start_time::text, t.end_time::text FROM timeslot t WHERE timeslot_id NOT IN
                (SELECT t.timeslot_id FROM account a INNER JOIN is_invited ii on a.account_id = ii.account_id
                INNER JOIN event e on e.event_id = ii.event_id INNER JOIN occupies o on e.event_id = o.event_id
                INNER JOIN timeslot t on t.timeslot_id = o.timeslot_id WHERE a.account_id IN %s AND e.date
                BETWEEN %s::date AND %s::date UNION SELECT t.timeslot_id FROM account a 
                INNER JOIN is_account_unavailable iau on a.account_id = iau.account_id 
                INNER JOIN timeslot t on t.timeslot_id = iau.timeslot_id 
                WHERE a.account_id IN %s AND iau.date BETWEEN %s::date AND %s::date);'''
        cursor.execute(query, (accounts, date1, date2, accounts, date1, date2,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def setAccountUnavailable(self, account_id, date, start_time, end_time):
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

    def setAccountAvailable(self, account_id, date, start_time, end_time):
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

    def getUserSchedule(self, uname, date):
        cursor = self.conn.cursor()
        query = '''
                    SELECT timeslot.timeslot_id,timeslot.start_time::text,timeslot.end_time::text,TRUE as available 
                    FROM timeslot WHERE timeslot.timeslot_id NOT IN (
                    SELECT timeslot.timeslot_id FROM account
                    INNER JOIN is_account_unavailable iau on account.account_id = iau.account_id
                    INNER JOIN timeslot on iau.timeslot_id = timeslot.timeslot_id
                    WHERE account.username = %s AND iau.date = %s
                    UNION
                    SELECT t2.timeslot_id FROM account
                    INNER JOIN is_invited i on account.account_id = i.account_id
                    INNER JOIN event e on i.account_id = e.event_id
                    INNER JOIN occupies o on e.event_id = o.event_id
                    INNER JOIN timeslot t2 on o.timeslot_id = t2.timeslot_id
                    WHERE account.username = %s AND e.date = %s
                    )
                    UNION
                    SELECT timeslot.timeslot_id,timeslot.start_time::text,timeslot.end_time::text,FALSE as available 
                    FROM account INNER JOIN is_account_unavailable iau on account.account_id = iau.account_id
                    INNER JOIN timeslot on iau.timeslot_id = timeslot.timeslot_id
                    WHERE account.username = %s AND iau.date = %s
                    UNION
                    SELECT t2.timeslot_id,t2.start_time::text,t2.end_time::text,FALSE as available FROM account
                    INNER JOIN is_invited i on account.account_id = i.account_id
                    INNER JOIN event e on i.account_id = e.event_id
                    INNER JOIN occupies o on e.event_id = o.event_id
                    INNER JOIN timeslot t2 on o.timeslot_id = t2.timeslot_id
                    WHERE account.username = %s AND e.date = %s ORDER BY start_time;    
                 '''
        cursor.execute(query, (uname, date, uname, date, uname, date, uname, date))
        result = cursor.fetchall()
        return result

    def getMostBookedUser(self):
        cursor = self.conn.cursor()
        query = """select account_id,username,password,full_name,role, count(event_id) as number_of_bookings
                    from is_invited natural join account
                    group by account_id,username,password,full_name,role
                    order by number_of_bookings desc limit 10; """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def getMostBooking_with_selected_User(self, account_id):
        cursor = self.conn.cursor()
        query = """with bookings_with_selected_user as
                    --query to determine account_ids that participate
                    -- in same events as the selected user
                        (select S2.account_id, S2.event_id
                        from is_invited as S1, is_invited as S2
                        where S1.account_id = %s -- id that represents the selected user
                          and S2.event_id = S1.event_id
                          and S2.account_id <> S1.account_id-- don't want selected user part of the solution
                          order by S2.account_id, S2.event_id),--ordering just for testing purposes
                    
                    --counting events per account
                    number_of_events_per_acount_with_selected_user as
                        (select account_id, count(event_id) as number_of_bookings_with_user
                         from bookings_with_selected_user
                         group by account_id)
                    
                    
                    select  account_id,username,password, full_name, 
                    role, number_of_bookings_with_user as number_of_bookings
                    from number_of_events_per_acount_with_selected_user natural join account
                    where number_of_bookings_with_user = (
                    --there could be more than one user that
                    --have the maximum amount of bookings
                    --with the selected user
                        select max(number_of_bookings_with_user)
                        from number_of_events_per_acount_with_selected_user
                        ) """
        cursor.execute(query, (account_id,))
        result = cursor.fetchall()
        return result
