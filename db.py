import pymysql
from tkinter.messagebox import *


class Database:
    # connect to the database
    def __init__(self):
        try:
            self.db = pymysql.connect(host="localhost", user="root", password="root",   # edit here
                                      db="covidtracker", charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)

            self.cursor = self.db.cursor()
        except pymysql.err.OperationalError as e:
            print("Wrong user or password for the database. Please try again.")
            print('Error: %d: %s' % (e.args[0], e.args[1]))

    def commit(self):
        self.db.commit()

    def close_db(self):
        self.db.close()

    # data validation method by retrieving all the county names for building a drop-down menu for users
    def data_validation(self, query):
        try:
            cur = self.cursor
            cur.execute(query)
            rows = cur.fetchall()

            list_counties = []
            for row in rows:
                keys = list(row.keys())
                for key in keys:
                    list_counties.append(row.get(key).lower())
            cur.close()

            return list_counties

        except pymysql.Error as e:
            print('Error: %d: %s' % (e.args[0], e.args[1]))
            showerror("Error", "Error occurs. Please try again.")
