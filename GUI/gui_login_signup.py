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
    global logged_in_username, logged_in_password
    adminusername = "admin"
    adminpassword = "admin"
    username = username_entry.get()
    password = password_entry.get()
    cur.execute("SELECT username, password FROM user")
    rows = cur.fetchall()

    if (username, password) == (adminusername, adminpassword):
        print(f"Welcome back, admin {username}!")
        # show_admin_screen()  # Implement adminmenu function
    elif any(username in row and password in row for row in rows):
        print(f"\nWelcome back, user {username}!")
        logged_in_username = username
        logged_in_password = password
        customermenu(username, password)  # Implement customermenu function
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

def customermenu(username, password):
    clear_window()

    app.configure(bg="#F0F0F0")

    # Configure grid layout of app window
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_columnconfigure(3, weight=1)
    app.grid_columnconfigure(4, weight=50)

    # Left panel
    left_panel1 = ctk.CTkFrame(app, fg_color="#9ED1F4", width=100)
    left_panel1.grid(row=0, column=0, sticky="nsew")

    left_panel2 = ctk.CTkFrame(app, fg_color="#1098F7", width=75)
    left_panel2.grid(row=0, column=1, sticky="nsew")

    left_panel3 = ctk.CTkFrame(app, fg_color="#B89E97", width=75)
    left_panel3.grid(row=0, column=2, sticky="nsew")

    left_panel4 = ctk.CTkFrame(app, fg_color="#DECCCC", width=100)
    left_panel4.grid(row=0, column=3, sticky="nsew")

    # Main customer menu frame
    customer_menu_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
    customer_menu_frame.grid(row=0, column=4, sticky="nsew")

    # Configure grid layout of customer_menu_frame
    customer_menu_frame.grid_columnconfigure(0, weight=1)
    customer_menu_frame.grid_columnconfigure(1, weight=1)
    customer_menu_frame.grid_columnconfigure(2, weight=1)


    # Welcome message
    welcome_label = ctk.CTkLabel(customer_menu_frame, text=f"Welcome!", font=("Helvetica", 45))
    welcome_label.grid(row=0, column=2, pady=(40, 20), padx=(0, 0))

    # Button options grid
    button_options = [
        "Review a \nFood Item",
        "Review an \nEstablishment",
        "Update a \nReview",
        "Delete a \nReview",
        "Search \nFood Item",
        "View"
    ]

    # Define colors for buttons
    button_colors = [
        "#1098F7",
        "#DECCCC",
        "#1098F7",
        "#B89E97",
        "#9ED1F4",
        "#B89E97"
    ]

    # Define commands for buttons
    button_commands = [
        select_estab_review_food_screen,
        show_review_establishment_screen,
        temp_command,
        temp_command,
        temp_command,
        temp_command
    ]

    # Create buttons and place them in a grid
    for i, (option, color, command) in enumerate(zip(button_options, button_colors, button_commands)): #missing button commands
        row = i // 3 + 1
        col = i % 3
        button = ctk.CTkButton(customer_menu_frame, text=option, width=250, height=250, fg_color=color, command=command,
                               font=("Helvetica", 30), text_color="#000000")
        button.grid(row=row, column=col, padx=10, pady=50)

    # Logout button
    logout_button = ctk.CTkButton(customer_menu_frame, text="Logout", font=("Helvetica", 28), fg_color="#FF3E3E",
                                  command=show_login_screen)
    logout_button.grid(row=0, column=0, padx=0, pady=(50, 10))

