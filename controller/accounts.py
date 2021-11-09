from config.dbconfig import pg_config
import psycopg2

class AccountsDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host='%s'" %(pg_config['dbname'], pg_config['user'],
                                                                  pg_config['password'], pg_config['dbport'], pg_config['dbhost'])
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

    def insertAccount(self, username, password ,full_name, role):
        cursor = self.conn.cursor()
        query = "INSERT INTO account (username, password ,full_name, role) VALUES (%s,%s,%s,%s) RETURNING account_id;"
        cursor.execute(query, (username, password ,full_name, role,))
        account_id = cursor.fetchone()[0]
        self.conn.commit()
        return account_id

    def updateAccount(self, account_id, username, password, full_name, role):
        cursor = self.conn.cursor()
        query= "UPDATE account SET username=%s, password=%s, full_name=%s, role=%s WHERE account_id=%s;"
        cursor.execute(query, (username, password, full_name, role,account_id,))
        self.conn.commit()
        return True

    def deleteAccount(self, account_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM account WHERE account_id=%s;"
        cursor.execute(query,(account_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the account was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0