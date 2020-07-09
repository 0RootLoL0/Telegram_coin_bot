import sqlite3

class userdb:
    def __init__(self, db):
        self.db = db
        cur = self.db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Account (ID INTEGER PRIMARY KEY, PHONE TEXT, PASS TEXT, API_ID TEXT, API_HASH TEXT, ACTIVITY TEXT, LITECOIN TEXT )""")
        self.db.commit()
        cur.close()
    def addUser(self, Phone, password, Api_id, Api_hash, Activity, Litecoin):
        cur = self.db.cursor()
        cur.execute(f"SELECT PHONE FROM Account WHERE PHONE = '{Phone}'")
        if cur.fetchone() is None:
            cur.execute(
                """INSERT INTO Account(PHONE, PASS, API_ID, API_HASH, ACTIVITY, LITECOIN) VALUES (?,?,?,?,?,?);""",
                (Phone, password, Api_id, Api_hash, Activity, Litecoin))
            self.db.commit()
        cur.close()
    def getUser(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Account")
        qwe = cur.fetchall()
        cur.close()
        return qwe
    def delUser(self, id):
        cur = self.db.cursor()
        cur.execute("DELETE FROM Account WHERE ID = "+str(int(id)))
        self.db.commit()
        cur.close()