def handle_foodestab_review():
    selected_establishment = establishment_label.cget("text").replace("Establishment: ", "")
    rating = rating_combo.get()
    review_body = review_body_entry.get("1.0", "end-1c")
    print(selected_establishment)

    if not selected_establishment or not rating or not review_body:
        print("All fields must be filled out.")
    else:
        cur.execute("SELECT estabid FROM food_estab WHERE estabname = ?", (selected_establishment,))
        estabid_row = cur.fetchone()
        estabid = estabid_row[0]
        if estabid:
            userid = fetchUserId(logged_in_username, logged_in_password)  # Replace with actual user details
            dateofreview = datetime.datetime.now()
            query = "insert into user_reviews_foodestab (userid, estabid, rating, date_of_review, body) values (?, ?, ?, ?, ?)"
            params = (userid, estabid, rating, dateofreview, review_body)
            execute_query(query, params)
            print(f"Review for {selected_establishment} submitted successfully.")

            # Updates the average rating of the establishment
            getRatingQuery = "select avg(rating) from user_reviews_foodestab where estabid = ?"
            getRatingParam = (estabid,)
            avg_rating = fetch(getRatingQuery, getRatingParam)[0]
            updateEstabRating(avg_rating, estabid)

            customermenu(logged_in_username, logged_in_password)
        else:
            print("Establishment not found.")

def show_review_establishment_screen():
    clear_window()

    app.configure(bg="#F0F0F0")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=5)

    panel_frame = ctk.CTkFrame(app, fg_color="#DECCCC")
    panel_frame.grid(row=0, column=0, sticky="nsew")

    options = [
        ("Review a \nFood Item"),
        ("Review an \nEstablishment"),
        ("Update a \nReview"),
        ("Delete a \nReview"),
        ("Search \nFood Item"),
        ("View")
    ]

    # Create buttons for each option and place them in the panel_frame
    for i, (text) in enumerate(options):
        button = ctk.CTkButton(panel_frame, text=text, font=("Helvetica", 12), width=100, height=100)
        button.grid(row=i, column=0, padx=10, pady=10)

    logout_button = ctk.CTkButton(panel_frame, text="Logout", font=("Helvetica", 18), fg_color="#FF3E3E",
                                  command=show_login_screen)
    logout_button.grid(row=len(options), column=0, padx=5, pady=(10, 10))

    screen_frame = ctk.CTkFrame(app, fg_color="#F1F1F1")
    screen_frame.grid(row=0, column=1, sticky="nsew")

    screen_frame.grid_columnconfigure(0, weight=10)
    screen_frame.grid_columnconfigure(1, weight=1)

    screen_title = ctk.CTkLabel(screen_frame, text="Shop Review", font=("Helvetica", 60))
    screen_title.grid(sticky="w", row=0, column=0, padx=15, pady=20)

    establishments_frame = ctk.CTkFrame(screen_frame, fg_color="#FFFFFF", corner_radius=10)
    establishments_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)

    establishments_label = ctk.CTkLabel(establishments_frame, text="Establishments", font=("Helvetica", 25))
    establishments_label.grid(row=0, column=0, pady=(20, 0), padx=15)

    headers = ["Name", "Address", "Rating"]
    for i, header in enumerate(headers):
        header_label = ctk.CTkLabel(establishments_frame, text=header, font=("Helvetica", 20))
        header_label.grid(row=1, column=i, pady=(20, 10))

    cur.execute("select estabname, branch_address, rating from food_estab")
    establishments = cur.fetchall()

    for i, (name, address, rating) in enumerate(establishments):
        # Display Name
        establishment_name_label = ctk.CTkLabel(establishments_frame, text=name, font=("Helvetica", 20))
        establishment_name_label.grid(row=i + 2, column=0, padx=20, pady=5, sticky="w")

        # Display Address
        establishment_address_label = ctk.CTkLabel(establishments_frame, text=address, font=("Helvetica", 20))
        establishment_address_label.grid(row=i + 2, column=1, padx=20, pady=5, sticky="w")

        # Display Rating
        establishment_rating_label = ctk.CTkLabel(establishments_frame, text=str(rating), font=("Helvetica", 20))
        establishment_rating_label.grid(row=i + 2, column=2, padx=20, pady=5, sticky="w")

        # Select Button
        select_button = ctk.CTkButton(establishments_frame, text="Select",
                                      command=lambda establishment=name: select_establishment(establishment))
        select_button.grid(row=i + 2, column=3, padx=20, pady=5)

    review_frame = ctk.CTkFrame(screen_frame, fg_color="#F1F1F1", corner_radius=10)
    review_frame.grid(row=1, column=1, sticky="nse", padx=20, pady=0)

    global establishment_label
    selected_estab_frame = ctk.CTkFrame(review_frame, fg_color="#FFFFFF", corner_radius=10)
    selected_estab_frame.grid(row=0, column=0, sticky="nsew", pady=10)
    establishment_label = ctk.CTkLabel(selected_estab_frame, text="Establishment: ", font=("Helvetica", 20))
    establishment_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    input_frame = ctk.CTkFrame(review_frame, fg_color="#FFFFFF", corner_radius=10)
    input_frame.grid(row=1, column=0)
    review_label = ctk.CTkLabel(input_frame, text="Review", font=("Helvetica", 25))
    review_label.grid(row=1, column=0, pady=20, padx=10, sticky="w")

    rating_label = ctk.CTkLabel(input_frame, text="Rating:", font=("Helvetica", 20))
    rating_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    global rating_combo
    rating_combo = ctk.CTkComboBox(input_frame, values=[str(i) for i in range(1, 6)], font=("Helvetica", 15))
    rating_combo.grid(row=2, column=0, pady=10, padx=10)

    review_body_label = ctk.CTkLabel(input_frame, text="Review Body (max: 200 chars):", font=("Helvetica", 20))
    review_body_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    global review_body_entry
    review_body_entry = ctk.CTkTextbox(input_frame, width=400, height=200, font=("Helvetica", 20))
    review_body_entry.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    submit_button = ctk.CTkButton(input_frame, text="Submit", font=("Helvetica", 20), command=handle_foodestab_review)
    submit_button.grid(row=5, column=0, columnspan=2, pady=20, padx=10)

