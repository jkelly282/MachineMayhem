import sqlite3

class Database_manager:

    def __init__(self, db_name):
      self.conn = sqlite3.connect(db_name)
      self.c = self.conn.cursor()


    def create_table(self, name:str, columns: tuple):
        self.c.execute(('''CREATE TABLE if not exists Scores 
             (Name text , Score integer )'''))

    def insert_into_table(self, scores ):
        self.c.execute('INSERT INTO Scores VALUES (? , ?)', scores, )
        self.commit()

    def retrieve_high_scores(self):
        self.c.execute('SELECT * from Scores ORDER BY Score DESC LIMIT 5;')
        return self.c.fetchall()


    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

