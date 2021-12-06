from backend.config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class OccupiedTimeslotDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'],
                                                                              pg_config['password'],
                                                                              pg_config['dbport'], pg_config['dbhost'])
        self.conn = psycopg2.connect(connection_url)

    def getAllTimeslots(self):
        cursor = self.conn.cursor()
        query = "SELECT timeslot_id, start_time::text, end_time::text FROM timeslot;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllOccupiedTimeslots(self):
        cursor = self.conn.cursor()
        query = "SELECT timeslot_id, event_id FROM occupies;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllOccupiedTimeslotsByEvent(self, event_id):
        cursor = self.conn.cursor()
        query = "SELECT timeslot_id, event_id from occupies WHERE event_id = %s;"
        cursor.execute(query, (event_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getOccupiedTimeslotByUniqueId(self, timeslot_id, event_id):
        cursor = self.conn.cursor()
        query = "SELECT timeslot_id, event_id from occupies WHERE timeslot_id = %s AND event_id = %s;"
        cursor.execute(query, (timeslot_id, event_id,))
        result = cursor.fetchone()
        return result

    def insertOccupiedTimeslot(self, timeslot_id, event_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO occupies (timeslot_id, event_Id) VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING " \
                "timeslot_id, event_id;"
        try:
            cursor.execute(query, (timeslot_id, event_id,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return None
        else:
            self.conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows

    def insertMultipleOccupiedTimeslots(self, timeslot_ids, event_id):
        values = []
        for timeslot_id in range(timeslot_ids[0],timeslot_ids[-1]):
            values.append([timeslot_id, event_id])
        # for account in timeslot_ids:
        #     values.append([account, event_id])
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO occupies (timeslot_id, event_id) VALUES %s ON CONFLICT DO NOTHING;"
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

    def updateOccupiedTimeslot(self, timeslot_id, event_id, new_timeslot_id, new_event_id):
        cursor = self.conn.cursor()
        query = "UPDATE occupies SET timeslot_id = %s, event_id = %s WHERE timeslot_id= %s AND event_id = %s;"
        try:
            cursor.execute(query, (new_timeslot_id, new_event_id, timeslot_id, event_id,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows != 0

    def deleteOccupiedTimeslot(self, timeslot_id, event_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM occupies WHERE timeslot_id = %s AND event_id = %s;"
        try:
            cursor.execute(query, (timeslot_id, event_id))
        except psycopg2.IntegrityError:
            self.conn.rollback()
        else:
            affected_rows = cursor.rowcount
            self.conn.commit()
            return affected_rows != 0