def select_establishment(name):
    establishment_label.configure(text=f"Establishment: {name}")

def select_estab_review_food_screen():
    clear_window()

    app.configure(bg="#F0F0F0")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=15)

    panel_frame = ctk.CTkFrame(app, fg_color="#FFFFFF")
    panel_frame.grid(row=0, column=0, sticky="nsew")

    options = [
        ("Review a \nFood Item"),
        ("Review an \nEstablishment"),
        ("Update a \nReview"),
        ("Delete a \nReview"),
        ("Search \nFood Item"),
        ("View")
    ]

    # Create buttons for each option and place them in the panel_frame
    for i, (text) in enumerate(options):
        button = ctk.CTkButton(panel_frame, text=text, font=("Helvetica", 16), width=100, height=100,
                               fg_color="#F0F0F0", text_color="#000000")
        button.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")

    logout_button = ctk.CTkButton(panel_frame, text="Logout", font=("Helvetica", 18), fg_color="#FF3E3E",
                                  command=show_login_screen)
    logout_button.grid(row=len(options), column=0, padx=5, pady=(10, 10))

    screen_frame = ctk.CTkFrame(app, fg_color="#F1F1F1")
    screen_frame.grid(row=0, column=1, sticky="nsew")

    screen_frame.grid_columnconfigure(0, weight=10)
    screen_frame.grid_columnconfigure(1, weight=1)
    screen_frame.grid_rowconfigure(0, weight=1)
    screen_frame.grid_rowconfigure(1, weight=15)


    screen_title = ctk.CTkLabel(screen_frame, text="Shop Review", font=("Helvetica", 60))
    screen_title.grid(sticky="w", row=0, column=0, padx=15, pady=20)

    establishments_frame = ctk.CTkFrame(screen_frame, fg_color="#FFFFFF", corner_radius=10)
    establishments_frame.grid(row=1, column=0, sticky="nsw", padx=20, pady=0)

    establishments_label = ctk.CTkLabel(establishments_frame, text="Establishments", font=("Helvetica", 25))
    establishments_label.grid(row=0, column=0, pady=(20, 0), padx=15)

    headers = ["Name", "Address", "Rating"]
    for i, header in enumerate(headers):
        header_label = ctk.CTkLabel(establishments_frame, text=header, font=("Helvetica", 25))
        header_label.grid(row=1, column=i, pady=(20, 10))

    cur.execute("select estabname, branch_address, rating from food_estab")
    establishments = cur.fetchall()

    for i, (name, address, rating) in enumerate(establishments):
        # Display Name
        establishment_name_label = ctk.CTkLabel(establishments_frame, text=name, font=("Helvetica", 25))
        establishment_name_label.grid(row=i + 2, column=0, padx=20, pady=5, sticky="w")

        # Display Address
        establishment_address_label = ctk.CTkLabel(establishments_frame, text=address, font=("Helvetica", 25))
        establishment_address_label.grid(row=i + 2, column=1, padx=20, pady=5, sticky="w")

        # Display Rating
        establishment_rating_label = ctk.CTkLabel(establishments_frame, text=str(rating), font=("Helvetica", 25))
        establishment_rating_label.grid(row=i + 2, column=2, padx=20, pady=5, sticky="w")

        # Select Button
        select_button = ctk.CTkButton(establishments_frame, text="Select",
                                      command=lambda establishment=name: show_review_food_screen(establishment))
        select_button.grid(row=i + 2, column=3, padx=20, pady=5)

