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
        query = "select * from room;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRoomById(self, room_id):
        cursor = self.conn.cursor()
        query = "select * from room where room_id = %s;"
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

    # def findAvailableRoom(self,startTime,endTime):
    # cursor = self.conn.cursor()
    # query = ""
    # cursor.execute(query,(startTime,endTime))
    # result = cursor.fetchall()

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
