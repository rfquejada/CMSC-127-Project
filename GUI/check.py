import customtkinter as ctk
import sys
import mariadb
from tkinter import messagebox

try:
    conn = mariadb.connect(
        user="root",
        password="mustbeOkay12",
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

def check_productid_in_item_exists(cur, productid):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM food_item WHERE productid = ?", (productid,))
    count = cur.fetchone()[0]
    return count > 0 # 0 if not existing & 1 if it exists

def check_contact_exists(cur, contactnum):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM estab_contact WHERE contactnum = ?", (contactnum,))
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
    cur.execute("SELECT estabid FROM food_estab WHERE estabname=?", (estabname,))
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

def search_food_product_id_by_name_estabid(cur, estabid, itemname):
    cur.execute("SELECT productid FROM food_item WHERE estabid=? and itemname=?", (estabid, itemname,))
    result = cur.fetchone()
    
    if result is None:
        print("Item not found.")
        return
    
    return result[0]


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
    new_estab_name.configure(state='normal')
    new_estab_address.configure(state='normal')
    contact_number.configure(state='normal')
    submit_buttonc.configure(state='normal')
    submit_buttone.configure(state='normal')
    reset_buttonc.configure(state='normal')
    estab_name_search.configure(state='disabled')
    messagebox.showinfo("Match Found!", "Found a Match: Input new details in the right area.")

def handleSearchItemEstabDelete():
    estabname = delete_estab_name_search.get() 

    if not estabname:
        print("Invalid input")
        return
    estabid = search_food_establishment_id(cur, estabname)
    if(check_estabid_exists(cur, estabid)== 0):
        messagebox.showerror("Input Error", "No Food Establishment found.")
        return
    submit_button_delete_item_estab.configure(state='disabled')
    delete_estab_name_search.configure(state='disabled')
    delete_item_name_search.configure(state='normal')
    food_item_single_delete_button.configure(state='normal') 
    item_multi_contact_delete_button.configure(state='normal')
    reset_item_single_delete_button.configure(state='normal')
    messagebox.showinfo("Match Found!", "Found a Match: Input new details in the right area.")

def handleResetSearchItemEstabDelete():
    submit_button_delete_item_estab.configure(state='normal')
    delete_estab_name_search.configure(state='normal')
    delete_item_name_search.configure(state='normal')
    delete_estab_name_search.delete(0,'end')
    delete_item_name_search.delete(0,'end')
    food_item_single_delete_button.configure(state='disabled') 
    item_multi_contact_delete_button.configure(state='disabled')
    reset_item_single_delete_button.configure(state='disabled')
    delete_item_name_search.configure(state='disabled')

def handleSearchItemEstab():
    estabname = e_estab_name_search.get() 
    itemname = item_name_search.get()

    if not estabname or not itemname:
        print("Invalid input")
        return
    estabid = search_food_establishment_id(cur, estabname)
    if(check_estabid_exists(cur, estabid)== 0):
        messagebox.showerror("Input Error", "No Food Establishment found.")
        return
    productid = search_food_product_id_by_name_estabid(cur, estabid, itemname)
    if check_productid_in_item_exists(cur,productid) == 0:
        messagebox.showerror("Input Error", "No Product like that in the inventory of this Food Establishment.")
        return
    submit_button_search_item_estab.configure(state='disabled')
    e_estab_name_search.configure(state='disabled')
    item_name_search.configure(state='disabled')
    new_item_name.configure(state='normal')
    submit_button_new_info_item.configure(state='normal')
    new_item_price.configure(state='normal')
    food_type.configure(state='normal')
    submit_button_food_type.configure(state='normal')
    reset_button_food_type.configure(state='normal')
    messagebox.showinfo("Match Found!", "Found a Match: Input new details in the right area.")

def handleResetSearchItemEstab():
    submit_button_search_item_estab.configure(state='normal')
    submit_button_new_info_item.configure(state='disabled')
    e_estab_name_search.configure(state='normal')
    item_name_search.configure(state='normal')
    e_estab_name_search.delete(0,'end')
    item_name_search.delete(0,'end')
    new_item_name.configure(state='normal')
    new_item_price.configure(state='normal')
    new_item_name.delete(0,'end')
    new_item_price.delete(0,'end')
    new_item_name.configure(state='disabled')
    new_item_price.configure(state='disabled')
    food_type.configure(state='normal')
    food_type.delete(0,'end')
    food_type.configure(state='disabled')
    submit_button_food_type.configure(state='disabled')
    reset_button_food_type.configure(state='disabled')


def reset_form_fields_estab():
    global estab_name_search
    global new_estab_name
    global new_estab_address
    global contact_num
    estab_name_search.configure(state='normal')
    new_estab_name.configure(state='normal')
    new_estab_address.configure(state='normal')
    contact_number.configure(state='normal')
    estab_name_search.delete(0,'end')
    new_estab_name.delete(0, 'end')
    new_estab_address.delete(0, 'end')
    contact_number.delete(0,'end')
    new_estab_name.configure(state='disabled')
    new_estab_address.configure(state='disabled')
    contact_number.configure(state='disabled')
    messagebox.showinfo("Search Ready","Can Search New Establishment")

def reset_form_fields_contact():
    global contact_num
    contact_number.configure(state='normal')
    submit_buttonc.configure(state='normal')
    contact_number.delete(0,'end')
    messagebox.showinfo("Input Ready","Can Insert New Establishment Contact Number")

def handleEstabUpdate():
    global estab_id
    if estab_id == None:
        messagebox.showerror("Missing ID", "No matching establishment! Search product with the search module first.")
        return
    
    global new_estab_address
    global new_estab_name
    global submit_buttone
    global submit_buttonc
    global reset_buttonc
    if new_estab_address.get() == None or new_estab_name.get() == None:
        messagebox.showerror("Invalid Input", "Please fill up the fields.")
        return
    
    name = str(new_estab_name.get())
    address = str(new_estab_address.get())
    if len(name)>50 or len(address)>50:
        messagebox.showerror("Invalid Input", "Either name or address is too long")
        return
    
    cur.execute('Update food_estab set estabname = ?, branch_address = ? where estabid = ?', (name, address, estab_id))
    contactnum = contact_number.get()
    if contactnum != None and contactnum.isdigit() == True and len(contactnum) == 11:
        cur.execute("SELECT contactnum FROM estab_contact WHERE estabid=?", (estab_id,))
        cn = cur.fetchall()
        
        # Extract product IDs from tuples
        cn = [conta[0] for conta in cn]
        
        for conta in cn:
            if conta == contactnum:
                messagebox.showerror("Invalid Input", "Contact Number Already Existing")
                return
        cur.execute("INSERT INTO estab_contact(estabid, contactnum) VALUES (?, ?)", (estab_id, contactnum))
        messagebox.showinfo("Update Complete!", "Details Updated For ALL Details!")
        return
    else:    
        new_estab_name.configure(state='disabled')
        new_estab_address.configure(state='disabled')
        contact_number.configure(state='disabled')
        submit_buttonc.configure(state='disabled')
        submit_buttone.configure(state='disabled')
        reset_buttonc.configure(state='disabled')
        messagebox.showinfo("Update Complete!", "Details Updated For Food Establishment Name and Branch Address!")
        return
    

def handleEstabContactUpdate():
    global estab_id, contact_number, cur, conn
    if estab_id == None:
        messagebox.showerror("Missing ID", "No matching establishment!")
        return
    
    global contact_number
    if contact_number.get() == None:
        messagebox.showerror("Invalid Input", "Please fill up the fields.")
        return
    
    contactnum =  contact_number.get()
    if contactnum.isdigit()==True and len(contactnum) == 11:
        cur.execute("SELECT contactnum FROM estab_contact WHERE estabid=?", (estab_id,))
        cn = cur.fetchall()
        
        # Extract product IDs from tuples
        cn = [conta[0] for conta in cn]
        
        for conta in cn:
            if conta == contactnum:
                messagebox.showerror("Invalid Input", "Contact Number Already Existing")
                return
        cur.execute("INSERT INTO estab_contact(estabid, contactnum) VALUES (?, ?)", (estab_id, contactnum))
        conn.commit()
        contact_number.configure(state='disabled')
        submit_buttonc.configure(state='disabled')
        messagebox.showinfo("Update Complete!", "Details Updated!")
    else:
        messagebox.showerror("Invalid Input", "Enter 11 Digit Number")
        return
    
def handleItemUpdate():
    estabname = e_estab_name_search.get() 
    itemname = item_name_search.get()
    estabid = search_food_establishment_id(cur, estabname)
    productid = search_food_product_id_by_name_estabid(cur, estabid, itemname)
    name = new_item_name.get()
    price = new_item_price.get()
    foodtype = food_type.get()
    if not name or not price:
        messagebox.showerror("Invalid Input", "Enter A Valid Input")
        return
    if len(name) <= 50 and price.isdigit() == True:
        price = float(price) 
        cur.execute('Update food_item set itemname = ?, price = ? where productid = ?', (name, price, productid))
        conn.commit()
        new_item_name.configure(state='disabled')
        new_item_price.configure(state='disabled')
        submit_button_new_info_item.configure(state='disabled')
        food_type.configure(state='disabled')
        submit_button_food_type.configure(state='disabled')
        reset_button_food_type.configure(state='disabled')
        if foodtype and len(foodtype) <= 20:
            cur.execute("SELECT foodtype FROM food_type WHERE productid=?", (productid,))
            ft = cur.fetchall()
            
            # Extract product IDs from tuples
            ft = [food_types[0] for food_types in ft]
            
            for food_types in ft:
                if food_types == foodtype:
                    messagebox.showerror("Invalid Input", "Food Type Already Existing")
                    return
            cur.execute("INSERT INTO food_type(productid, foodtype) VALUES (?, ?)", (productid, foodtype))
            conn.commit()
            messagebox.showinfo("Update Complete!", "Details Updated For Product Name, Price, and Food Type!")
            return
        else:
            messagebox.showinfo("Update Complete!", "Details Updated For Product Name And Price!")
            return
    else:
        messagebox.showerror("Invalid Input", "Name is too long or Price is not a digit")
        return

def handleFoodTypeUpdate():
    estabname = e_estab_name_search.get() 
    itemname = item_name_search.get()
    estabid = search_food_establishment_id(cur, estabname)
    productid = search_food_product_id_by_name_estabid(cur, estabid, itemname)
    foodtype = food_type.get()
    if len(foodtype) > 20:
        messagebox.showerror("Invalid Input", "Name is too long")
        return
    if not foodtype:
        messagebox.showerror("Invalid Input", "Enter A Food Type")

    cur.execute("SELECT foodtype FROM food_type WHERE productid=?", (productid,))
    ft = cur.fetchall()
    
    # Extract product IDs from tuples
    ft = [food_types[0] for food_types in ft]
    
    for food_types in ft:
        if food_types == foodtype:
            messagebox.showerror("Invalid Input", "Food Type Already Existing")
            return

    cur.execute("INSERT INTO food_type(productid, foodtype) VALUES (?, ?)", (productid, foodtype))
    conn.commit()
    food_type.configure(state='disabled')
    submit_button_food_type.configure(state='disabled')
    messagebox.showinfo("Update Complete!", "Details Updated!")
    return

def reset_food_type():
    food_type.configure(state='normal')
    submit_button_food_type.configure(state='normal')
    food_type.delete(0,'end')
    messagebox.showinfo("Input Ready","Can Insert New Food Type")

def handleSearchDelEstab():
    estabname = estab_name_delete.get()
    estabid = search_food_establishment_id(cur, estabname)
    if(check_estabid_exists(cur, estabid)== 0):
        messagebox.showerror("Input Error", "No Food Establishment found.")
        return
    messagebox.showinfo("Match Found!", "Found a Match: Input details needed to remove the establishment.")
    estab_name_delete.configure(state='disabled')
    estab_single_contact_delete.configure(state='normal')
    estab_multi_contact_delete_button.configure(state='normal')
    estab_single_contact_delete_button.configure(state='normal')
    estab_delete_real_button.configure(state='normal')
    reset_single_contact_delete_button.configure(state='normal')
    estab_delete_button.configure(state='disabled')

def handleResetDelEstab():
    estab_single_contact_delete.configure(state='normal')
    estab_name_delete.configure(state='normal')
    estab_name_delete.delete(0,'end')
    estab_single_contact_delete.delete(0,'end')
    estab_single_contact_delete.configure(state='disabled')
    estab_single_contact_delete_button.configure(state='disabled')
    estab_multi_contact_delete_button.configure(state='disabled')
    estab_delete_real_button.configure(state='disabled')
    reset_single_contact_delete_button.configure(state='disabled')
    estab_delete_button.configure(state='normal')

def handleResetSinCon():
    estab_single_contact_delete.configure(state='normal')
    estab_single_contact_delete.delete(0,'end')
    estab_single_contact_delete_button.configure(state='normal')
    messagebox.showinfo("Input Ready","Can Insert Contact Number to be Deleted")

def handleSinDelCon():
    estabname = estab_name_delete.get()
    estabid = search_food_establishment_id(cur, estabname)
    contactnumIntForm = estab_single_contact_delete.get()
    print(check_contact_exists(cur,contactnumIntForm))
    if check_contact_exists(cur,contactnumIntForm) == 0:
        messagebox.showerror("Invalid Input", "There is no contact number in the establishment you entered")
        return

    if contactnumIntForm.isdigit()==True and len(contactnumIntForm) == 11 and check_estabid_exists(cur,estabid) == 1 and check_estabid_in_contact_exists(cur,estabid) == 1:
        cur.execute("DELETE FROM estab_contact WHERE estabid=? and contactnum=?",(estabid, contactnumIntForm))
        conn.commit()
        messagebox.showinfo("Deletion Complete!", "Details Updated!")
        estab_single_contact_delete.configure(state='disabled')
        estab_single_contact_delete_button.configure(state='disabled')
        print("Successfully Deleted\n")
    else:
        messagebox.showerror("Invalid Input", "There seems to be an error on your input")
        print("There is no existing food establishment id with the same establishment id in contacts\n")
        return

def handleMultDelCon():
    estabname = estab_name_delete.get()
    estabid = search_food_establishment_id(cur, estabname)
    if check_estabid_in_contact_exists(cur,estabid) == 0:
        messagebox.showinfo("No More Contact Number Existing!", "Now Valid to Delete The Establishment(Optional)")
        return

    if(check_estabid_exists(cur,estabid) == 1 and check_estabid_in_contact_exists(cur,estabid) == 1):
        cur.execute("DELETE FROM estab_contact WHERE estabid=?",(estabid,))
        conn.commit()
        messagebox.showinfo("Deletion Complete!", "Now Valid to Delete The Establishment(Optional)")
        estab_multi_contact_delete_button.configure(state='disabled')
        estab_single_contact_delete.configure(state='disabled')
        estab_single_contact_delete_button.configure(state='disabled')
        reset_single_contact_delete_button.configure(state='disabled')
        print("Successfully Deleted\n")
    else:
        messagebox.showerror("Invalid Input", "There is no existing food establishment id with the same establishment id in contacts")
        print("There is no existing food establishment id with the same establishment id in contacts\n")
        return

def handleDelEstabReal():
    estabname = estab_name_delete.get()
    estabid = search_food_establishment_id(cur, estabname)
    if(check_estabid_exists(cur, estabid)== 0):
        messagebox.showerror("Invalid Input", "Food establishment is not existing")
        return
    cur.execute("SELECT productid FROM food_item WHERE estabid=?", (estabid,))
    product_ids = cur.fetchall()
    
    # Extract product IDs from tuples
    product_ids = [product_id[0] for product_id in product_ids]
    
    for product_id in product_ids:
        cur.execute("DELETE FROM food_type WHERE productid=?", (product_id,))
    
    # Delete all related entries in food_item table
    cur.execute("DELETE FROM food_item WHERE estabid=?", (estabid,))

    if(check_estabid_in_contact_exists(cur, estabid) == 0):  # contact number does not exist
        # Rules to delete a food establishment
        # Remove food_type because it uses productid as a FK
        # Remove food_item because it uses estabid as a FK
        # Remove estab_contact because it uses estabid as a FK, which is in a different function
        # After all that, you can now remove the establishment
        #cur.execute("DELETE FROM food_type WHERE productid=?", (productid,))  # needs to be deleted since estabid is a FK in this table
        #cur.execute("DELETE FROM food_item WHERE estabid=?", (estabid,))  # needs to be deleted since estabid is a FK in this table
        cur.execute("DELETE FROM food_estab WHERE estabid=?", (estabid,))
        conn.commit()
        estab_multi_contact_delete_button.configure(state='disabled')
        estab_single_contact_delete.configure(state='disabled')
        estab_single_contact_delete_button.configure(state='disabled')
        estab_delete_real_button.configure(state='disabled')
        reset_single_contact_delete_button.configure(state='disabled')
        messagebox.showinfo("Deletion Complete!", "Food Establishment is removed")
        print("Successfully Deleted\n")
        return
    else:
        messagebox.showerror("Be Careful", "Delete contact number, food item ,and food type related to this establishment")
        print("Delete contact number, food item ,and food type related to this establishment\n")
        return

def handleSinDelItem():
    estabname = delete_estab_name_search.get()
    estabid = search_food_establishment_id(cur, estabname)
    itemname = delete_item_name_search.get()
    productid = search_food_product_id_by_name_estabid(cur, estabid, itemname)
    if check_productid_in_item_exists(cur, productid) == 0:
        messagebox.showerror("Invalid Input", "There is food item like that in this establishment")
        return
    if check_estabid_exists_in_item(cur,estabid) == 1 and check_productid_in_item_exists(cur,productid) == 1:
        cur.execute("DELETE FROM food_type WHERE productid=?", (productid,))
        cur.execute("DELETE FROM food_item WHERE estabid=? and productid=?", (estabid,productid,))
        conn.commit()
        delete_item_name_search.configure(state='disabled')
        food_item_single_delete_button.configure(state='disabled')
        messagebox.showinfo("Deletion Complete!", "Details Updated!")
        return

def handleResetSinDelItem():
    delete_item_name_search.configure(state='normal')
    delete_item_name_search.delete(0,'end')
    food_item_single_delete_button.configure(state='normal')
    messagebox.showinfo("Input Ready","Can Input A new Food Item to be Deleted")

def handleMultDelItem():
    estabname = delete_estab_name_search.get()
    estabid = search_food_establishment_id(cur, estabname)
    if check_estabid_exists_in_item(cur,estabid) == 1:
        cur.execute("SELECT productid FROM food_item WHERE estabid=?", (estabid,))
        product_ids = cur.fetchall()
        
        # Extract product IDs from tuples
        product_ids = [product_id[0] for product_id in product_ids]
        
        for product_id in product_ids:
            cur.execute("DELETE FROM food_type WHERE productid=?", (product_id,))
        
        # Delete all related entries in food_item table
        cur.execute("DELETE FROM food_item WHERE estabid=?", (estabid,))
        conn.commit()
        delete_item_name_search.configure(state='disabled')
        food_item_single_delete_button.configure(state='disabled')
        item_multi_contact_delete_button.configure(state='disabled')
        reset_item_single_delete_button.configure(state='disabaled')
        messagebox.showinfo("Deletion Complete!", "Valid for Deletion of Food Establishment!")
        return

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
    edit_tab.add("Delete Establishment")
    edit_tab.add("Delete Food Item")

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

    reset_button = ctk.CTkButton(search_estab_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: reset_form_fields_estab())
    reset_button.grid(row=3, column=0, pady=25, padx=15, sticky='se')

    #Edit Estab Frame
    global estab_id
    edit_estab_frame = ctk.CTkFrame(edit_tab.tab("Establishment"), width=450, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    edit_estab_frame.grid(row=0, column=1, padx = 30, pady= 15, sticky='ne')
    edit_estab_frame.grid_propagate(0)

    label = ctk.CTkLabel(edit_estab_frame, text='Establishment', fg_color='transparent', text_color='#000000', font=('Helvetica', 32))
    label.grid(row=0, column=0, pady=15, padx=10, sticky='nw')

    global new_estab_name
    global new_estab_address
    global contact_number
    global submit_buttone
    global submit_buttonc
    global reset_buttonc
    new_estab_name_label = ctk.CTkLabel(edit_estab_frame, text="New Establishment Name", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_estab_name_label.grid(row = 1, column = 0, pady=15, padx=15, sticky='w')

    new_estab_name = ctk.CTkEntry(edit_estab_frame,placeholder_text="Establishment name..." ,width=369, height=55, corner_radius=20, state='disabled')
    new_estab_name.grid(row=2, column=0, pady=15, padx=25, sticky='w')

    new_estab_address_label = ctk.CTkLabel(edit_estab_frame, text="New Branch Address", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_estab_address_label.grid(row = 3, column = 0, padx=15, sticky='w')

    new_estab_address = ctk.CTkEntry(edit_estab_frame,width=369, placeholder_text="Branch address...", height=55, corner_radius=20, state='disabled')
    new_estab_address.grid(row=4, column=0, pady=15, padx=25, sticky='w')

    submit_buttone = ctk.CTkButton(edit_estab_frame, text='Submit', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleEstabUpdate(), state='disabled')
    submit_buttone.grid(row=5, column=0, pady=15, padx=25, sticky='w')

    contact_number_label = ctk.CTkLabel(edit_estab_frame, text="Add Contact Number (Optional)", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    contact_number_label.grid(row = 6, column = 0, padx=15, sticky='w')

    contact_number = ctk.CTkEntry(edit_estab_frame,width=369, placeholder_text="00000000000", height=55, corner_radius=20, state='disabled')
    contact_number.grid(row=7, column=0, pady=15, padx=25, sticky='w')

    submit_buttonc = ctk.CTkButton(edit_estab_frame, text='Submit', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleEstabContactUpdate(), state='disabled')
    submit_buttonc.grid(row=8, column=0, pady=15, padx=25, sticky='w')

    reset_buttonc = ctk.CTkButton(edit_estab_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: reset_form_fields_contact(), state='disabled')
    reset_buttonc.grid(row=8, column=0, pady=25, padx=15, sticky='e')

    #Search Item Frame
    search_item_frame = ctk.CTkFrame(edit_tab.tab("Item"), width=350, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    search_item_frame.grid(row=0, column=0, padx = 30, pady= 15, sticky='nw')
    search_item_frame.grid_propagate(0)

    search_label = ctk.CTkLabel(search_item_frame, text='Search', fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    search_label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    item_name_label = ctk.CTkLabel(search_item_frame, text='Item Name', fg_color='transparent', text_color='#000000', font=('Helvetica', 16))
    item_name_label.grid(row=1, column=0, pady=15, padx=25, sticky='w')
    
    global item_name_search
    item_name_search = ctk.CTkEntry(search_item_frame, placeholder_text="Insert Item Name Here..." ,width=300, height=35, corner_radius=20, state='normal')
    item_name_search.grid(row=2, column=0, pady=1, padx=25, sticky='w')

    estab_name_label = ctk.CTkLabel(search_item_frame, text='Establishment Name', fg_color='transparent', text_color='#000000', font=('Helvetica', 16))
    estab_name_label.grid(row=3, column=0, pady=15, padx=25, sticky='w')

    global e_estab_name_search
    e_estab_name_search = ctk.CTkEntry(search_item_frame, placeholder_text="Insert Establishment Name Here..." ,width=300, height=35, corner_radius=20, state='normal')
    e_estab_name_search.grid(row=4, column=0, pady=1, padx=25, sticky='w')

    global submit_button_search_item_estab
    submit_button_search_item_estab = ctk.CTkButton(search_item_frame, text='Search', width=64, height=41, command=lambda: handleSearchItemEstab(), state='normal')
    submit_button_search_item_estab.grid(row=5, column=0, pady=25, padx=25, sticky='sw')

    reset_estab_delete_button = ctk.CTkButton(search_item_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: handleResetSearchItemEstab())
    reset_estab_delete_button.grid(row=5, column=0, pady=25, padx=15, sticky='se')

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

    new_item_name = ctk.CTkEntry(edit_item_frame,placeholder_text="Item name..." ,width=369, height=55, corner_radius=20, state='disabled')
    new_item_name.grid(row=2, column=0, pady=5, padx=25, sticky='w')

    new_item_price_label = ctk.CTkLabel(edit_item_frame, text="New Price", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    new_item_price_label.grid(row = 3, column = 0, pady=15, padx=15, sticky='w')

    new_item_price = ctk.CTkEntry(edit_item_frame,width=369, height=55, placeholder_text='Price...', corner_radius=20, state='disabled')
    new_item_price.grid(row=4, column=0, pady=5, padx=25, sticky='w')

    global submit_button_new_info_item
    submit_button_new_info_item = ctk.CTkButton(edit_item_frame, text='Update', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleItemUpdate(), state='disabled')
    submit_button_new_info_item.grid(row=5, column=0, pady=15, padx=25, sticky='w')

    # for food type
    food_type_label = ctk.CTkLabel(edit_item_frame, text="Add Food Type (Optional)", fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    food_type_label.grid(row = 6, column = 0, padx=15, sticky='w')

    global food_type
    food_type = ctk.CTkEntry(edit_item_frame,width=369, height=55, corner_radius=20, state='disabled')
    food_type.grid(row=7, column=0, pady=15, padx=25, sticky='w')

    global submit_button_food_type
    submit_button_food_type = ctk.CTkButton(edit_item_frame, text='Submit', text_color='#FFFFFF', font=('Helvetica', 16), width=128, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleFoodTypeUpdate(), state='disabled')
    submit_button_food_type.grid(row=8, column=0, pady=15, padx=25, sticky='w')

    global reset_button_food_type
    reset_button_food_type = ctk.CTkButton(edit_item_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: reset_food_type(), state='disabled')
    reset_button_food_type.grid(row=8, column=0, pady=25, padx=15, sticky='e')

    # Delete Establishment Frame
    delete_estab_frame = ctk.CTkFrame(edit_tab.tab("Delete Establishment"), width=350, height=300, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    delete_estab_frame.grid(row=0, column=0, padx = 30, pady= 15, sticky='nw')
    delete_estab_frame.grid_propagate(0)

    delete_estab_title = ctk.CTkLabel(delete_estab_frame, text="Search", text_color="#000000", font=("Helvetica", 28))
    delete_estab_title.grid(row=0, column=0, padx=10, pady=15, sticky='w')
    delete_estab_label = ctk.CTkLabel(delete_estab_frame, text="Enter the name of the Establishment:", text_color="#000000", font=("Helvetica", 14))
    delete_estab_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    global estab_name_delete
    global estab_delete_button
    estab_name_delete = ctk.CTkEntry(delete_estab_frame, placeholder_text="<Establishment Name> - <General Location>" ,width=280, height=40, corner_radius=10, border_width=1)
    estab_name_delete.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    estab_delete_button = ctk.CTkButton(delete_estab_frame, text="Search", text_color="#FFFFFF", font=("Helvetica", 20), width=64, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleSearchDelEstab(), state='normal')
    estab_delete_button.grid(row=3, column=0, pady=25, padx=25, sticky='sw')

    reset_estab_delete_button = ctk.CTkButton(delete_estab_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: handleResetDelEstab())
    reset_estab_delete_button.grid(row=3, column=0, pady=25, padx=15, sticky='se')

    # Delete Item Frame
    delete_estab_frame = ctk.CTkFrame(edit_tab.tab("Delete Establishment"), width=450, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    delete_estab_frame.grid(row=0, column=1, padx = 30, pady= 15, sticky='nw')
    delete_estab_frame.grid_propagate(0)

    #Single Deletion
    delete_estab_title = ctk.CTkLabel(delete_estab_frame, text="Conditions", text_color="#000000", font=("Helvetica", 28))
    delete_estab_title.grid(row=0, column=0, padx=10, pady=15, sticky='w')
    delete_estab_label = ctk.CTkLabel(delete_estab_frame, text="Delete A Single Contact Number (Optional)", text_color="#000000", font=("Helvetica", 14))
    delete_estab_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    global estab_single_contact_delete
    global estab_single_contact_delete_button
    global reset_single_contact_delete_button
    estab_single_contact_delete = ctk.CTkEntry(delete_estab_frame, placeholder_text="00000000000" ,width=250, height=40, corner_radius=10, border_width=1, state='disabled')
    estab_single_contact_delete.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    
    estab_single_contact_delete_button = ctk.CTkButton(delete_estab_frame, text="Delete", text_color="#FFFFFF", font=("Helvetica", 20), width=64, height=41, corner_radius=10, fg_color="#FF0000",command=lambda: handleSinDelCon(), state='disabled')
    estab_single_contact_delete_button.grid(row=3, column=0, padx=10, pady=15, sticky='w')

    reset_single_contact_delete_button = ctk.CTkButton(delete_estab_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#1098F7", command=lambda: handleResetSinCon(), state='disabled')
    reset_single_contact_delete_button.grid(row=3, column=0, pady=25, padx=15, sticky='se')

    #For delete all contacts
    delete_estab_multi_label = ctk.CTkLabel(delete_estab_frame, text="Delete All Contact Number (Recommended): ", text_color="#000000", font=("Helvetica", 16))
    delete_estab_multi_label.grid(row=4, column=0, padx=4, pady=5, sticky='w')

    global estab_multi_contact_delete_button
    estab_multi_contact_delete_button = ctk.CTkButton(delete_estab_frame, text="Delete", text_color="#FFFFFF", font=("Helvetica", 20), width=40, height=41, corner_radius=10, fg_color="#FF0000", command=lambda: handleMultDelCon(), state='disabled')
    estab_multi_contact_delete_button.grid(row=4, column=1, padx=4, pady=15, sticky='w')


    #Deletion of food establishment
    estab_delete_real_label = ctk.CTkLabel(delete_estab_frame, text="Delete Food Establishment: ", text_color="#000000", font=("Helvetica", 16))
    estab_delete_real_label.grid(row=6, column=0, padx=4, pady=5, sticky='w')

    global estab_delete_real_button
    estab_delete_real_button = ctk.CTkButton(delete_estab_frame, text="Delete", text_color="#FFFFFF", font=("Helvetica", 20), width=40, height=41, corner_radius=10, fg_color="#FF0000", command=lambda: handleDelEstabReal(), state='disabled')
    estab_delete_real_button.grid(row=6, column=1, padx=4, pady=15, sticky='w')

    # Delete Food Item Frame
    delete_item_frame = ctk.CTkFrame(edit_tab.tab("Delete Food Item"), width=350, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    delete_item_frame.grid(row=0, column=0, padx = 30, pady= 15, sticky='nw')
    delete_item_frame.grid_propagate(0)

    search_label = ctk.CTkLabel(delete_item_frame, text='Search', fg_color='transparent', text_color='#000000', font=('Helvetica', 24))
    search_label.grid(row=0, column=0, pady=15, padx=25, sticky='nw')

    estab_name_label = ctk.CTkLabel(delete_item_frame, text='Establishment Name', fg_color='transparent', text_color='#000000', font=('Helvetica', 16))
    estab_name_label.grid(row=1, column=0, pady=15, padx=25, sticky='w')

    global delete_estab_name_search
    delete_estab_name_search = ctk.CTkEntry(delete_item_frame, placeholder_text="Insert Establishment Name Here..." ,width=300, height=35, corner_radius=20, state='normal')
    delete_estab_name_search.grid(row=2, column=0, pady=1, padx=25, sticky='w')

    global submit_button_delete_item_estab
    submit_button_delete_item_estab = ctk.CTkButton(delete_item_frame, text='Search', width=64, height=41, command=lambda: handleSearchItemEstabDelete(), state='normal')
    submit_button_delete_item_estab.grid(row=3, column=0, pady=25, padx=25, sticky='sw')

    reset_item_delete_button = ctk.CTkButton(delete_item_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=64, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: handleResetSearchItemEstabDelete())
    reset_item_delete_button.grid(row=3, column=0, pady=25, padx=15, sticky='se')

    # Delete Item Frame
    delete_item_frame = ctk.CTkFrame(edit_tab.tab("Delete Food Item"), width=450, height=600, corner_radius=20, border_width=1, fg_color="#FFFFFF")
    delete_item_frame.grid(row=0, column=1, padx = 30, pady= 15, sticky='nw')
    delete_item_frame.grid_propagate(0)

    #Single Deletion
    delete_item_title = ctk.CTkLabel(delete_item_frame, text="Conditions", text_color="#000000", font=("Helvetica", 28))
    delete_item_title.grid(row=0, column=0, padx=10, pady=15, sticky='w')
    
    delete_item_label = ctk.CTkLabel(delete_item_frame, text="Delete A Single Food Item (Optional): ", text_color="#000000", font=("Helvetica", 16))
    delete_item_label.grid(row=1, column=0, padx=15, pady=15, sticky='w')

    global delete_item_name_search
    delete_item_name_search = ctk.CTkEntry(delete_item_frame, placeholder_text="Insert Item Name Here..." ,width=300, height=35, corner_radius=20, state='disabled')
    delete_item_name_search.grid(row=2, column=0, pady=15, padx=15, sticky='w')
    
    global food_item_single_delete_button
    food_item_single_delete_button = ctk.CTkButton(delete_item_frame, text="Delete", text_color="#FFFFFF", font=("Helvetica", 20), width=40, height=41, corner_radius=10, fg_color="#FF0000",command=lambda: handleSinDelItem(), state='disabled')
    food_item_single_delete_button.grid(row=3, column=0, padx=8, pady=15, sticky='w')#function

    global reset_item_single_delete_button
    reset_item_single_delete_button = ctk.CTkButton(delete_item_frame, text='reset', text_color='#FFFFFF', font=('Helvetica', 16), width=40, height=41, corner_radius=10, fg_color="#FF3E3E", command=lambda: handleResetSinDelItem(), state='disabled')
    reset_item_single_delete_button.grid(row=3, column=0, pady=25, padx=15, sticky='se')

    #For delete all food item in estab
    delete_item_multi_label = ctk.CTkLabel(delete_item_frame, text="Delete All Food Item (Recommended): ", text_color="#000000", font=("Helvetica", 16))
    delete_item_multi_label.grid(row=4, column=0, padx=4, pady=5, sticky='w')

    global item_multi_contact_delete_button
    item_multi_contact_delete_button = ctk.CTkButton(delete_item_frame, text="Delete", text_color="#FFFFFF", font=("Helvetica", 20), width=40, height=41, corner_radius=10, fg_color="#FF0000", command=lambda: handleMultDelItem(), state='disabled')
    item_multi_contact_delete_button.grid(row=4, column=1, padx=4, pady=15, sticky='w')


# Run the application
def clear_window():
    for widget in app.winfo_children():
        widget.destroy()
        conn.close()

def start_gui():
    edit_itemstore_screen()
    app.mainloop()

start_gui()