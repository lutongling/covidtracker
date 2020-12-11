from tkinter import *
from tkinter import ttk
from view import View
from modify import Modify
from updateDonate import UpdateDonate
from donateCallback import DonateCallback


class History(View):
    def __init__(self, username):
        super().__init__(username)
        self.invisible()
        self.view = Toplevel()
        self.view.title("Donation History")

        width = 660
        height = 350
        self.view.geometry(
            "%dx%d+%d+%d" % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2))

        Label(self.view, text='Donation History', bg='white', fg='DarkSlateGray', font='Helvetica 18 bold').pack(
            side=TOP, fill='x')

        # create the table/tree for showing donation history
        self.tree = ttk.Treeview(self.view, show="headings",
                                 column=(
                                     'hospital_name', 'donation_value', 'donation_type', 'description'))

        scroll = Scrollbar(self.view, orient='vertical', command=self.tree.yview)
        scroll.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)

        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.column('hospital_name', width=150, anchor="center")
        self.tree.column('donation_value', width=50, anchor="center")
        self.tree.column('donation_type', width=100, anchor="center")
        self.tree.column('description', width=100, anchor="center")

        self.tree.heading('hospital_name', text='Hospital Name')
        self.tree.heading('donation_value', text='Value')
        self.tree.heading('donation_type', text='Type')
        self.tree.heading('description', text='Details')

        self.tree.place(relx=0.02, rely=0.2, relwidth=0.93, relheight=0.5)

        # create labels for inputs for update
        Label(self.view, text='* Right click on a particular record if you want to CANCEL it.',
              fg='blue').place(relx=0.01, rely=0.1, width=400, height=25)
        Label(self.view, text='Hospital Name').place(relx=0.1, rely=0.7, width=100)
        Label(self.view, text='Value').place(relx=0.37, rely=0.7, width=50)
        Label(self.view, text='Type').place(relx=0.56, rely=0.7, width=50)
        Label(self.view, text='Details').place(relx=0.78, rely=0.7, width=80)

        hosp_name = StringVar()
        donation_val = StringVar()
        Entry(self.view, width=30, textvariable=hosp_name).place(relx=0.03, rely=0.76)
        Entry(self.view, width=10, textvariable=donation_val).place(relx=0.36, rely=0.76)

        # create the drop down menu
        drop_down = ttk.Combobox(self.view)
        drop_down.place(relx=0.52, rely=0.76, relwidth=0.18, height=25)
        drop_down["values"] = ["cash", "daily supplies", "medical equipment"]
        drop_down.current(0)

        description = Text(self.view, height=3, width=20)
        description.place(relx=0.73, rely=0.76)

        # create right-click menu for tree
        self.menu = Menu(self.view, tearoff=0)
        self.menu.add_command(label='Cancel', command=self.remove_callback)

        # Button-3 is right click on windows
        self.tree.bind("<Button-3>", self.popup)

        Button(self.view, text="Update the donation", width=20,
               command=lambda: DonateCallback(username=self.username, hosp_name=hosp_name, donation_val=donation_val,
                                              donation_type=drop_down, description=description).donate_callback(
                   self.tree, True)).place(relx=0.36, rely=0.9)

    def remove_callback(self):
        item_text = self.get_tree_selection()
        update = UpdateDonate(self.username, item_text[0], item_text[1], item_text[2], item_text[3])
        update.remove(self.view)

        m = Modify(self.username, self.tree)
        m.modify("track_donation", 4)

        self.view.wm_attributes('-topmost', 1)
