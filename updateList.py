from db import Database
import pymysql
from tkinter.messagebox import *


class UpdateList:
    def __init__(self, user_name, county_name):
        self.user_name = user_name
        self.county_name = county_name
        self.db = Database()

    def add(self, root):
        try:
            cur = self.db.cursor
            cur.callproc("add_user_list", (self.user_name, self.county_name))
            self.db.commit()
            cur.close()
            showinfo(title="Success", message="Added successfully!", parent=root)
        except pymysql.Error:
            showwarning(title="Warning", message="This record already exists.", parent=root)

    def remove(self, root):
        try:
            cur = self.db.cursor
            cur.callproc("remove_user_list", (self.user_name, self.county_name))
            self.db.commit()
            cur.close()
            showinfo(title="Success", message="Removed successfully!", parent=root)
        except pymysql.Error:
            showerror(title="Error", message="Error occurs. Please try again.", parent=root)