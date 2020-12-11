from tkinter.messagebox import *
from db import Database
from modify import Modify
from updateDonate import UpdateDonate
from view import View


class DonateCallback(View):
    def __init__(self, username, hosp_name, donation_val, donation_type, description):
        super().__init__(username)
        self.invisible()
        self.db = Database()

        self.hosp_name = hosp_name.get()
        self.donation_val = donation_val.get()
        self.donation_type = donation_type.get()
        self.description = description.get("1.0", "end-1c")

    def donate_callback(self, tree, is_hist):
        try:
            float(self.donation_val)
        except ValueError:
            showerror("Error", "Donation values should only contain a number.", parent=self.view)
            return

        if len(self.hosp_name) == 0:
            showerror("Error", "Hospital name cannot be empty.", parent=self.view)
        elif self.donation_val == 0:
            showerror("Error", "Donation values should not be 0.", parent=self.view)
        elif self.hosp_name.lower() not in self.db.data_validation("SELECT hospital_name FROM hospital"):
            showerror("Sorry", "Hospital name doesn't exist. Please try again.", parent=self.view)
        else:
            ud = UpdateDonate(self.username, self.hosp_name, self.donation_val, self.donation_type, self.description)
            if is_hist:
                ud.update(self.view)
            else:
                ud.add(self.view)
            m = Modify(self.username, tree)
            m.modify("track_donation", 4)
            self.view.wm_attributes('-topmost', 1)
            self.invisible()