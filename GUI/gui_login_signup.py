import customtkinter as ctk
import mariadb

from review_functions import *

app = ctk.CTk()
app.title("Critiqué Login")
app.geometry("1440x1024")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(0.90)

mydb = mariadb.connect(
    user="root",
    password="123123",
    host="127.0.0.1",
    port=3306,
    database="127projdb"
)

cur = mydb.cursor()

def handle_login():
    adminusername = "admin"
    adminpassword = "admin"
    username = username_entry.get()
    password = password_entry.get()
    cur.execute("SELECT username, password FROM user")
    rows = cur.fetchall()

    if (username, password) == (adminusername, adminpassword):
        print(f"Welcome back, admin {username}!")
        # adminmenu()  # Implement adminmenu function
    elif any(username in row and password in row for row in rows):
        print(f"\nWelcome back, user {username}!")
        # customermenu(username, password)  # Implement customermenu function
    elif any(username in row for row in rows):
        print(f"\nIncorrect password for user {username}. Try again.")
    else:
        print("\nUser does not exist. Sign up instead.")


def show_login_screen():
    clear_window()

    app.configure(bg="#F0F0F0")

    # Configure grid layout of app window
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=10)
    app.grid_columnconfigure(1, weight=1)

    # Left panel
    left_panel1 = ctk.CTkFrame(app, fg_color="#9ED1F4")
    left_panel1.grid(row=0, column=0, sticky="nsew")

    # Main login frame
    login_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
    login_frame.grid(row=0, column=1, sticky="nsew")

    # Configure grid layout of login_frame
    login_frame.grid_rowconfigure(0, weight=1)
    login_frame.grid_columnconfigure(0, weight=1)

    # Welcome label
    welcome_label = ctk.CTkLabel(login_frame, text="Welcome to", font=("Helvetica", 60))
    welcome_label.pack(anchor="w", pady=(100, 5), padx=(30, 0))

    # Critique frame
    critique_frame = ctk.CTkFrame(login_frame, fg_color="#FFFFFF")
    critique_frame.pack(anchor="w", pady=(5, 100), padx=(30, 0))

    critique_label_1 = ctk.CTkLabel(critique_frame, text="Criti", font=("Helvetica", 60), text_color="#1E90FF")
    critique_label_2 = ctk.CTkLabel(critique_frame, text="qué", font=("Helvetica", 60), text_color="#B89E97")
    critique_label_1.pack(side="left")
    critique_label_2.pack(side="left")

    global username_entry
    username_entry = ctk.CTkEntry(login_frame, placeholder_text="Username", font=("Helvetica", 20), width=500, height=60,
                                  corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                  placeholder_text_color="#A9A9A9", border_color="#B89E97")
    username_entry.pack(anchor="w", pady=(5, 20), padx=30)

    global password_entry
    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", font=("Helvetica", 20), show="*", width=500, height=60,
                                  corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                  placeholder_text_color="#A9A9A9", border_color="#B89E97")
    password_entry.pack(anchor="w", pady=(10, 100), padx=30)

    # Login button
    login_button = ctk.CTkButton(login_frame, text="Login", font=("Helvetica", 20),
                                 width=500, height=60, corner_radius=10, fg_color="#B89E97",
                                 command=handle_login)
    login_button.pack(anchor="w", pady=(20, 5), padx=30)

    # Sign up link
    signup_frame = ctk.CTkFrame(login_frame, fg_color="#FFFFFF")
    signup_frame.pack(anchor="w",pady=(0, 10), padx=30)

    signup_label = ctk.CTkLabel(signup_frame, text="New User?", font=("Helvetica", 15))
    signup_label.pack(anchor="w",side="left")

    signup_link = ctk.CTkButton(signup_frame, text="Sign up here", font=("Helvetica", 15), width=80, height=25,
                                fg_color="#FFFFFF", text_color="#1E90FF", hover_color="#FFFFFF", command=show_signup_screen)
    signup_link.pack(anchor="w",side="left")
