from __future__ import print_function
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io
import pickle
import os.path
import os
import shutil
import tkinter
import tkinter.messagebox as tm
from tkinter import filedialog, ttk
import zipfile
import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk
import mysql.connector

folders = {
    'videos': ['.mp4', '.mkv'],
    'audios': ['.wav', '.mp3', ],
    'images': ['.jpg', '.jpeg', '.png'],
    'documents': ['.doc', '.xlsx', '.xls', '.pdf', '.zip', '.rar', '.rtf'],
    'software': ['.exe']}

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kishore",
)

db_cursor = db_connection.cursor(buffered=True)


class LoginApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("600x450+351+174") 
        self.configure(bg="#000000")
        self.lblHeading = tk.Label(self, text="Welcome to EROHSIK", font=("Helvetica", 16), bg="black", fg="white")
        self.lbluname = tk.Label(self, text="Enter UserName:", font=("Helvetica", 10), bg="black", fg="white")
        self.lblpsswd = tk.Label(self, text="Enter Password:", font=("Helvetica", 10), bg="black", fg="white")
        self.txtuname = tk.Entry(self, width=60)
        self.txtpasswd = tk.Entry(self, width=60, show="*")
        self.btn_login = tk.Button(self, text="Login", font=("Helvetica", 11), bg="black", fg="white",
                                   command=self.login)
        self.btn_clear = tk.Button(self, text="Clear", font=("Helvetica", 11), bg="black", fg="white",
                                   command=self.clear_form)
        self.btn_register = tk.Button(self, text="Not Member ? Register", font=("Helvetica", 11), bg="black",
                                      fg="yellow", command=self.open_registration_window)
        self.btn_exit = tk.Button(self, text="Exit", font=("Helvetica", 20), bg="black", fg="red", command=self.exit)
        self.lblHeading.place(relx=0.35, rely=0.089, height=50, width=250)
        self.lbluname.place(relx=0.235, rely=0.289, height=21, width=106)
        self.lblpsswd.place(relx=0.242, rely=0.378, height=21, width=102)
        self.txtuname.place(relx=0.417, rely=0.289, height=20, relwidth=0.273)
        self.txtpasswd.place(relx=0.417, rely=0.378, height=20, relwidth=0.273)
        self.btn_login.place(relx=0.45, rely=0.489, height=24, width=52)
        self.btn_clear.place(relx=0.54, rely=0.489, height=24, width=72)
        self.btn_register.place(relx=0.695, rely=0.489, height=24, width=175)
        self.btn_exit.place(relx=0.75, rely=0.911, height=24, width=61)

    def open_registration_window(self):
        self.withdraw()
        window = RegisterWindow(self)
        window.grab_set()

    def open_login_success_window(self):
        self.withdraw()
        window = Login_Success_Window(self)
        window.grab_set()

    def show(self):
        """"""
        self.update()
        self.deiconify()

    def login(self):
        if db_connection.is_connected() == False:
            db_connection.connect()

        db_cursor.execute("CREATE DATABASE IF NOT EXISTS User")
        db_cursor.execute("use User")
        db_cursor.execute(
            "create table if not exists USER(uid VARCHAR(30) NOT NULL  PRIMARY KEY,password VARCHAR(30),"
            "fname VARCHAR(30),lname VARCHAR(30))")
        db_connection.commit()

        try:
            global username
            username = str(self.txtuname.get())  # Retrieving entered username
            passwd = str(self.txtpasswd.get())  # Retrieving entered password
            if username == "":
                mb.showinfo('Information', "Please Enter Username")
                self.txtuname.focus_set()
                return
            if passwd == "":
                mb.showinfo('Information', "Please Enter Password")
                self.txtpasswd.focus_set()
                return

            print(username)
            print(passwd)
            query = "SELECT * FROM User WHERE uid = '" + username + "' AND password = '" + passwd + "'"
            print(query)

            db_cursor.execute(query)
            rowcount = db_cursor.rowcount
            print(rowcount)
            if db_cursor.rowcount == 1:
                mb.showinfo('Information', "Login Successfully")
                self.open_login_success_window()
            else:
                mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")
        except:

            db_connection.disconnect()

    def clear_form(self):
        self.txtuname.delete(0, tk.END)
        self.txtpasswd.delete(0, tk.END)
        self.txtuname.focus_set()

    def exit(self):
        MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                icon='warning')
        if MsgBox == 'yes':
            self.destroy()


