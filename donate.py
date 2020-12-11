from tkinter import *
from tkinter import ttk
from view import View
from donateCallback import DonateCallback


class Donate(View):
    def __init__(self, username):
        super().__init__(username)
        self.invisible()
        self.view = Toplevel()
        self.view.title("Donate Form")

        width = 750
        height = 200
        self.view.geometry(
            "%dx%d+%d+%d" % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2))

        Label(self.view, text='Create a new Donation', bg='white', fg='DarkCyan', font='Helvetica 18 bold').pack(
            side=TOP, fill='x')

        Label(self.view, text="Hospital Name").place(relx=0.05, rely=0.2)
        Label(self.view, text="Donation Value").place(relx=0.35, rely=0.2)
        Label(self.view, text="Donation Type").place(relx=0.55, rely=0.2)
        Label(self.view, text="Description(optional)").place(relx=0.8, rely=0.2)

        # create entry boxes for user inputs
        hosp_name = StringVar()
        donation_val = StringVar()
        Entry(self.view, width=30, textvariable=hosp_name).place(relx=0.05, rely=0.3)
        Entry(self.view, width=10, textvariable=donation_val).place(relx=0.35, rely=0.3)

        # create the drop down menu
        drop_down = ttk.Combobox(self.view)
        drop_down.place(relx=0.55, rely=0.3, relwidth=0.15, height=25)
        drop_down["values"] = ["cash", "daily supplies", "medical equipment"]
        drop_down.current(0)

        description = Text(self.view, height=6, width=15)
        description.place(relx=0.8, rely=0.3)

        Button(self.view, text="Donate Now!", width=20,
               command=lambda: DonateCallback(username=self.username, hosp_name=hosp_name, donation_val=donation_val,
                                              donation_type=drop_down, description=description).donate_callback(
                   self.tree, False)).place(relx=0.36, rely=0.81)
