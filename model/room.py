from config.dbconfig import pg_config
import psycopg2


class RoomDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'],
                                                                              pg_config['password'],
                                                                              pg_config['dbport'], pg_config['dbhost'])
        print("connection url: ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    # CRUD OPERATIONS

    def getAllRooms(self):
        cursor = self.conn.cursor()
        query = "select room_id, name, capacity, type from room;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = "select room_id, name, capacity, type from room where room_id = %s;"
        cursor.execute(query, (room_id,))
        result = cursor.fetchone()
        return result

    def insertRoom(self, name, capacity, type):
        cursor = self.conn.cursor()
        query = "insert into room (name, capacity, type) values (%s,%s,%s) returning room_id;"
        cursor.execute(query, (name, capacity, type))
        rid = cursor.fetchone()[0]
        self.conn.commit()
        return rid

    def updateRoom(self, room_id, name, capacity, type):
        cursor = self.conn.cursor()
        query = "update room set name = %s, capacity = %s, type = %s where room_id=%s;"
        cursor.execute(query, (name, capacity, type, room_id))
        self.conn.commit()
        return True

    def deleteRoom(self, room_id):
        cursor = self.conn.cursor()
        query = "delete from room where room_id=%s;"
        cursor.execute(query, (room_id,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    # CRUD OPERATIONS FINISH

    def setRoomAvailable(self, room_id, date, start_time, end_time):
        cursor = self.conn.cursor()
        query = "DELETE FROM is_room_unavailable WHERE room_id IN " \
                "(SELECT iru.room_id FROM is_room_unavailable iru " \
                "INNER JOIN timeslot t on t.timeslot_id = iru.timeslot_id " \
                "WHERE room_id = %s AND date = %s " \
                "AND (t.start_time >= %s::time AND t.end_time <= %s::time) " \
                "AND (t.end_time-t.start_time >= '00:00:00'::time));"
        try:
            cursor.execute(query, (room_id, date, start_time, end_time,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def setRoomUnavailable(self, room_id, date, start_time, end_time):
        cursor = self.conn.cursor()
        query = "INSERT INTO is_room_unavailable SELECT %s as room_id, t.timeslot_id, %s as date " \
                "FROM timeslot t WHERE (t.start_time >= %s::time AND t.end_time <= %s::time) " \
                "AND (t.end_time-t.start_time >= '00:00:00'::time) ON CONFLICT DO NOTHING;"
        try:
            cursor.execute(query, (room_id, date, start_time, end_time,))
        except psycopg2.IntegrityError:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def findAvailableRoom(self, start_time, end_time, date):
        cursor = self.conn.cursor()
        query = """SELECT room_id, name, capacity, type FROM room
                   WHERE room.room_id NOT IN (
                   SELECT room.room_id FROM room
                   INNER JOIN is_room_unavailable iru on room.room_id = iru.room_id
                   INNER JOIN timeslot on iru.timeslot_id = timeslot.timeslot_id
                   WHERE date = %s and start_time = %s and end_time = %s
                   UNION SELECT room.room_id FROM room
                   INNER JOIN event e on room.room_id = e.room_id
                   INNER JOIN occupies o on e.event_id = o.event_id
                   INNER JOIN timeslot t on t.timeslot_id = o.timeslot_id
                   WHERE date = %s AND (t.start_time >= %s::time AND t.end_time <= %s::time) 
                   AND (t.end_time-t.start_time >= '00:00:00'::time));
                """
        cursor.execute(query, (date, start_time, end_time, date, start_time, end_time,))
        result = cursor.fetchall()
        return result

    def whoAppointedRoom(self, name, date, start_time, end_time):
        cursor = self.conn.cursor()
        query = """SELECT full_name FROM account
                   JOIN event e ON account.account_id = e.creator_id
                   INNER JOIN  room r ON r.room_id = e.room_id
                   INNER JOIN occupies o ON e.event_id = o.event_id
                   INNER JOIN  timeslot t ON t.timeslot_id = o.timeslot_id
                   WHERE name = %s AND date = %s AND (t.start_time >= %s::time AND t.end_time <= %s::time) 
                   AND (t.end_time-t.start_time >= '00:00:00'::time);
                """
        cursor.execute(query, (name, date, start_time, end_time,))
        result = cursor.fetchone()
        return result

    def getAllDaySchedule(self, name, date):
        cursor = self.conn.cursor()
        query = """SELECT %s AS room_name, timeslot.start_time::text,timeslot.end_time::text,TRUE as available FROM timeslot 
                    WHERE timeslot.timeslot_id NOT IN (
                    SELECT timeslot.timeslot_id FROM room
                    INNER JOIN is_room_unavailable iru on room.room_id = iru.room_id
                    INNER JOIN timeslot on iru.timeslot_id = timeslot.timeslot_id
                    WHERE room.name = %s AND iru.date = %s
                    UNION
                    SELECT t.timeslot_id FROM room
                    INNER JOIN event e on room.room_id = e.room_id
                    INNER JOIN occupies o on e.event_id = o.event_id
                    INNER JOIN timeslot t on t.timeslot_id = o.timeslot_id
                    WHERE room.name = %s AND e.date = %s
                    )
                    UNION
                    SELECT room.name,timeslot.start_time::text,timeslot.end_time::text,FALSE as available FROM room
                    INNER JOIN is_room_unavailable iru on room.room_id = iru.room_id
                    INNER JOIN timeslot on iru.timeslot_id = timeslot.timeslot_id
                    WHERE room.name = %s AND iru.date = %s
                    UNION
                    SELECT room.name,t.start_time::text,t.end_time::text,FALSE as available FROM room
                    INNER JOIN event e on room.room_id = e.room_id
                    INNER JOIN occupies o on e.event_id = o.event_id
                    INNER JOIN timeslot t on t.timeslot_id = o.timeslot_id
                    WHERE room.name = %s AND e.date = %s ORDER BY start_time;
                """
        cursor.execute(query, (name, name, date, name, date, name, date, name, date,))
        result = cursor.fetchall()
        return result

    def getMostBookedRooms(self):
        cursor = self.conn.cursor()
        query = """ select room_id, name, count(event_id) as events_in_room
                    from event natural join room
                    group by room_id, name
                    order by events_in_room desc limit 10;"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result