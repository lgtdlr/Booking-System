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

    # def findAvailableRoom(self,startTime,endTime,date):
    #     cursor = self.conn.cursor()
    #     query = """SELECT name FROM room
    #                WHERE room.room_id NOT IN (
    #                SELECT room.room_id FROM room
    #                INNER JOIN is_room_unavailable iru on room.room_id = iru.room_id
    #                INNER JOIN timeslot on iru.timeslot_id = timeslot.timeslot_id
    #                WHERE date = %s and start_time = %s and end_time = %s
    #                UNION SELECT room.room_id FROM room
    #                INNER JOIN event e on room.room_id = e.room_id
    #                INNER JOIN occupies o on e.event_id = o.event_id
    #                INNER JOIN timeslot t on t.timeslot_id = o.timeslot_id
    #                WHERE date = %s and start_time = %s and end_time = %s;
    #             """
    #     cursor.execute(query, (startTime,endTime,date,startTime,endTime,date))
    #     result = cursor.fetchall()
    #     return result

    # def whoAppointedRoom(self,rname,date,startTime,endTime):
    #     cursor = self.conn.cursor()
    #     query = """SELECT full_name FROM account
    #                JOIN event e ON account.account_id = e.creator_id
    #                INNER JOIN  room r ON r.room_id = e.room_id
    #                INNER JOIN occupies o ON e.event_id = o.event_id
    #                INNER JOIN  timeslot t ON t.timeslot_id = o.timeslot_id
    #                WHERE name = %s AND date = %s AND start_time = %s AND end_time = %s;
    #             """
    #     cursor.execute(query,(rname,date,startTime,endTime))
    #     result = cursor.fetchone()
    #     return result

    # def getAllDaySchedule(self,rname,date):
    #     cursor.conn.cursor()
    #     query = """SELECT start_time,end_time from timeslot
    #                INNER JOIN is_room_unavailable iru on timeslot.timeslot_id = iru.timeslot_id
    #                 inner join room r on r.room_id = iru.room_id
    #                 WHERE r.name = %s AND 
    #             """