def handle_fooditem_review():
    selected_food = food_item_label.cget("text").replace("Food Item: ", "")
    rating = rating_combo.get()
    review_body = review_body_entry.get("1.0", "end-1c")

    if not selected_food or not rating or not review_body:
        print("All fields must be filled out.")
    else:
        cur.execute("SELECT productid FROM food_item WHERE itemname = ?", (selected_food,))
        productid_row = cur.fetchone()
        productid = productid_row[0]

        cur.execute("select estabid from food_item where productid = ?", (productid,))
        estabid_row = cur.fetchone()
        estabid = estabid_row[0]
        if productid:
            userid = fetchUserId(logged_in_username, logged_in_password)  # Replace with actual user details
            dateofreview = datetime.datetime.now()
            query = "insert into user_reviews_foodestab_item (userid, estabid, productid, rating, date_of_review, body) values (?, ?, ?, ?, ?, ?)"
            params = (userid, estabid, productid, rating, dateofreview, review_body)
            execute_query(query, params)
            print(f"Review for {selected_food} submitted successfully.")

            # Updates the average rating of the establishment
            getRatingQuery = "select avg(rating) from user_reviews_foodestab_item where estabid = ?"
            getRatingParam = (estabid,)
            avg_rating = fetch(getRatingQuery, getRatingParam)[0]
            updateFoodItemRating(avg_rating, estabid, productid)

            customermenu(logged_in_username, logged_in_password)
        else:
            print("Establishment not found.")
