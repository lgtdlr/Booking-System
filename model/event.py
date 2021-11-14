from config.dbconfig import pg_config
import psycopg2


class EventDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'],
                                                                              pg_config['password'],
                                                                              pg_config['dbport'], pg_config['dbhost'])
        print("connection url: ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    # CRUD OPERATIONS

    def getAllEvents(self):
        cursor = self.conn.cursor()
        query = "select event_id, title, description, date, creator_id, room_id from event;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getEventById(self, event_id):
        cursor = self.conn.cursor()
        query = "select event_id, title, description, date, creator_id, room_id from event where event_id = %s;"
        cursor.execute(query, (event_id,))
        result = cursor.fetchone()
        return result

    def createEvent(self, title, description, date, creator_id, room_id):
        cursor = self.conn.cursor()
        query = "insert into event (title,description,date,creator_id,room_id) values (%s,%s,%s,%s,%s) returning event_id;"
        cursor.execute(query, (title, description, date, creator_id, room_id,))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

    def updateEvent(self, event_id, title, description, date, room_id):
        cursor = self.conn.cursor()
        query = "update event set title = %s, description = %s, date = %s, room_id = %s where event_id=%s;"
        cursor.execute(query, (title, description, date, event_id, room_id,))
        self.conn.commit()
        return True

    def deleteEvent(self, event_id):
        cursor = self.conn.cursor()
        query = "delete from event where event_id=%s;"
        cursor.execute(query, (event_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    def getMostBusiestTimes(self):
        cursor = self.conn.cursor()
        query = """select timeslot_id,start_time::varchar,end_time::varchar, count(event_id) as busiest_30_min
                    from occupies natural join timeslot
                    group by timeslot_id ,start_time::varchar,end_time::varchar
                    order by busiest_30_min desc, timeslot_id desc limit 5;"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    # CRUD OPERATIONS FINISH
