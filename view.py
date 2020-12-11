from db import Database
from tkinter import *
from tkinter import ttk
from search import Search


class View:
    def __init__(self, username):
        self.username = username
        self.db = Database()
        self.view = Tk()

        self.screenwidth = self.view.winfo_screenwidth()
        self.screenheight = self.view.winfo_screenheight()

        # create the table/tree for showing counties using Tkinter Treeview
        self.tree = ttk.Treeview(self.view, show="headings",
                                 column=(
                                     'county_name', 'positive_number', 'positive_rate', 'death_number',
                                     'level_of_risk'))

        # create the scrollbar for tree
        scroll = Scrollbar(self.view, orient='vertical', command=self.tree.yview)
        scroll.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)

        # set column fields, size and position
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.column('county_name', width=80, anchor="center")
        self.tree.column('positive_number', width=80, anchor="center")
        self.tree.column('positive_rate', width=80, anchor="center")
        self.tree.column('death_number', width=80, anchor="center")
        self.tree.column('level_of_risk', width=80, anchor="center")

        # set heading titles for column fields
        self.tree.heading('county_name', text='Name')
        self.tree.heading('positive_number', text='Positive Cases')
        self.tree.heading('positive_rate', text='Positive Rate')
        self.tree.heading('death_number', text='Death Cases')
        self.tree.heading('level_of_risk', text='Risk Level')

        # create right-click menu for tree
        self.menu = Menu(self.view, tearoff=0)

        # bind the popup with the right-click behavior
        self.tree.bind("<Button-3>", self.popup)

    def invisible(self):
        self.view.withdraw()

    def visible(self):
        self.view.deiconify()

    def popup(self, event):
        # select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.menu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def get_tree_selection(self):
        item_text = []
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
        return item_text

    def check_button_callback(self, check_button, is_subview):
        if check_button.instate(['selected']):
            search = Search(tree=self.tree)
            if is_subview:
                search.show_all("track_all_counties")
            else:
                search.show_all("track_all_hospitals")
        else:
            for item in self.tree.get_children():
                self.tree.delete(item)
