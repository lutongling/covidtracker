from db import Database
from tkinter import *
from tkinter.messagebox import *
from mainView import MainView


class Login:
    def __init__(self):
        self.db = Database()

        self.login = Tk()
        self.login.resizable(0, 0)
        self.login.title("Covid Tracker")

        screenwidth = self.login.winfo_screenwidth()
        screenheight = self.login.winfo_screenheight()
        width = 500
        height = 300
        self.login.geometry("%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2))

        self.canvas = Canvas(self.login, height=300, width=500)
        self.file = PhotoImage(file="covid_tracker.png")
        self.image = self.canvas.create_image(0, 0, anchor=CENTER, image=self.file)
        self.canvas.pack(side="top")

        Label(self.login, text="username").place(relx=0.2, y=70)
        Label(self.login, text="password").place(relx=0.2, y=95)

        username = StringVar()
        password = StringVar()

        Entry(self.login, width=30, textvariable=username).place(relx=0.37, y=70)
        Entry(self.login, width=30, show="*", textvariable=password).place(relx=0.37, y=95)

        # using lambda to allow passing arguments in Tk Button's command
        Button(self.login, text="Login", width=10,
               command=lambda: self.login_check(username, password)).place(relx=0.3, y=200)
        Button(self.login, text="Register", width=10,
               command=lambda: self.register(username, password)).place(relx=0.5, y=200)

        mainloop()

    def login_check(self, username, password):
        username = username.get()
        password = password.get()
        cur = self.db.cursor
        if not (len(username) == 0 or len(password) == 0):
            query = "SELECT user_password FROM user_account WHERE user_name=%s"
            cur.execute(query, username)
            result = cur.fetchone()
            if result:
                if password == result['user_password']:
                    showinfo(title="Welcome", message="Logged in successfully!")
                    self.login.destroy()
                    MainView(username)
                    cur.close()
                else:
                    showerror(title="Error", message="Unmatched username and password!")
            else:
                showwarning(title="Warning", message="Username does not exist. Please register first.")
        else:
            showerror(title="Error", message="Username or password cannot be empty.")

    def register(self, username, password):
        username = username.get()
        password = password.get()
        cur = self.db.cursor
        if not (len(username) == 0 or len(password) == 0):
            if ' ' in username:
                showerror(title="Error", message="Username cannot contain space.")
            else:
                cur.callproc("initialize_user_account", (username, password))
                self.db.commit()
                showinfo(title="Success", message="Congratulations! Register Done.")
        else:
            showerror(title="Error", message="Username or password cannot be empty.")
