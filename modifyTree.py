from db import Database


class ModifyTree:
    def __init__(self, tree):
        self.db = Database()
        self.tree = tree

        # delete previously selected record(s)
        old = self.tree.get_children()
        for row in old:
            self.tree.delete(row)

    '''
    Get methods are encapsulation the loops for retrieving the results from the database.
    Insert methods are for inserting the corresponding values to the trees/tables in GUI.
    '''

    def get_list_values(self, fetch_rows):
        list_values = []
        for row in fetch_rows:
            keys = list(row.keys())
            for key in keys:
                list_values.append(row.get(key))
        return list_values

    def get_list_rows(self, fetch_rows, split_n):
        list_rows = []
        list_values = self.get_list_values(fetch_rows)

        for i in range(0, len(list_values), split_n):
            new = list_values[i:i + split_n]
            list_rows.append(new)
        return list_rows

    def insert_single(self, list_values):
        self.tree.insert("", "end", values=list_values)

    def insert_multiple(self, list_rows):
        for row in list_rows:
            self.tree.insert("", "end", values=row)
