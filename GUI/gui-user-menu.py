import customtkinter as ctk

# Initialize the main window
app = ctk.CTk()
app.geometry("1440x1024")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def show_admin_screen():
    clear_window()

    # Main login frame
    admin_frame = ctk.CTkFrame(app, width=1080, height=1024, fg_color="white")
    admin_frame.place(x = 0, y = 0, anchor="ne")

    # Create and place the Welcome label in the upper left corner of admin_frame
    welcome_label = ctk.CTkLabel(app, text="Welcome!", font=("Arial", 55))
    welcome_label.grid(row=0, column=1, sticky='w', padx=650, pady=20)

    # Create and place the Logout button in the upper right corner of admin_frame
    logout_button = ctk.CTkButton(app, text="Logout", width=50, height=50)
    logout_button.grid(row=0, column=0, sticky='ne', padx=20, pady=20)

    
    # Create and place the button for admin dashboard under the Welcome label
    button_manage_estab = ctk.CTkButton(app, text="Review a product and shop", width=200, height=200, fg_color="#0000FF")
    button_manage_estab.grid(row=1, column=0, padx= 70, pady=(20, 20), sticky='w')

    button_manage_food = ctk.CTkButton(app, text="Review an establishment", width=200, height=200, fg_color= "#D2B48C")
    button_manage_food.grid(row=1, column=1, padx = 70, pady=(20, 20), sticky='w')

    button_manage_view = ctk.CTkButton(app, text="View Reviews", width=200, height=200, fg_color="#ADD8E6")
    button_manage_view.grid(row=2, column=0, padx = 70, pady=(20, 20), sticky='w')

    button_manage_any = ctk.CTkButton(app, text="View All Entries", width=200, height=200, fg_color="#A52A2A")
    button_manage_any.grid(row=2, column=1, padx = 70, pady=(20, 20), sticky='w')

    right_most1 = ctk.CTkFrame(app, width=360, height=1024, fg_color="#D2B48C")
    right_most1.place(x=1440, y=0, anchor="ne")

    right_most2 = ctk.CTkFrame(app, width=270, height=1024, fg_color="#A52A2A")
    right_most2.place(x=1410, y=0, anchor="ne")

    left_most1 = ctk.CTkFrame(app, width=180, height=1024, fg_color="#0000FF")
    left_most1.place(x=1380, y=0, anchor="ne")

    left_most2 = ctk.CTkFrame(app, width=90, height=1024, fg_color="#ADD8E6")
    left_most2.place(x=1340, y=0, anchor="ne")



# Run the application
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def start_gui():
    show_admin_screen()
    app.mainloop()


start_gui()