def show_review_food_screen(establishment):
    clear_window()

    app.configure(bg="#F0F0F0")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=5)

    panel_frame = ctk.CTkFrame(app, fg_color="#DECCCC")
    panel_frame.grid(row=0, column=0, sticky="nsew")

    options = [
        ("Review a \nFood Item"),
        ("Review an \nEstablishment"),
        ("Update a \nReview"),
        ("Delete a \nReview"),
        ("Search \nFood Item"),
        ("View")
    ]

    # Create buttons for each option and place them in the panel_frame
    for i, (text) in enumerate(options):
        button = ctk.CTkButton(panel_frame, text=text, font=("Helvetica", 12), width=100, height=100)
        button.grid(row=i, column=0, padx=10, pady=10)

    logout_button = ctk.CTkButton(panel_frame, text="Logout", font=("Helvetica", 18), fg_color="#FF3E3E",
                                  command=show_login_screen)
    logout_button.grid(row=len(options), column=0, padx=5, pady=(10, 10))

    screen_frame = ctk.CTkFrame(app, fg_color="#F1F1F1")
    screen_frame.grid(row=0, column=1, sticky="nsew")

    screen_frame.grid_columnconfigure(0, weight=10)
    screen_frame.grid_columnconfigure(1, weight=1)

    screen_title = ctk.CTkLabel(screen_frame, text="Food Review", font=("Helvetica", 60))
    screen_title.grid(sticky="w", row=0, column=0, padx=15, pady=20)

    food_items_frame = ctk.CTkFrame(screen_frame, fg_color="#FFFFFF", corner_radius=10)
    food_items_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)

    food_items_label = ctk.CTkLabel(food_items_frame, text="Food Items", font=("Helvetica", 25))
    food_items_label.grid(row=0, column=0, pady=(20, 0), padx=15)

    headers = ["Name", "Price", "Rating"]
    for i, header in enumerate(headers):
        header_label = ctk.CTkLabel(food_items_frame, text=header, font=("Helvetica", 20))
        header_label.grid(row=1, column=i, pady=(20, 10))

    # Fetch food items from the database
    cur.execute("select estabid from food_estab where estabname = ?", (establishment, ))
    estabid = cur.fetchone()[0]
    cur.execute("select itemname, price, rating from food_item where estabid = ? ", (estabid, ))
    food_items = cur.fetchall()

    for i, (name, price, rating) in enumerate(food_items):
        # Display Name
        food_name_label = ctk.CTkLabel(food_items_frame, text=name, font=("Helvetica", 20))
        food_name_label.grid(row=i + 2, column=0, padx=20, pady=5, sticky="w")

        # Display Price
        food_price_label = ctk.CTkLabel(food_items_frame, text=price, font=("Helvetica", 20))
        food_price_label.grid(row=i + 2, column=1, padx=20, pady=5, sticky="w")

        # Display Rating
        food_rating_label = ctk.CTkLabel(food_items_frame, text=rating, font=("Helvetica", 20))
        food_rating_label.grid(row=i + 2, column=2, padx=20, pady=5, sticky="w")

        # Select Button
        select_button = ctk.CTkButton(food_items_frame, text="Select",
                                      command=lambda food=name: select_food(food))
        select_button.grid(row=i + 2, column=3, padx=20, pady=5)

    review_frame = ctk.CTkFrame(screen_frame, fg_color="#F1F1F1", corner_radius=10)
    review_frame.grid(row=1, column=1, sticky="nse", padx=20, pady=0)

    global establishment_label
    selected_estab_frame = ctk.CTkFrame(review_frame, fg_color="#FFFFFF", corner_radius=10)
    selected_estab_frame.grid(row=0, column=0, sticky="nsew", pady=10)
    establishment_label = ctk.CTkLabel(selected_estab_frame, text=f"Establishment: {establishment}",
                                       font=("Helvetica", 20))
    establishment_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    global food_item_label
    food_item_label = ctk.CTkLabel(selected_estab_frame, text="Food Item: ",
                                       font=("Helvetica", 20))
    food_item_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    input_frame = ctk.CTkFrame(review_frame, fg_color="#FFFFFF", corner_radius=10)
    input_frame.grid(row=1, column=0)
    review_label = ctk.CTkLabel(input_frame, text="Review", font=("Helvetica", 25))
    review_label.grid(row=1, column=0, pady=20, padx=10, sticky="w")

    rating_label = ctk.CTkLabel(input_frame, text="Rating:", font=("Helvetica", 20))
    rating_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    global rating_combo
    rating_combo = ctk.CTkComboBox(input_frame, values=[str(i) for i in range(1, 6)], font=("Helvetica", 15))
    rating_combo.grid(row=2, column=1, pady=10, padx=10)

    review_body_label = ctk.CTkLabel(input_frame, text="Review Body (max: 200 chars):", font=("Helvetica", 20))
    review_body_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    global review_body_entry
    review_body_entry = ctk.CTkTextbox(input_frame, width=400, height=200, font=("Helvetica", 20))
    review_body_entry.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

    submit_button = ctk.CTkButton(input_frame, text="Submit", font=("Helvetica", 20),
                                  command=lambda: handle_fooditem_review())
    submit_button.grid(row=5, column=0, columnspan=2, pady=20, padx=10)



def select_food(name):
    food_item_label.configure(text=f"Food Item: {name}")

def temp_command():
    print("TEMP COMMAND")

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def start_gui():
    show_login_screen()
    app.mainloop()


start_gui()
