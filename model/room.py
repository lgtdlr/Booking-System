from config.dbconfig import pg_config
import psycopg2

class RoomDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" %(pg_config['dbname'], pg_config['user'],
                          pg_config['password'], pg_config['dbport'], pg_config['dbhost'])
        print("connection url: ", connection_url)
        self.conn = psycopg2.connect(connection_url)
        

    #CRUD OPERATIONS

    def getAllRooms(self):
        cursor = self.conn.cursor()
        query =  "select * from room;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result
    
    def getRoomById(self,rid):
        cursor = self.conn.cursor()
        query = "select * from room where rid = %s;"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        return result

    def insertRoom(self, rname, rcapacity,rtype):
        cursor = self.conn.cursor()
        query = "insert into room (rname, rcapacity, rtype) values (%s,%s,%s) returning rid;"
        rid = cursor.fetchone()[0]
        self.conn.commit()
        return rid

    def updateRoom(self, rid, rname, rcapacity,rtype):
        cursor = self.conn.cursor()
        query = "update parts set rname=%s, rcapcity=%s, rtype=%s;"
        cursor.execute(query,(rname,rcapacity,rtype,rid))
        self.conn.commit()
        return True

    def deleteRoom(self,rid):
        cursor = self.conn.cursor()
        query = "delete from room where rid=%s;"
        cursor.execute(query,(rid,))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    # CRUD OPERATIONS FINISH

    #def findAvailableRoom(self,startTime,endTime):
       # cursor = self.conn.cursor()
       # query = ""
       # cursor.execute(query,(startTime,endTime))
       # result = cursor.fetchall()
    

    