class Login_Success_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("800x400")
        self.title("You Have Successfully Login -> " + str(username))
        self.configure(background="#000000")
        self.lbl_Login_success = tk.Label(self, text="Hello " + str(username) + " Welcome to App",
                                          font=("Helvetica", 15), bg="black", fg="white")

        self.lbl_Login_success.place(relx=0.150, rely=0.111, height=50, width=300)

        db_cursor.execute("SELECT * FROM user limit 0,10")
        i = 1
        for user in db_cursor:
            for j in range(len(user)):
                e = Entry(self, bg="black", fg="white")
                e.grid(row=i, column=j)
                e.insert(END, user[j])
            i = i + 1

        self.btn_next = tk.Button(self, text='START', font=("Helvetica", 11), bg='black', fg='white'
                                  , command=self.m_screen_call)
        self.btn_next.place(relx=0.700, rely=0.300)
        self.btn_register = tk.Button(self, text="Logout", font=("Helvetica", 11), bg="black", fg="white",
                                      command=self.logout)
        self.btn_register.place(relx=0.467, rely=0.311, height=21, width=50)

    def m_screen_call(self):
        main()

    def start(self):
        self.destroy()
        self.main_window()

    def logout(self):
        mb.showinfo('Information', "You Have Successfully Logout " + str(username))
        self.destroy()
        self.original_frame.show()


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+485+162")
        self.title("Register")
        self.configure(background="#000000")

        self.lblRegister = tk.Label(self, text="Register", font=("Helvetica", 16), bg="black", fg="white")
        self.lblFName = tk.Label(self, text="Enter FirstName:", font=("Helvetica", 10), bg="black", fg="white")
        self.lblLName = tk.Label(self, text="Enter LastName:", font=("Helvetica", 10), bg="black", fg="white")
        self.lblLName = tk.Label(self, text="Enter LastName:", font=("Helvetica", 10), bg="black", fg="white")
        self.lblUId = tk.Label(self, text="Enter UserId:", font=("Helvetica", 10), bg="black", fg="white")
        self.lblPwd = tk.Label(self, text="Enter Password:", font=("Helvetica", 10), bg="black", fg="white")

        self.txtFName = tk.Entry(self)
        self.txtLName = tk.Entry(self)
        self.txtUId = tk.Entry(self)
        self.txtPwd = tk.Entry(self)

        self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="black", fg="white",
                                      command=self.register)
        self.btn_cancel = tk.Button(self, text="Back To Login", font=("Helvetica", 11), bg="black", fg="white",
                                    command=self.onClose)

        self.lblRegister.place(relx=0.467, rely=0.111, height=21, width=100)
        self.lblFName.place(relx=0.318, rely=0.2, height=21, width=100)
        self.lblLName.place(relx=0.319, rely=0.267, height=21, width=100)
        self.lblUId.place(relx=0.355, rely=0.333, height=21, width=78)
        self.lblPwd.place(relx=0.319, rely=0.4, height=21, width=100)
        self.txtFName.place(relx=0.490, rely=0.2, height=20, relwidth=0.223)
        self.txtLName.place(relx=0.490, rely=0.267, height=20, relwidth=0.223)
        self.txtUId.place(relx=0.490, rely=0.333, height=20, relwidth=0.223)
        self.txtPwd.place(relx=0.490, rely=0.4, height=20, relwidth=0.223)
        self.btn_register.place(relx=0.500, rely=0.660, height=24, width=63)
        self.btn_cancel.place(relx=0.605, rely=0.660, height=24, width=150)

    def register(self):

        if db_connection.is_connected() == False:
            db_connection.connect()

        db_cursor.execute("CREATE DATABASE IF NOT EXISTS User")  #
        db_cursor.execute("use User")

        db_cursor.execute(
            "Create table if not exists USER(uid VARCHAR(30) NOT NULL  PRIMARY KEY,password VARCHAR(30),fname VARCHAR(30),lname VARCHAR(30))")

        db_connection.commit()

        fname = self.txtFName.get()
        lname = self.txtLName.get()
        uid = self.txtUId.get()
        pwd = self.txtPwd.get()
        if fname == "":
            mb.showinfo('Information', "Please Enter Firstname")
            self.txtFName.focus_set()
            return
        if lname == "":
            mb.showinfo('Information', "Please Enter Lastname")
            self.txtLName.focus_set()
            return
        if uid == "":
            mb.showinfo('Information', "Please Enter User Id")
            self.txtUId.focus_set()
            return
        if pwd == "":
            mb.showinfo('Information', "Please Enter Password")
            self.txtPwd.focus_set()
            return

        db_cursor.execute("use User")
        query = "INSERT INTO User(uid,password,fname,lname) VALUES ('%s','%s','%s','%s')" % (uid, pwd, fname, lname,)

        try:
            db_cursor.execute(query)
            mb.showinfo('Information', "Data inserted Successfully")
            db_connection.commit()
        except:
            mb.showinfo('Information', "Data insertion failed!!!")
            db_connection.rollback()
            db_connection.close()

    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()


