import customtkinter as ctk
from tkinter import messagebox
import mariadb
import sys

# Initialize the main window
app = ctk.CTk()
app.geometry("1440x1024")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def create_connection():
    try:
        conn = mariadb.connect(
            password="04302004",
            host="localhost",
            port=3306,
            database="127projdb",
            autocommit=True
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def check_estabid_exists(cur, estabid):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM food_estab WHERE estabid = ?", (estabid,))
    count = cur.fetchone()[0]
    return count > 0 # 0 if not existing & 1 if it exists

# Checks if estabid is existing in food establishment contact table
def check_estabid_in_contact_exists(cur, estabid):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM estab_contact WHERE estabid = ?", (estabid,))
    count = cur.fetchone()[0]
    return count > 0 # 0 if not existing & 1 if it exists

# Checks if estabid is existing in food establishment table
def check_estabid_exists_in_item(cur, estabid):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM food_item WHERE estabid = ?", (estabid,))
    count = cur.fetchone()[0]
    return count > 0 # 0 if not existing & 1 if it exists

#function that gets establishment_id
def search_food_establishment_id(cur, estabname):
    estab = estabname.split()
    namequery = ("select estabid from food_estab where estabname like '%")
    for string in estab:
        namequery += (string + '%')
    namequery += "'"

    cur.execute(namequery)
    result = cur.fetchone()
    
    if result is None:
        print("Establishment not found.")
        return
    
    return result[0]

#function that gets product_id
def search_food_product_id(cur, estabid):
    cur.execute("SELECT productid FROM food_item WHERE estabid=?", (estabid,))
    result = cur.fetchone()
    
    if result is None:
        print("Item not found.")
        return
    
    return result[0]

def get_values_estab():
    global estab_name
    global estab_name_address
    global contact_num
    
    estabname = estab_name.get()
    branch_address = estab_name_address.get()
    contactnum = contact_num.get() 
    
    if contactnum.isdigit()==True:
        if len(estabname) > 50 or len(branch_address) > 50 or len(contactnum) > 11:
            print("There has been a problem on one of the attributes inputted")
            messagebox.showerror("Input Error", "There has been a problem with one of the attributes inputted")
            return
        else:
            print("Food Establishment Details Added To The Food Establishment Table\n")
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO food_estab(estabname, branch_address) VALUES (?, ?)", (estabname, branch_address))
            conn.commit()
            estabid = search_food_establishment_id(cur, estabname)
            if check_estabid_exists(cur, estabid) == 0:
                return
            else:
                cur.execute("INSERT INTO estab_contact(estabid, contactnum) VALUES (?, ?)", (estabid, contactnum))
                conn.commit()
            cur.close()
            conn.close()
            print("Establishment Name:", estabname)
            print("Branch Address:", branch_address)
            print("Contact Number:", contactnum)
            messagebox.showinfo("Success", "Details saved successfully")
            estab_name.configure(state='disabled')
            estab_name_address.configure(state='disabled')
            contact_num.configure(state='disabled')
    else:
        messagebox.showerror("Input Error", "There has been a problem with contact number inputted") 
    
def reset_form_fields():
    global estab_name
    global estab_name_address
    global contact_num
    estab_name.configure(state='normal')
    estab_name_address.configure(state='normal')
    contact_num.configure(state='normal')
    estab_name.delete(0, 'end')
    estab_name_address.delete(0, 'end')
    contact_num.delete(0,'end')

def get_values_item():
    global product_name
    global price_var
    global selling_food_estab
    global food_type
    global second_food_type
    
    itemname = product_name.get()
    price = price_var.get()
    estabname = selling_food_estab.get()
    foodtype = food_type.get()
    foodtype1 = second_food_type.get()
    conn = create_connection()
    cur = conn.cursor()


    estabid = search_food_establishment_id(cur, estabname)
    if estabid is None:
        return
    if(price.isdigit()==True): 
        print("item name: ", itemname)
        print("price: ", price)
        print("estab name: ", estabname)
        print("1 foodtype: ", foodtype)
        print("2 foodtype: ", foodtype1)
        #add mo na lang function dito di ko kasi saulo paano mo ginagawa yung inyo
        cur.execute("INSERT INTO food_item(itemname, price, estabid) VALUES(?,?,?)", (itemname, price, estabid))
        cur.execute("SELECT productid from food_item where itemname=? and estabid=?", (itemname, estabid))
        itemid = cur.fetchone()[0]

        cur.execute("INSERT INTO food_type(productid, foodtype) VALUES (?,?)", (itemid, foodtype))
        
        if foodtype1 != None or foodtype1 != "":
            cur.execute("INSERT INTO food_type(productid, foodtype) VALUES (?,?)", (itemid, foodtype1))


        product_name.configure(state='disabled')
        price_var.configure(state='disabled')
        selling_food_estab.configure(state='disabled')
        food_type.configure(state='disabled')
        second_food_type.configure(state='disabled')
        messagebox.showinfo("Success", "Details saved successfully")
        reset_form_fields_items()
    else:
        messagebox.showerror("Input Error", "There has been a problem with price input")

def reset_form_fields_items():
    global product_name
    global price_var
    global selling_food_estab
    global food_type
    global second_food_type
    product_name.configure(state='normal')
    price_var.configure(state='normal')
    selling_food_estab.configure(state='normal')
    food_type.configure(state='normal')
    second_food_type.configure(state='normal')
    product_name.delete(0, 'end')
    price_var.delete(0, 'end')
    selling_food_estab.delete(0,'end')
    food_type.delete(0,'end')
    second_food_type.delete(0,'end')

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

    global estab_name
    global estab_name_address
    global contact_num
    
    estab_name_label = ctk.CTkLabel(add_estab, text="Establishment Name", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    estab_name_label.grid(row = 1, column = 0)
    estab_name = ctk.CTkEntry(add_estab,placeholder_text="<Establishment Name> - <General Location>" ,width=400, height=55, corner_radius=20, state='normal')
    estab_name.grid(row=2, column=0, pady=15, padx=25, sticky='w')

    estab_name_address_label = ctk.CTkLabel(add_estab, text="Branch Address", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    estab_name_address_label.grid(row = 3, column = 0)
    estab_name_address = ctk.CTkEntry(add_estab,width=400, height=55, corner_radius=20, state='normal')
    estab_name_address.grid(row=4, column=0, pady=15, padx=25, sticky='w')

    contact_number_label = ctk.CTkLabel(add_estab, text="Contact Number", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    contact_number_label.grid(row = 5, column = 0)
    contact_num = ctk.CTkEntry(add_estab, placeholder_text="00000000000", width=400, height=55, corner_radius=20, state='normal')
    contact_num.grid(row=6, column=0, pady=15, padx=25, sticky='w')

    submit_button = ctk.CTkButton(add_estab, text='Submit', text_color='#FFFFFF', font=('Helvetica', 16), width=100, height=52, corner_radius=10, fg_color="#b89e97", command=lambda: get_values_estab())
    submit_button.grid(row=11, column=0, pady=15, padx=24, sticky='w')

    reset_button = ctk.CTkButton(add_estab, text='Reset', text_color='#FFFFFF', font=('Helvetica', 16), width=100, height=52, corner_radius=10, fg_color="#FF3E3E", command=lambda: reset_form_fields())
    reset_button.grid(row=11, column=0, pady=15, padx=24, sticky='e')

    #Add Item Frame
    add_item = ctk.CTkFrame(main_content, width=473, height=682, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    add_item.grid(row=1, column=1, padx=20, pady=34, sticky="w")
    add_item.grid_propagate(0)

    label = ctk.CTkLabel(add_item, text='Item', fg_color='transparent', text_color='#000000', font=('Helvetica', 40))
    label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    global product_name
    global price_var
    global selling_food_estab
    global food_type
    global second_food_type
    product_name_label = ctk.CTkLabel(add_item, text="Product Name", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    product_name_label.grid(row = 1, column = 0)
    product_name = ctk.CTkEntry(add_item, width=369, height=45, corner_radius=20, state='normal')
    product_name.grid(row=2, column=0, pady=15, padx=25, sticky='w')

    price_label = ctk.CTkLabel(add_item, text="Price", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    price_label.grid(row = 3, column = 0)
    price_var = ctk.CTkEntry(add_item, placeholder_text="0.00", width=369, height=55, corner_radius=20, state='normal')
    price_var.grid(row=4, column=0, pady=15, padx=25, sticky='w')

    selling_food_estab_label = ctk.CTkLabel(add_item, text="Selling Food Establishment", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    selling_food_estab_label.grid(row = 5, column = 0)
    selling_food_estab = ctk.CTkEntry(add_item, width=369, height=45, corner_radius=20, state='normal')
    selling_food_estab.grid(row=6, column=0, pady=15, padx=25, sticky='w')

    food_type_label = ctk.CTkLabel(add_item, text="Food Type", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    food_type_label.grid(row = 7, column = 0)
    food_type = ctk.CTkEntry(add_item, width=369, height=45, corner_radius=20, state='normal')
    food_type.grid(row=8, column=0, pady=15, padx=25, sticky='w')

    second_food_type_label = ctk.CTkLabel(add_item, text="Second Food Type (Optional)", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    second_food_type_label.grid(row = 9, column = 0)
    second_food_type = ctk.CTkEntry(add_item, width=369, height=45, corner_radius=20, state='normal')
    second_food_type.grid(row=10, column=0, pady=15, padx=25, sticky='w')

    submit_button = ctk.CTkButton(add_item, text='Submit', text_color='#FFFFFF', font=('Helvetica', 16), width=100, height=52, corner_radius=10, fg_color="#b89e97", command=lambda: get_values_item())
    submit_button.grid(row=11, column=0, pady=15, padx=24, sticky='w')

    reset_button = ctk.CTkButton(add_item, text='Reset', text_color='#FFFFFF', font=('Helvetica', 16), width=100, height=52, corner_radius=10, fg_color="#FF3E3E", command=lambda: reset_form_fields_items())
    reset_button.grid(row=11, column=0, pady=15, padx=24, sticky='e')



def start_gui():
    add_itemstore_screen()
    app.mainloop()


start_gui()