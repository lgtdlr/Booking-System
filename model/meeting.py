from config.dbconfig import pg_config
from flask import jsonify
import psycopg2


class MeetingDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" % (pg_config['dbname'], pg_config['user'],
                                                                              pg_config['password'],
                                                                              pg_config['dbport'], pg_config['dbhost'])
        print("connection url: ", connection_url)
        self.conn = psycopg2.connect(connection_url)
    
    
#CRUD OPERATIONS

    def getAllMeetings(self):
        cursor = self.conn.cursor()
        query = "select * from event;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMeetingById(self, event_id):
        cursor = self.conn.cursor()
        query = "select * from room where event_id = %s;"
        cursor.execute(query, (event_id,))
        result = cursor.fetchone()
        return result

    def createMeeting(self,title,description,date):
        cursor = self.conn.cursor()
        query = "insert into event (title,description,date) values (%s,%s,%s) returning event_id;"
        cursor.execute(query, (title,description,date))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

    def updateMeeting(self,event_id,title, description,date):
        cursor = self.conn.cursor()
        query = "update event set title = %s, description = %s, date = %s where event_id=%s;"
        cursor.execute(query, (title,description,date,event_id))
        self.conn.commit()
        return True

    def deleteEvent(self,event_id):
        cursor = self.conn.cursor()
        query = "delete from event where event_id=%s;"
        cursor.execute(query, (event_id))
        affected_rows = cursor.rowcount
        self.conn.commit()
        return affected_rows != 0

    # CRUD OPERATIONS FINISH

   
        

