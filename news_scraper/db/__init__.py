import psycopg2


class Database():
    def __init__(self, user, password, port, database, host):
        self.conn = psycopg2.connect(user=user, password=password, port=port, database=database, host=host)
        self.cur = self.conn.cursor()

    def query(self, query, params={}):
        try:
            self.cur.execute(query, params)
        except:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()
        return self.cur.fetchall()

    def execute(self, query, params={}):
        try:
            self.cur.execute(query, params)
        except:
            self.conn.rollback()
            raise
        else:
            self.conn.commit()
        return

    def close(self):
        self.cur.close()
        self.conn.close()
