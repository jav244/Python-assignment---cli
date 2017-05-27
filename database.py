import sqlite3


class Database:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name, .1)
            self.c = self.conn.cursor()
            self.create_table()
            self.c.close()
        except Exception as e:
            print(e)
        else:
            print("connection established")

    def create_table(self):
        self.c.execute("DROP TABLE IF EXISTS Employee")

        # Create table
        self.c.execute('''CREATE TABLE Employee
                     (EMPID char(4) PRIMARY KEY,
                      Gender char(1),
                      Age INTEGER,
                      Sales INTEGER,
                      BMI VARCHAR(15),
                      Salary INTEGER,
                      Birthday DATE)''')

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def insert(self, data):
        self.c = self.conn.cursor()
        sql = []

        for key, value in data.items():
            sql.append(value)
        empid = sql[0]
        gender = sql[1]
        age = int(sql[2])
        sales = int(sql[3])
        bmi = sql[4]
        salary = int(sql[5])
        birthday = sql[6]

        sql_string = "INSERT INTO Employee VALUES ('{empid}', '{gender}', {age}, {sales}, '{bmi}', {salary}, '{birthday}' )".format(
            **vars())
        self.c.execute(sql_string)

        self.c.execute("COMMIT")

        self.c.close()

    def query(self, input):
        self.c = self.conn.cursor()
        sql = "select %s from employee" % input
        self.c.execute(sql)
        result = self.c.fetchall()
        self.c.close()
        return result

    def count_query(self, row, id):
        self.c = self.conn.cursor()
        sql = ("select count(%s) from employee where upper(%s) = '%s'" % (row, row, str(id)))
        self.c.execute(sql)
        result = self.c.fetchall()
        self.c.close()
        return result