class DriveAPI:
    global SCOPES

    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        print('hello')

        self.creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:

            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)

        results = self.service.files().list(
            pageSize=100, fields="files(id, name)").execute()
        global items
        items = results.get('files', [])

        print("Here's a list of files: \n")
        print(*items, sep="\n", end="\n\n")
        print(items)

    def FileDownload(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False

        # Download the data in chunks
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        # Write the received data to the file
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)

        print("File Downloaded")
        # Return True if file Downloaded successfully
        return True
        # except:

        # Return False if something went wrong
        # print("Something went wrong.")
        # return False

    def FileUpload(self, filepath):

        # Extract the file name out of the file path
        name = filepath.split('/')[-1]

        # Find the MimeType of the file
        mimetype = MimeTypes().guess_type(name)[0]

        # create file metadata
        file_metadata = {'name': name}

        media = MediaFileUpload(filepath, mimetype=mimetype)
        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        print("File Uploaded.")


class main_screen():
    DriveAPI

    def __init__(self):
        self.widget = None

        def fo():
            gk = Tk()

            def out():
                # global directry
                folder_path = tkinter.filedialog.askdirectory()
                k = folder_path

                print(k)

                def out2():

                    def create_other():
                        other = kishore
                        print(other)
                        directry = k
                        for j in os.listdir(directry):
                            if os.path.isfile(os.path.join(directry, j)) == True:
                                if other not in os.listdir(directry):
                                    os.mkdir(os.path.join(directry, other))
                                shutil.move(os.path.join(directry, j), os.path.join(directry, other))

                    other1 = Label(gk, text='Mention the name of the folder')
                    other1.pack()
                    other1value = StringVar()
                    other1entry = Entry(gk, textvariable=other1value)
                    other1entry.pack()
                    kishore = other1value.get()
                    print(kishore)
                    Button(gk, text='NEXT', command=create_other).pack()

                def create_move(ext, file_name):
                    for folder_name in folders:
                        if '.' + ext in folders[folder_name]:
                            if folder_name not in os.listdir(directry):
                                os.mkdir(os.path.join(directry, folder_name))
                            shutil.move(os.path.join(directry, file_name), os.path.join(directry, folder_name))

                def new1():
                    value = tm.askquestion('PLEASE ANSWER !!!',
                                           '''THERE WERE SOME FILES WHICH THE SYSTEM COULD NOT ARRANGE
                                               DO YOU WANT TO ARRANGE THEM IN A NEW FOLDER?''')
                    if value == "yes":
                        out2()
                    else:
                        pass

                # if k == "":
                #   print('sorry')

                directry = k
                for i in os.listdir(directry):
                    if os.path.isfile(os.path.join(directry, i)) == True:
                        create_move(i.split(".")[-1], i)
                for i in os.listdir(directry):
                    if os.path.isfile(os.path.join(directry, i)) == True:
                        break
                new1()

            gk.configure(background='black')

            gk.geometry('700x700')

            gk.title('EROHISK: FILE ORGANIZER')
            Label(gk, text='EROHISK: FILE ORGANIZER', bg='RED', fg='BLACK', font=('chicanes', 20),
                  borderwidth=3, relief=RAISED).pack()
            Button(gk, text="SELECT THE FOLDER", bg='red', fg='white',
                   font=('Helvtica', 20, 'italic', 'bold'), borderwidth=10,
                   relief='raised', width=15, height=1, command=out).pack()
            gk.mainloop()

        def ug():
            k = Tk()
            k.configure(background='black')
            k.geometry('700x700')
            k.title('EROHISK: FILE ORGANIZER')
            Label(k, text='EROHISK: GOOGLE DRIVE UPLOAD DOWNLOAD', bg='RED', fg='BLACK', font=('chicanes', 20),
                  borderwidth=3,
                  relief=RAISED).pack()

            Button(k, text='upload', bg='red', fg='blue', font=('Helvtica', 20, 'italic', 'bold'),
                   borderwidth=10,
                   relief='raised', width=15, height=1, command=self.upload).pack()
            Button(k, text='download', bg='red', fg='blue', font=('Helvtica', 20, 'italic', 'bold'),
                   borderwidth=10,
                   relief='raised', width=15, height=1, command=self.d_load).pack()
            Button(k, text='exit', bg='red', fg='blue', font=('Helvtica', 20, 'italic', 'bold'), borderwidth=10,
                   relief='raised', width=15, height=1, command=self.exit1).pack()

            k.mainloop()

        def zf():

            def zf_final():
                directry1 = tkinter.filedialog.askdirectory()
                os.chdir(directry1)
                k = nameofzip.get()
                shutil.make_archive(f'{k}', 'zip', directry1)
                print('done')

            # for i in os.listdir(directry):

            f = Tk()
            f.configure(background='black')

            f.geometry('700x700')
            f.title('EROHISK: ZIP FILE MAKER')
            Label(f, text='give a name for the zip folder', bg='yellow', fg='black',font=('Helvtica', 20, 'italic', 'bold'), borderwidth=10).pack() 
            nameofzip = Entry(f, textvariable=StringVar())
            nameofzip.pack()
            butt = Button(f, text="SELECT THE FOLDER", bg='yellow', fg='black', font=('Helvtica', 20, 'italic', 'bold'),
                          borderwidth=10,
                          relief='raised', width=15, height=1, command=zf_final).pack(pady=40)
            # butt.pack()
            f.mainloop()

        g = Tk()
        g.configure(background='black')
        g.geometry("700x700")
        g.title('EROHSIK')
        f2 = Frame(g, borderwidth=20, bg="grey", relief=SUNKEN)
        f2.pack(side=TOP, padx=10)
        l1 = Label(f2, text='WELCOME TO EROHSIK', bg='black', fg='white', font=('chicanes', 25), borderwidth=10,
                   relief=SUNKEN)
        l1.pack()
        print('hwello')
        Button(g, text='FILE ORGANIZER', bg='yellow', fg='black', font=('Helvtica', 20, 'italic', 'bold'),
               borderwidth=10,
               relief='raised', width=15, height=1, command=fo).pack(pady=40)
        Button(g, text='GOOGLE DRIVE U/D LOAD', bg='yellow', fg='black', font=('Helvtica', 20, 'italic', 'bold'), borderwidth=10,
               relief='raised', width=25, height=1, command=ug).pack(pady=20)
        Button(g, text='ZIP THE FILES', bg='yellow', fg='black', font=('Helvtica', 20, 'italic', 'bold'),
               borderwidth=10,
               relief='raised', width=15, height=1, command=zf).pack(pady=40)
        g.mainloop()

    def to_take(self):
        obj = DriveAPI()

        i = int(input("Enter your choice: 1 - Download file, 2- Upload File, 3- Exit.\n"))

    def click(self, event):
        global text1
        text1 = event.widget.cget('text')
        text1_fi = 'id: ' + text1

        f_id_value.set(f_id_value.get() + text1)
        # self.f_id_entry.update()
        print(text1)

    def click2(self, event):
        global text2
        text2 = event.widget.cget('text')
        f_name_value.set(f_name_value.get() + text2)
        # self.f_name_entry.update()
        print(text2)

    def d_load(self):
        obj = DriveAPI()

        root = Tk()
        root.title('google drive download')
        root.geometry('390x500')
        root.configure(bg='black')
        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        mycanvas = Canvas(main_frame)
        mycanvas.pack(side=LEFT, fill=BOTH, expand=1)
        myscroll = ttk.Scrollbar(main_frame, orient=VERTICAL, command=mycanvas.yview)
        myscroll.pack(side=RIGHT, fill=Y)
        mycanvas.configure(yscrollcommand=myscroll.set)
        mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
        second_frame = Frame(mycanvas, bg='black')
        mycanvas.create_window((0, 0), window=second_frame, anchor='nw')

        # for thing in range(100):
        #  Button(second_frame, text=f'Button{thing} yo').grid(row=thing, column=0, pady=10, padx=10)
        # root.mainloop()
        # root = tk.Tk()
        # root.geometry('1000x1000')
        Label(root, text='ENTER THE FILE ID AND FILE FROM THE LIST SHOWN')
        k = items
        for i in range(0, len(items)):
            j = items[i]
            for k in j:
                print(k, "::::", j[k])
                # id = k
                if k == 'id':
                    id = j[k]
                    g = Button(second_frame, text=id, bg='red',width=50,height=2)
                    Label(second_frame,text='').pack()
                    g.pack()
                    g.bind("<Button-1>", self.click)
                else:
                    name = j[k]
                    f = Button(second_frame, text=name, bg='green',width=50,height=2)
                    f.pack()
                    f.bind("<Button-1>", self.click2)
                # g = Button(second_frame, text=id)
                # g.pack()
                # g.bind("<Button-1>", self.click)
                # f = Button(second_frame, text=name)
                # f.pack()
                # f.bind("<Button-1>", self.click2)
            # Label(root,text=j).pack()
        # id_and_name = Label(root, text=items)
        # id_and_name.pack()
        f_id = Label(root, text='ENTER THE FILE Id')
        f_id.pack()
        global f_id_value
        f_id_value = StringVar()

        # self.f_id_entry = Entry(root, textvariable=f_id_value)
        # self.f_id_entry.pack()
        f_name = Label(root, text='ENTER THE NAME OF THE FILE')
        f_name.pack()
        global f_name_value
        f_name_value = StringVar()

        # self.f_name_entry = Entry(root, textvariable=f_name_value)
        # self.f_name_entry.pack()
        button = Button(root, text='NEXT', command=self.d_load_gui)
        button.pack()
        # root.mainloop()
        # print(*items, sep="\n", end="\n\n")

    def d_load_gui(self):
        f_id_use = text1
        f_name_use = text2
        # f_id_use = self.f_id_entry.get()
        # f_name_use = self.f_name_entry.get()
        print(f_id_use)
        print(f_name_use)
        obj1 = DriveAPI()
        obj1.FileDownload(f_id_use, f_name_use)

    def path_get(self):
        obj = DriveAPI()
        folder_path = filedialog.askopenfilename()
        print(folder_path)
        # f_path = input("Enter full file path: ")
        obj.FileUpload(folder_path)

        exit()

    #   print(f_path)

    def upload(self):
        # obj = DriveAPI()
        root = Tk()
        root.geometry('500x500')
        root.configure(bg='black')
        Label(root, text='SELECT THE PATH OF THE FILE', bg='yellow', fg='black',
              font=('Helvtica', 20, 'italic', 'bold'), borderwidth=10).pack()
        # self.path_entry = Entry(root, textvariable=StringVar(), width=15)
        # self.path_entry.pack()
        Button(root, text='SELECT', bg='yellow', fg='black', font=('Helvtica', 20, 'italic', 'bold'), borderwidth=10,
               command=self.path_get,
               relief='raised', width=15, height=1).pack(pady=20)
        # f_path = input("Enter full file path: ")
        # obj.FileUpload(f_path)

    # root.mainloop()

    def exit1(self):
        exit()


def main():
    main_screen()


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
