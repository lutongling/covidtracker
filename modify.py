import pymysql
from modifyTree import ModifyTree


class Modify(ModifyTree):
    def __init__(self, user_name, tree):
        super().__init__(tree)
        self.user_name = user_name

    def modify(self, procedure_name, split_n):
        try:
            cur = self.db.cursor
            cur.callproc(procedure_name, (self.user_name,))
            rows = cur.fetchall()

            result = self.get_list_rows(rows, split_n)
            self.insert_multiple(result)
            cur.close()
        except pymysql.err.OperationalError as e:
            print("Database error occurs. Please try again.")
            print('Error: %d: %s' % (e.args[0], e.args[1]))

