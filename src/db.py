import sqlite3
import uuid


class ConnServDb:
    def __init__(self):
        self.name = 'conserv.db'
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.__createTables()

    def __createTables(self):
        tables = self.getTablesList()
        if len(tables) == 0:
            self.cursor.execute('CREATE TABLE file_id_table (FileID text, Hash text);')
            self.conn.commit()

    def getTablesList(self):
        return list(self.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"'))

    def getFileID(self, hash):
        fileID = self.cursor.execute('SELECT FileID FROM file_id_table WHERE Hash = "%s"' % hash).fetchone()
        if fileID == None:
            fileID = uuid.uuid4().hex
            self.cursor.execute('INSERT INTO file_id_table VALUES ("%s", "%s")' % (fileID, hash))
            self.conn.commit()
        else:
            fileID = fileID[0]
        return fileID

if __name__ == '__main__':
    db = ConnServDb()
    for i in range(100000):
        db.getFileID('aaafa')
