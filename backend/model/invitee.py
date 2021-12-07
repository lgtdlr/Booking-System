from backend.config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class InviteeDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'],
                                                                              pg_config['password'],
                                                                              pg_config['dbport'], pg_config['dbhost'])
        self.conn = psycopg2.connect(connection_url)

    def getAllInvitees(self):
        cursor = self.conn.cursor()
        query = "SELECT account_id, event_id FROM is_invited;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllInviteesByEvent(self, event_id):
        cursor = self.conn.cursor()
        query = """SELECT account_id, username, full_name, event_id 
        from account NATURAL INNER JOIN is_invited WHERE event_id = %s;"""
        cursor.execute(query, (event_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getInviteeByUniqueId(self, account_id, event_id):
        cursor = self.conn.cursor()
        query = "SELECT account_id, event_id from is_invited WHERE account_id = %s AND event_id = %s;"
        cursor.execute(query, (account_id, event_id,))
        result = cursor.fetchone()
        return result

    def insertInvitee(self, account_id, event_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO is_invited (account_id, event_Id) VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING " \
                "account_id, event_id;"
        try:
            cursor.execute(query, (account_id, event_id,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return None
        else:
            self.conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows

    def insertMultipleInvitees(self, account_ids, event_id):
        values = []
        for account in account_ids:
            values.append([account, event_id])
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO is_invited (account_id, event_id) VALUES %s ON CONFLICT DO NOTHING;"
            psycopg2.extras.execute_values(
                cursor, query, values, template=None, page_size=100
            )
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return None
        else:
            self.conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows

    def updateInvitee(self, account_id, event_id, new_account_id, new_event_id):
        cursor = self.conn.cursor()
        query = "UPDATE is_invited SET account_id = %s, event_id = %s WHERE account_id= %s AND event_id = %s;"
        try:
            cursor.execute(query, (new_account_id, new_event_id, account_id, event_id,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows != 0

    def deleteInvitee(self, account_id, event_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM is_invited WHERE account_id=ANY(%s) AND event_id=%s;"
        try:
            cursor.execute(query, (account_id, event_id))
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows != 0
