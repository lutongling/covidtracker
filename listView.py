from tkinter import *
from updateList import UpdateList
from modify import Modify
from view import View


class ListView(View):
    def __init__(self, username):
        super().__init__(username)
        self.view.title("List")

        width = 700
        height = 300
        self.view.geometry(
            "%dx%d+%d+%d" % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2))

        Label(self.view, text='My County List', bg='white', fg='Brown', font='Helvetica 18 bold').pack(side=TOP,
                                                                                                       fill='x')

        # set the tree place for user list
        self.tree.place(relx=0.02, rely=0.3, relwidth=0.9, relheight=0.5)

        Label(self.view, text='* Right click on a particular record if you want to DELETE it from your list',
              fg='red').place(relx=0.02, rely=0.86, relwidth=0.6, height=25)

        # create right-click menu for tree
        self.menu.add_command(label='remove this from your list', command=self.remove_callback)

    def remove_callback(self):
        update = UpdateList(self.username, self.get_tree_selection()[0])
        update.remove(self.view)
        m = Modify(self.username, self.tree)
        m.modify("track_user_list", 5)

        self.view.wm_attributes('-topmost', 1)
