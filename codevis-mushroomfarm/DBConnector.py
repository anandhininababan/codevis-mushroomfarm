import mysql.connector as sqlcon



class DBConnector:
    DATABASE_NAME = 'mushroom_farm'

    def __init__(self, db = DATABASE_NAME):
        self.db = sqlcon.connect(
            host = 'localhost',
            user = 'root',
            passwd= '',
            database= db
        )
        self.cursor = self.db.cursor()

    def execute(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()