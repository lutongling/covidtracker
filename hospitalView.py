from tkinter import *
from tkinter import ttk
from search import Search
from donate import Donate
from donateHistory import History
from modify import Modify
from tkinter.messagebox import *
from view import View


class Hospital(View):
    def __init__(self, username):
        super().__init__(username)
        self.invisible()
        self.view = Toplevel()
        self.view.title("Hospital Information")

        width = 860
        height = 500
        self.view.geometry(
            "%dx%d+%d+%d" % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2))

        Label(self.view, text='Hospital Information', bg='white', fg='Purple', font='Helvetica 18 bold').pack(side=TOP,
                                                                                                              fill='x')
        # textual input searching
        Label(self.view, text="Search by a Hospital name in MA: ").place(relx=0.1, y=70)
        hospital_name = StringVar()
        Entry(self.view, width=30, textvariable=hospital_name).place(relx=0.33, y=70, relwidth=0.35)
        Button(self.view, text="OK", width=10,
               command=lambda: self.text_search_callback(hospital_name, self.view)).place(relx=0.7,
                                                                                          y=65)

        # label for dropdown menu
        Label(self.view, text="Search by a County in MA: ").place(relx=0.1, y=120)

        # create the drop down menu
        self.drop_down = ttk.Combobox(self.view)
        self.drop_down.place(relx=0.33, y=120, relwidth=0.35, height=25)
        self.drop_down["values"] = self.db.data_validation("SELECT county_name FROM county")
        self.drop_down.current(0)
        self.drop_down.bind("<<ComboboxSelected>>", self.drop_down_callback)

        # create the checkbox for showing all info
        check_button = ttk.Checkbutton(self.view, text="show all hospitals",
                                       command=lambda: self.check_button_callback(check_button, False))
        check_button.place(relx=0.8, rely=0.3)

        # create the table/tree for showing hospital data
        self.tree = ttk.Treeview(self.view, show="headings",
                                 column=(
                                     'hospital_name', 'county_name', 'covid_hospitalizations',
                                     'covid_ICU_hospitalizations',
                                     'shortage_status'))

        scroll = Scrollbar(self.view, orient='vertical', command=self.tree.yview)
        scroll.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)

        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.column('hospital_name', width=150, anchor="center")
        self.tree.column('county_name', width=50, anchor="center")
        self.tree.column('covid_hospitalizations', width=60, anchor="center")
        self.tree.column('covid_ICU_hospitalizations', width=80, anchor="center")
        self.tree.column('shortage_status', width=30, anchor="center")

        self.tree.heading('hospital_name', text='Name')
        self.tree.heading('county_name', text='Location')
        self.tree.heading('covid_hospitalizations', text='COVID hospitalizations')
        self.tree.heading('covid_ICU_hospitalizations', text='COVID ICU hospitalizations')
        self.tree.heading('shortage_status', text='shortage or not')

        self.tree.place(relx=0.02, rely=0.36, relwidth=0.93, relheight=0.5)

        Button(self.view, text="Create New Donation", width=25, command=self.donate_form).place(relx=0.39, rely=0.9)
        Button(self.view, text="Donation History", width=20, command=self.donate_history).place(relx=0.01, rely=0.9)

    def text_search_callback(self, hospital_name, parent):
        hospital_name = hospital_name.get()
        if hospital_name == "":
            showwarning("Warning", "The Hospital Name should not be empty.", parent=self.view)
        else:
            search = Search(tree=self.tree)
            search.search_hospital(hosp_name=hospital_name, parent=parent)

    def drop_down_callback(self, event):
        s = Search(tree=self.tree)
        s.search_by_county(county_name=self.drop_down.get())

    def donate_form(self):
        Donate(self.username)

    def donate_history(self):
        m = Modify(self.username, History(self.username).tree)
        m.modify("track_donation", 4)
