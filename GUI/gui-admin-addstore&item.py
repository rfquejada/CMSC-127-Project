import customtkinter as ctk

# Initialize the main window
app = ctk.CTk()
app.title("Critiqué - Add Store & Item")
app.geometry("1440x1024")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def add_itemstore_screen():
    app.configure(bg="#F0F0F0")

    #navbar
    main_menu = ctk.CTkFrame(app, width=315, height=950, corner_radius=20, fg_color="#FFFFFF")
    main_menu.grid(row=0, column=0, padx=20, pady=34, sticky="nw")
    main_menu.grid_propagate(0)

    add_item_store_tab_button = ctk.CTkButton(main_menu, text='Add Shop/Item', font=('Helvetica', 20), width=220, height=180, corner_radius=20, fg_color="#1098F7")
    add_item_store_tab_button.grid(row=0, column=0, pady=50, padx=43, sticky='n')

    edit_button = ctk.CTkButton(main_menu, text='Edit or Delete\nShop/Item', text_color='#000000', font=('Helvetica', 20), width=220, height=180, corner_radius=20, fg_color="#E9E9E9")
    edit_button.grid(row=1, column=0, pady=20, padx=43, sticky='n')

    view_button = ctk.CTkButton(main_menu, text='View all entries', text_color='#000000', font=('Helvetica', 20), width=220, height=180, corner_radius=20, fg_color="#E9E9E9")
    view_button.grid(row=2, column=0, pady=20, padx=43, sticky='n')

    logout_button = ctk.CTkButton(main_menu, text='Log Out', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#FF3E3E")
    logout_button.grid(row=4, column=0, pady=100, padx=43, sticky='n')

    #Main Content Frame
    main_content = ctk.CTkFrame(app, width=1050, height=950, corner_radius=20, fg_color="#FFFFFF")
    main_content.grid(row=0, column=1,columnspan=5, padx=20, pady=34, sticky="nw")
    main_content.grid_propagate(0)

    #Content Label
    label = ctk.CTkLabel(main_content, text='Add Store/Item', fg_color='transparent', text_color='#000000', font=('Helvetica', 72))
    label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    #Add Estab Frame
    add_estab = ctk.CTkFrame(main_content, width=473, height=682, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    add_estab.grid(row=1, column=0, padx=20, pady=34, sticky="w")
    add_estab.grid_propagate(0)

    label = ctk.CTkLabel(add_estab, text='Establishment', fg_color='transparent', text_color='#000000', font=('Helvetica', 40))
    label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    estab_name = ctk.CTkTextbox(add_estab, width=369, height=55, corner_radius=20, state='normal')
    estab_name.grid(row=1, column=0, pady=15, padx=25, sticky='w')


    #Add Item Frame
    add_item = ctk.CTkFrame(main_content, width=473, height=682, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    add_item.grid(row=1, column=1, padx=20, pady=34, sticky="w")
    add_item.grid_propagate(0)

    label = ctk.CTkLabel(add_item, text='Item', fg_color='transparent', text_color='#000000', font=('Helvetica', 40))
    label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

# Run the application
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def start_gui():
    add_itemstore_screen()
    app.mainloop()

start_gui()