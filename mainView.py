from view import View
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from search import Search
from updateList import UpdateList
from listView import ListView
from modify import Modify
from hospitalView import Hospital
import sys


class MainView(View):
    def __init__(self, username):
        super().__init__(username)
        self.view.title("COVID-19 Information by Counties in MA")

        width = 700
        height = 600
        self.view.geometry(
            "%dx%d+%d+%d" % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2))

        Label(self.view, text='Search Counties', bg='white', fg='Navy', font='Helvetica 18 bold').pack(side=TOP,
                                                                                                       fill='x')
        Label(self.view, text="Please select a specific county you want to know: ").place(relx=0.1, rely=0.1,
                                                                                          relwidth=0.5,
                                                                                          height=25)

        # create the drop down menu
        self.drop_down = ttk.Combobox(self.view)
        self.drop_down.place(relx=0.6, rely=0.1, relwidth=0.35, height=25)
        self.drop_down["values"] = self.db.data_validation("SELECT county_name FROM county")
        self.drop_down.current(0)
        self.drop_down.bind("<<ComboboxSelected>>", self.drop_down_callback)

        # create the checkbox for showing all info
        check_button = ttk.Checkbutton(self.view, text="show all counties",
                                       command=lambda: self.check_button_callback(check_button, True))
        check_button.place(relx=0.1, rely=0.25)

        # set the tree location
        self.tree.place(relx=0.01, rely=0.3, relwidth=0.95)

        Label(self.view, text='* Right click on a particular record if you want to SAVE it to your list',
              fg='blue').place(relx=0.05, rely=0.7, width=400, height=25)

        # create right-click menu for tree
        self.menu.add_command(label='add this to your list', command=self.add_callback)

        # Button for jumping to the user list
        Button(self.view, text="my county list", command=self.jump_to_list).place(relx=0.1, rely=0.8, width=100)

        # Button for jumping to the Hospital info
        Button(self.view, text="hospital information", command=self.jump_to_hospital).place(
            relx=0.7, rely=0.8, width=150)

        self.view.protocol("WM_DELETE_WINDOW", lambda: self.logout(self.view))

        self.view.mainloop()

    def jump_to_list(self):
        m = Modify(user_name=self.username, tree=ListView(username=self.username).tree)
        m.modify("track_user_list", 5)

    def jump_to_hospital(self):
        Hospital(self.username)

    def drop_down_callback(self, event):
        search = Search(tree=self.tree)
        search.search_county(county_name=self.drop_down.get())

    def add_callback(self):
        self.get_tree_selection()
        update = UpdateList(user_name=self.username, county_name=self.get_tree_selection()[0])
        update.add(self.view)

    def logout(self, root):
        if askokcancel("Question", "Are you sure you want to quit?"):
            root.destroy()
            self.db.close_db()
            sys.exit()
