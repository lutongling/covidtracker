from db import Database
import pymysql
from tkinter.messagebox import *


class UpdateDonate:
    def __init__(self, user_name, hosp_name, donation_val, donation_type, description):
        self.user_name = user_name
        self.hosp_name = hosp_name
        self.donation_val = donation_val
        self.donation_type = donation_type
        self.description = description
        self.db = Database()

    def add(self, root):
        try:
            cur = self.db.cursor
            cur.callproc("add_donation",
                         (self.user_name, self.hosp_name, self.donation_val, self.donation_type, self.description))
            self.db.commit()
            cur.close()
            showinfo(title="Success",
                     message="Thank you for your Donation!\n"
                             "You can now check it in your donation record.", parent=root)
        except pymysql.Error as e:
            print('Error: %d: %s' % (e.args[0], e.args[1]))
            showerror(title="Error",
                      message="You've already donated to this hospital. Please choose another.\n"
                              "If you want to update it, please check the history. Thanks.", parent=root)

    def remove(self, root):
        try:
            cur = self.db.cursor
            cur.callproc("remove_donation", (self.user_name, self.hosp_name))
            self.db.commit()
            cur.close()
            showinfo(title="Success", message="Cancelled successfully!", parent=root)
        except pymysql.Error:
            showerror(title="Error", message="Error occurs. Please try again.", parent=root)

    def update(self, root):
        try:
            cur = self.db.cursor
            cur.callproc("if_donated", (self.user_name, self.hosp_name))
            is_donated = cur.fetchone()

            if is_donated:
                # cur = self.db.cursor
                cur.callproc("update_donation",
                             (self.user_name, self.hosp_name, self.donation_val, self.donation_type, self.description))
                self.db.commit()
                cur.close()
                showinfo(title="Success",
                         message="Update successfully!", parent=root)
            else:
                showerror(title="Error",
                          message="You haven't donated for this hospital.", parent=root)

        except pymysql.Error as e:
            print('Error: %d: %s' % (e.args[0], e.args[1]))
            showerror(title="Error",
                      message="Error occurs. Please tried again.", parent=root)
