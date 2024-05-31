import customtkinter as ctk

app = ctk.CTk()
app.title("Critiqué Login")
app.geometry("1440x1024")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def handle_login():
    username = username_entry.get()
    password = password_entry.get()
    print(f"Username: {username}, Password: {password}")
    # Add login logic here


def show_login_screen():
    clear_window()

    app.configure(bg="#F0F0F0")

    left_panel1 = ctk.CTkFrame(app, width=251, height=1024, fg_color="#9ED1F4")
    left_panel1.grid(row=0, column=0, sticky="nsw")

    left_panel2 = ctk.CTkFrame(app, width=216, height=1024, fg_color="#1E90FF")
    left_panel2.grid(row=0, column=1, sticky="ns")

    right_panel1 = ctk.CTkFrame(app, width=216, height=1024, fg_color="#B89E97")
    right_panel1.grid(row=0, column=3, sticky="ns")

    right_panel2 = ctk.CTkFrame(app, width=251, height=1024, fg_color="#DECCCC")
    right_panel2.grid(row=0, column=4, sticky="nse")

    # Main login frame
    login_frame = ctk.CTkFrame(app, width=506, height=1024, fg_color="#FFFFFF")
    login_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

    # Welcome label
    welcome_label = ctk.CTkLabel(login_frame, text="Welcome to", font=("Helvetica", 36))
    welcome_label.pack(pady=(50, 5))
    critique_frame = ctk.CTkFrame(login_frame, fg_color="#FFFFFF")
    critique_frame.pack(pady=(5, 50))
    critique_label_1 = ctk.CTkLabel(critique_frame, text="Criti", font=("Helvetica", 36), text_color="#1E90FF")
    critique_label_2 = ctk.CTkLabel(critique_frame, text="qué", font=("Helvetica", 36), text_color="#B89E97")
    critique_label_1.pack(side="left")
    critique_label_2.pack(side="left")

    global username_entry
    username_entry = ctk.CTkEntry(login_frame,
                                  placeholder_text="Username", font=("Helvetica", 15), width=300, height=40, corner_radius=30,
                                  fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9")
    username_entry.pack(pady=(5, 10), padx=30)

    global password_entry
    password_entry = ctk.CTkEntry(login_frame, placeholder_text="Password", font=("Helvetica", 15), show="*", width=300, height=40,
                                  corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                  placeholder_text_color="#A9A9A9")
    password_entry.pack(pady=(10, 20))

    # Login button
    login_button = ctk.CTkButton(login_frame, text="Login", font=("Helvetica", 15),
                                 width=150, height=40, corner_radius=10, fg_color="#D2B48C",
                                 command=handle_login)
    login_button.pack(pady=(20, 20))

    # Sign up link
    signup_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
    signup_frame.grid(row=0, column=2, pady=(0, 20))
    signup_label = ctk.CTkLabel(signup_frame, text="New User?", font=("Helvetica", 15))
    signup_label.pack(side="left")
    signup_link = ctk.CTkButton(signup_frame, text="Sign up here", font=("Helvetica", 15), width=80, height=25,
                                fg_color="#FFFFFF", text_color="#1E90FF", hover_color="#FFFFFF", command=show_signup_screen)
    signup_link.pack(side="left")

def handle_signup():
    username = username_entry.get()
    name = name_entry.get()
    contactnum = contactnum_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        print("Passwords do not match!")
        # You can add error handling or display a message to the user
    else:
        print(f"Name: {name}, Username: {username}, Contact Number: {contactnum}, Password: {password}")
        # Add sign-up logic here

def show_signup_screen():
    clear_window()

    app.configure(bg="#F0F0F0")

    left_panel1 = ctk.CTkFrame(app, width=251, height=1024, fg_color="#9ED1F4")
    left_panel1.grid(row=0, column=0, sticky="nsw")

    left_panel2 = ctk.CTkFrame(app, width=216, height=1024, fg_color="#1E90FF")
    left_panel2.grid(row=0, column=1, sticky="ns")

    right_panel1 = ctk.CTkFrame(app, width=216, height=1024, fg_color="#B89E97")
    right_panel1.grid(row=0, column=3, sticky="ns")

    right_panel2 = ctk.CTkFrame(app, width=251, height=1024, fg_color="#DECCCC")
    right_panel2.grid(row=0, column=4, sticky="nse")

    signup_frame = ctk.CTkFrame(app, width=506, height=1024, fg_color="#FFFFFF")
    signup_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ns")

    signup_text = ctk.CTkFrame(signup_frame, fg_color="#FFFFFF")
    signup_text.pack(pady=(5, 50))

    signup_text1 = ctk.CTkLabel(signup_text, text="Sign", font=("Helvetica", 36), text_color="#1E90FF")
    signup_text2 = ctk.CTkLabel(signup_text, text="up", font=("Helvetica", 36), text_color="#B89E97")
    signup_text1.pack(side="left")
    signup_text2.pack(side="left")

    global name_entry
    name_entry = ctk.CTkEntry(signup_frame,
                                placeholder_text="Name", font=("Helvetica", 15), width=300, height=40, corner_radius=30,
                                fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9")
    name_entry.pack(pady=(5, 10), padx=30)

    global username_entry
    username_entry = ctk.CTkEntry(signup_frame,
                                   placeholder_text="Username", font=("Helvetica", 15), width=300, height=40, corner_radius=30,
                                   fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9")
    username_entry.pack(pady=(5, 10), padx=30)

    global contactnum_entry
    contactnum_entry = ctk.CTkEntry(signup_frame,
                                  placeholder_text="Contact Number", font=("Helvetica", 15), width=300, height=40,
                                  corner_radius=30,
                                  fg_color="#E9E9E9", text_color="#000000", placeholder_text_color="#A9A9A9")
    contactnum_entry.pack(pady=(5, 10), padx=30)

    global password_entry
    password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Password", font=("Helvetica", 15), show="*", width=300, height=40,
                                   corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                   placeholder_text_color="#A9A9A9")
    password_entry.pack(pady=(5, 10))

    global confirm_password_entry
    confirm_password_entry = ctk.CTkEntry(signup_frame, placeholder_text="Confirm Password", font=("Helvetica", 15), show="*", width=300, height=40,
                                           corner_radius=30, fg_color="#E9E9E9", text_color="#000000",
                                           placeholder_text_color="#A9A9A9")
    confirm_password_entry.pack(pady=(5, 20))

    signup_button = ctk.CTkButton(signup_frame, text="Sign Up", font=("Helvetica", 15),
                                  width=150, height=40, corner_radius=10, fg_color="#D2B48C",
                                  command=handle_signup)
    signup_button.pack(pady=(20, 20))

    login_frame = ctk.CTkFrame(signup_frame, fg_color="#FFFFFF")
    login_frame.pack(pady=(20, 10))

    login_label = ctk.CTkLabel(login_frame, text="Already have an account?", font=("Helvetica", 15))
    login_label.pack(side="left")

    login_link = ctk.CTkButton(login_frame, text="Login here", font=("Helvetica", 15), width=80, height=25,
                               fg_color="#FFFFFF", text_color="#1E90FF", hover_color="#FFFFFF", command=show_login_screen)
    login_link.pack(side="left")

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def start_gui():
    show_login_screen()
    app.mainloop()


start_gui()
