import customtkinter as ctk
import sys
import mariadb
from tkinter import messagebox

try:
    conn = mariadb.connect(
        password="04302004",
        host="localhost",
        port=3306,
        database="127projdb",
        autocommit=True
    )
except mariadb.Error as e:
    print("Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
global cur
cur = conn.cursor()

# Initialize the main window
app = ctk.CTk()
app.title("Critiqué - Add Store & Item")
app.geometry("1440x1024")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

estab_id = None
estab_name_search = None

item_id = None
item_name_search = None

def handleSearchEstab():
    global estab_id
    global estab_name_search
    estab_input = estab_name_search.get().split()
    print(estab_input)
    if estab_input == []:
        messagebox.showerror("Input Error", "No Input Detected.")
        return
    
    namequery = "SELECT estabid from food_estab where estabname like '%"
    for string in estab_input:
        namequery += (string + '%')
    namequery += "'"

    cur.execute(namequery)
    try:
        estab_id=cur.fetchone()[0]
    except:
        messagebox.showerror("Input Error", "No Record of Establishment!")
        return 
    
    messagebox.showinfo("Match Found!", "Found a Match: Input new details in the right area.")
        
def handleSearchItem():
    global item_id
    global item_name_search
    global estab_name_search
    item_input = item_name_search.get().split()
    print(item_input)
    if item_input == []:
        messagebox.showerror("Input Error", "No Input Detected.")
        return
    
    namequery = "SELECT itemid from food_item where itemname like '%"
    for string in item_input:
        namequery += (string + '%')
    namequery += "'"

    estab_input = estab_name_search.split()
    namequery += ("AND estabid = (select estabid from food_estab where estabname like '%")
    for string in estab_input:
        namequery += (string + '%')
    namequery += ("')")

    cur.execute(namequery)
    try:
        item_id=cur.fetchone()[0]
    except:
        messagebox.showerror("Input Error", "No Record of Item!")
        return 
    
    messagebox.showinfo("Match Found!", "Found a Match: Input new details in the right area.")
    return

def handleEstabUpdate():
    global estab_id
    if estab_id == None:
        messagebox.showerror("Missing ID", "No matching establishment! Search product with the search module first.")
        return
    
    global new_estab_address
    global new_estab_name
    if new_estab_address == None or new_estab_name == None:
        messagebox.showerror("Invalid Input", "Please fill up the fields.")
        return
    
    name = str(new_estab_name)
    address = str(new_estab_address)
    
    
    cur.execute('Update food_estab set estabname = ?, branch_address = ? where estabid = ?', (name, address, estab_id))
    messagebox.showinfo("Update Complete!", "Details Updated!")
    
    
def handleItemUpdate():
    global item_id
    if item_id == None:
        messagebox.showerror("Missing ID", "No matching product! Search product with the search module first.")
        return

    global new_item_name
    global new_item_price
    if new_item_name == None or new_item_price == None:
        messagebox.showerror("Invalid Input", "Please fill up the fields.")
        return

    name = str(new_item_name)

    try:
        price = int(new_item_price)
    except:
        messagebox.showerror("Invalid Type", "Please input a valid number for price")
        return
    
    cur.execute('Update food_item set itemname = ?, price = ? where productid = ?', (name, price, item_id))
    messagebox.showinfo("Update Complete!", "Details Updated!")




def edit_itemstore_screen():
    app.configure(bg="#F0F0F0")

    #navbar
    main_menu = ctk.CTkFrame(app, width=315, height=950, corner_radius=20, fg_color="#FFFFFF")
    main_menu.grid(row=0, column=0, padx=20, pady=34, sticky="nw")
    main_menu.grid_propagate(0)

    add_item_store_tab_button = ctk.CTkButton(main_menu, text='Add Shop/Item', text_color='#000000', font=('Helvetica', 20), width=220, height=180, corner_radius=20, fg_color="#E9E9E9")
    add_item_store_tab_button.grid(row=0, column=0, pady=50, padx=43, sticky='n')

    edit_button = ctk.CTkButton(main_menu, text='Edit or Delete\nShop/Item', font=('Helvetica', 20), width=220, height=180, corner_radius=20, fg_color="#1098F7")
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
    label = ctk.CTkLabel(main_content, text='Edit Store/Item', fg_color='transparent', text_color='#000000', font=('Helvetica', 72))
    label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    #Edit TabView
    edit_tab = ctk.CTkTabview(main_content, width=950, height=750, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    edit_tab.grid(row=1, column=0, padx=50, pady=15, sticky="w")
    edit_tab.grid_propagate(0)

    edit_tab.add("Establishment")
    edit_tab.add("Item")

    #Search Estab Frame
    search_estab_frame = ctk.CTkFrame(edit_tab.tab("Establishment"), width=350, height=300, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    search_estab_frame.grid(row=0, column=0, padx = 30, pady= 15, sticky='nw')
    search_estab_frame.grid_propagate(0)

    search_label = ctk.CTkLabel(search_estab_frame, text='Search', fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    search_label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    estab_name_label = ctk.CTkLabel(search_estab_frame, text='Establishment Name', fg_color='transparent', text_color='#000000', font=('Helvetica', 16))
    estab_name_label.grid(row=1, column=0, pady=15, padx=25, sticky='w')

    global estab_name_search
    estab_name_search = ctk.CTkEntry(search_estab_frame, placeholder_text="Insert Establishment Name Here..." ,width=300, height=35, corner_radius=20, state='normal')
    estab_name_search.grid(row=2, column=0, pady=1, padx=25, sticky='w')

    submit_button = ctk.CTkButton(search_estab_frame, text='Search', width=80, height=40, command=lambda:handleSearchEstab())
    submit_button.grid(row=3, column=0, pady=25, padx=25, sticky='sw')

    #Edit Estab Frame
    global estab_id
    edit_estab_frame = ctk.CTkFrame(edit_tab.tab("Establishment"), width=450, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    edit_estab_frame.grid(row=0, column=1, padx = 30, pady= 15, sticky='ne')
    edit_estab_frame.grid_propagate(0)

    label = ctk.CTkLabel(edit_estab_frame, text='Establishment', fg_color='transparent', text_color='#000000', font=('Helvetica', 32))
    label.grid(row=0, column=0, pady=15, padx=10, sticky='nw')

    global new_estab_name
    global new_estab_address
    new_estab_name_label = ctk.CTkLabel(edit_estab_frame, text="New Establishment Name", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_estab_name_label.grid(row = 1, column = 0, pady=15, padx=15, sticky='w')

    new_estab_name = ctk.CTkEntry(edit_estab_frame,placeholder_text="Establishment name..." ,width=369, height=55, corner_radius=20, state='normal')
    new_estab_name.grid(row=2, column=0, pady=15, padx=25, sticky='w')

    new_estab_address_label = ctk.CTkLabel(edit_estab_frame, text="New Branch Address", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_estab_address_label.grid(row = 3, column = 0, padx=15, sticky='w')

    new_estab_address = ctk.CTkEntry(edit_estab_frame,width=369, placeholder_text="Branch address...", height=55, corner_radius=20, state='normal')
    new_estab_address.grid(row=4, column=0, pady=15, padx=25, sticky='w')

    submit_button = ctk.CTkButton(edit_estab_frame, text='Submit', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleEstabUpdate())
    submit_button.grid(row=5, column=0, pady=15, padx=25, sticky='w')

    #Search Item Frame
    search_item_frame = ctk.CTkFrame(edit_tab.tab("Item"), width=350, height=300, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    search_item_frame.grid(row=0, column=0, padx = 30, pady= 15, sticky='nw')
    search_item_frame.grid_propagate(0)

    search_label = ctk.CTkLabel(search_item_frame, text='Search', fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    search_label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    item_name_label = ctk.CTkLabel(search_item_frame, text='Item Name', fg_color='transparent', text_color='#000000', font=('Helvetica', 16))
    item_name_label.grid(row=1, column=0, pady=15, padx=25, sticky='w')

    global item_name_search
    item_name_search = ctk.CTkEntry(search_item_frame, placeholder_text="Insert Item Name Here..." ,width=300, height=35, corner_radius=20, state='normal')
    item_name_search.grid(row=2, column=0, pady=1, padx=25, sticky='w')

    submit_button = ctk.CTkButton(search_item_frame, text='Search', width=80, height=40, command=lambda: handleSearchItem())
    submit_button.grid(row=3, column=0, pady=25, padx=25, sticky='sw')
    
    #Edit Item Frame
    global item_id
    edit_item_frame = ctk.CTkFrame(edit_tab.tab("Item"), width=450, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    edit_item_frame.grid(row=0, column=1, padx = 30, pady= 15, sticky='ne')
    edit_item_frame.grid_propagate(0)

    label = ctk.CTkLabel(edit_item_frame, text='Item', fg_color='transparent', text_color='#000000', font=('Helvetica', 32))
    label.grid(row=0, column=0, pady=15, padx=15, sticky='nw')

    global new_item_name
    global new_item_price
    new_item_name_label = ctk.CTkLabel(edit_item_frame, text="New Item Name", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_item_name_label.grid(row = 1, column = 0, pady=5, padx=15, sticky='w')

    new_item_name = ctk.CTkEntry(edit_item_frame,placeholder_text="Item name..." ,width=369, height=55, corner_radius=20, state='normal')
    new_item_name.grid(row=2, column=0, pady=5, padx=25, sticky='w')

    new_item_price_label = ctk.CTkLabel(edit_item_frame, text="New Price", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_item_price_label.grid(row = 3, column = 0, pady=15, padx=15, sticky='w')

    new_item_price = ctk.CTkEntry(edit_item_frame,width=369, height=55, placeholder_text='Price...', corner_radius=20, state='normal')
    new_item_price.grid(row=4, column=0, pady=5, padx=25, sticky='w')

    submit_button = ctk.CTkButton(edit_item_frame, text='Update', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleItemUpdate())
    submit_button.grid(row=6, column=0, pady=15, padx=25, sticky='w')

    

    # add_item = ctk.CTkFrame(main_content, width=300, height=300, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    # add_item.grid(row=2, column=0, padx=20, pady=34, sticky="w")
    # add_item.grid_propagate(0)

# Run the application
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()
        conn.close()

def start_gui():
    edit_itemstore_screen()
    app.mainloop()

start_gui()