def handle_signup():
    username = username_entry.get()
    name = name_entry.get()
    contactnum = contactnum_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        print("Passwords do not match!")
    else:
        cur.execute("INSERT INTO user (name, username, password) VALUES (?, ?, ?)", (name, username, password))
        mydb.commit()
        cur.execute("SELECT userid FROM user WHERE username = ? AND password = ?", (username, password))
        row = cur.fetchone()
        userid = row[0]
        cur.execute("INSERT INTO user_contact (userid, contactnum) VALUES (?, ?)", (userid, contactnum))
        mydb.commit()
        print(f"\nUser {username} has been signed up.")
        # customermenu(username, password)  # Implement customermenu function

def show_signup_screen():
    clear_window()

    app.configure(bg="#F0F0F0")

    # Configure grid layout of app window
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=10)
    app.grid_columnconfigure(1, weight=1)

    # Left panel
    left_panel1 = ctk.CTkFrame(app, fg_color="#9ED1F4")
    left_panel1.grid(row=0, column=0, sticky="nsew")

    # Main sign-up frame
    signup_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
    signup_frame.grid(row=0, column=1, sticky="nsew")

    # Configure grid layout of signup_frame
    signup_frame.grid_rowconfigure(0, weight=1)
    signup_frame.grid_columnconfigure(0, weight=1)

    # Sign up frame
    signup_text = ctk.CTkFrame(signup_frame, fg_color="#FFFFFF")
    signup_text.pack(anchor="w", pady=(100, 50), padx=(30, 0))

    signup_text1 = ctk.CTkLabel(signup_text, text="Sign", font=("Helvetica", 60), text_color="#1E90FF")
    signup_text2 = ctk.CTkLabel(signup_text, text="up", font=("Helvetica", 60), text_color="#B89E97")
    signup_text1.pack(side="left")
    signup_text2.pack(side="left")

    global name_entry
    name_entry = ctk.CTkEntry(signup_frame,
                                placeholder_text="Name", font=("Helvetica", 20), width=500, height=60, corner_radius=30,
                                fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9", border_color="#B89E97")
    name_entry.pack(anchor="w", pady=(5, 20), padx=30)

    global username_entry
    username_entry = ctk.CTkEntry(signup_frame,
                                   placeholder_text="Username", font=("Helvetica", 20), width=500, height=60, corner_radius=30,
                                   fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9", border_color="#B89E97")
    username_entry.pack(anchor="w", pady=(5, 20), padx=30)

    global contactnum_entry
    contactnum_entry = ctk.CTkEntry(signup_frame,
                                  placeholder_text="Contact Number", font=("Helvetica", 20), width=500, height=60,
                                  corner_radius=30, fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9", border_color="#B89E97")
    contactnum_entry.pack(anchor="w", pady=(5, 20), padx=30)

    global password_entry
    password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Password", font=("Helvetica", 20), show="*", width=500, height=60,
                                   corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                   placeholder_text_color="#A9A9A9", border_color="#B89E97")
    password_entry.pack(anchor="w", pady=(5, 20), padx=30)

    global confirm_password_entry
    confirm_password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Confirm Password", font=("Helvetica", 20), show="*", width=500, height=60,
                                           corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                           placeholder_text_color="#A9A9A9", border_color="#B89E97")
    confirm_password_entry.pack(anchor="w", pady=(5, 20), padx=30)

    # Sign Up button
    signup_button = ctk.CTkButton(signup_frame, text="Sign Up", font=("Helvetica", 20),
                                  width=500, height=60, corner_radius=10, fg_color="#B89E97",
                                  command=handle_signup)
    signup_button.pack(anchor="w", pady=(20, 5), padx=30)

    # Login link
    login_frame = ctk.CTkFrame(signup_frame, fg_color="#FFFFFF")
    login_frame.pack(anchor="w", pady=(0, 10), padx=30)

    login_label = ctk.CTkLabel(login_frame, text="Already have an account?", font=("Helvetica", 15))
    login_label.pack(side="left")

    login_link = ctk.CTkButton(login_frame, text="Login here", font=("Helvetica", 15), width=120, height=40,
                               fg_color="#FFFFFF", text_color="#1E90FF", hover_color="#FFFFFF", command=show_login_screen)
    login_link.pack(side="left")

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def start_gui():
    show_login_screen()
    app.mainloop()


start_gui()
