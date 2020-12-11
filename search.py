from tkinter.messagebox import *
from modifyTree import ModifyTree


class Search(ModifyTree):
    def __init__(self, tree):
        super().__init__(tree)

    def show_all(self, procedure_name):
        cur = self.db.cursor
        cur.callproc(procedure_name)
        rows = cur.fetchall()

        result = self.get_list_rows(rows, 5)
        self.insert_multiple(result)
        cur.close()

    def search_county(self, county_name):
        cur = self.db.cursor
        cur.callproc("track_county_name", (county_name,))
        rows = cur.fetchall()

        result = self.get_list_values(rows)
        self.insert_single(result)
        cur.close()

    def search_hospital(self, hosp_name, parent):
        cur = self.db.cursor
        cur.callproc("track_hospital_name", (hosp_name,))
        if cur.rowcount == 0:
            showwarning("Empty", "The hospital name doesn't exist.", parent=parent)

        rows = cur.fetchall()

        result = self.get_list_values(rows)
        self.insert_single(result)
        cur.close()

    def search_by_county(self, county_name):
        cur = self.db.cursor
        cur.callproc("track_hospital_by_county", (county_name,))
        rows = cur.fetchall()

        result = self.get_list_rows(rows, 5)
        self.insert_multiple(result)
        cur.close()
