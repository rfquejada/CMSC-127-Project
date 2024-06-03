import mariadb
import sys
from tabulate import tabulate

def print_menu_search():
    print("[1] Search for a Food Establishment")
    print("[2] Search for a Food Establishment Contact Number")
    print("[0] Exit\n")
    

    SearchChoice = input("\nEnter choice: ")
    return SearchChoice

def NewTransaction():
    print("#-------------------------------------------------------------#")
    print("[1] Add Food Establishment")
    print("[2] Add Food Establishment Contact Number")
    print("[3] Update/Edit Food Establishment")
    print("[4] Delete Food Establishment")
    print("[5] Delete All Contacts Related To A Food Establishment")
    print("[6] Search Food Establishment")
    print("[7] Search Food Establishment Contacts")
    print("[8] Print All Details About Food Establishment")
    print("[9] Print All Details About Food Establishment Contacts")
    print("[0] Back to Main Menu")
    print("#-------------------------------------------------------------#")

    ChoiceForTransaction = input("\nWhat you want to do?\nEnter choice: ")
    return ChoiceForTransaction

def print_option_delete():
    print("#-------------------------------------------------------------#")
    print("[1] Delete A Food Establishment")
    print("[2] Delete All Contact Number Related To A Food Establishment")
    print("[3] Delete Single A Contact Number Related To A Food Establishment")
    print("[0] Return to Food Establishment Options\n")
    print("#-------------------------------------------------------------#")

    ChoiceForOptionDelete = input("\nEnter choice: ")
    return ChoiceForOptionDelete

def get_int_input(prompt):
    #helper function to get integer input safely.
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

# Checks if estabid is existing in food establishment table
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

def check_estabid_contactnum_in_contact_exists(cur, estabid, contactnum):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM estab_contact WHERE estabid = ? and contactnum = ?", (estabid, contactnum,))
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

# Adds single food establishment
def add_food_establishment(cur,conn):
    estabname = (input("Enter Establishment Name <Establishment Name> - <General Location>: "))
    branch_address = (input("Enter Branch Address: "))
    if(len(estabname) > 50 or len(branch_address) > 50):
        print("There has been a problem on one of the attribute inputted")
        return
    else:
        print("Food Establishment Details Added To The Food Establishment Table\n")
        #adds the given details about food establishment to the food establishment table
        cur.execute("INSERT INTO food_estab(estabname, branch_address) VALUES (?, ?)",(estabname, branch_address))
        conn.commit()
        return

# Adds single contact
def add_food_establishment_contact(cur,conn):
    estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
    estabid = search_food_establishment_id(cur, estabname_input)
    if(check_estabid_exists(cur, estabid) == 0):
        return
    contactnumIntForm = str(get_int_input("Enter Contact Number: "))
    if not check_estabid_contactnum_in_contact_exists(cur, estabid, contactnumIntForm):
        if(len(contactnumIntForm) == 11):
            #adds the given details about food establishment contact number to the food establishment contact number table
            cur.execute("INSERT INTO estab_contact(estabid, contactnum) VALUES (?, ?)",(estabid, contactnumIntForm))
            print("A New Number For Establishment " + estabname_input +" Is Added\n")
            conn.commit()
        else:
            print("There has been a problem on one of the attribute inputted\n")
    else:
        print("This establishment already has this contact number")
    return

def update_food_establishment(cur,conn):
    #updates specific attributes of an establishment in the table
    estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
    estabid = search_food_establishment_id(cur, estabname_input)
    if(check_estabid_exists(cur, estabid) == 0):
        return
    else:
        estabname_input = input("Enter Establishment Name to update for (Leave empty if do not want to update): ")
        branch_address_input = input("Enter Branch Address to update for (Leave empty if do not want to update): ")

        if(len(estabname_input) <= 50):
            estabname = estabname_input if estabname_input else None
        else:
            print("Invalid input for Establishment Name.")
            return
        if(len(branch_address_input) <= 50):
            branch_address = branch_address_input if branch_address_input else None
        else:
            print("Invalid input for Branch Address.")
            return
        
    update_query = "UPDATE food_estab SET "
    update_values = []

    if estabname is not None:
        update_query += "estabname=?, "
        update_values.append(estabname)

    if branch_address is not None:
        update_query += "branch_address=?, "
        update_values.append(branch_address)
            
    # Remove the trailing comma and space
    update_query = update_query[:-2]

    if(not update_values):
        print("There is no information to edit")
        return
    # Add the WHERE clause
    update_query += " WHERE estabid=?"

    # Add the estabid to the values list
    update_values.append(estabid)

    # Execute the update query
    cur.execute(update_query, update_values)
    conn.commit()
    print("Successfully Updated Details\n")
    return


#delete instance of food establishment
def delete_food_establishment(cur, conn):
    # Deletes a detail in the table
    estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
    estabid = search_food_establishment_id(cur, estabname_input)
    if(check_estabid_exists(cur, estabid)== 0):
        return
    #print("Removing all food products and its food type related to this food establishment")  # remove product id prompt when combined
    # Delete all related entries in food_type table
    cur.execute("SELECT productid FROM food_item WHERE estabid=?", (estabid,))
    product_ids = cur.fetchall()
    
    # Extract product IDs from tuples
    product_ids = [product_id[0] for product_id in product_ids]
    
    for product_id in product_ids:
        cur.execute("DELETE FROM food_type WHERE productid=?", (product_id,))
    
    # Delete all related entries in food_item table
    cur.execute("DELETE FROM food_item WHERE estabid=?", (estabid,))
        # Rules to delete a food establishment
        # Remove food_type because it uses productid as a FK
        # Remove food_item because it uses estabid as a FK
        # Remove estab_contact because it uses estabid as a FK, which is in a different function
        # After all that, you can now remove the establishment
        #cur.execute("DELETE FROM food_type WHERE productid=?", (productid,))  # needs to be deleted since estabid is a FK in this table
        #cur.execute("DELETE FROM food_item WHERE estabid=?", (estabid,))  # needs to be deleted since estabid is a FK in this table
    cur.execute("DELETE FROM estab_contact WHERE estabid=?", (estabid,))
    cur.execute("DELETE FROM user_reviews_foodestab WHERE estabid=?", (estabid,))
    cur.execute("DELETE FROM user_reviews_foodestab_item WHERE estabid=?", (estabid,))
    cur.execute("DELETE FROM food_estab WHERE estabid=?", (estabid,))
    conn.commit()
    print("Successfully Deleted\n")


#delete all instance of food establishment contact number
def delete_food_establishment_contact(cur, conn):
   #deletes detail in the table
   estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
   estabid = search_food_establishment_id(cur, estabname_input)
   if(check_estabid_exists(cur, estabid) == 0):
    return
   if(check_estabid_exists(cur,estabid) == 1 and check_estabid_in_contact_exists(cur,estabid) == 1):
    cur.execute("DELETE FROM estab_contact WHERE estabid=?",(estabid,))
    conn.commit()
    print("Successfully Deleted\n")
   else:
    print("There is no existing food establishment id with the same establishment id in contacts\n")
   return

#delete a single instance of food establishment contact number
def delete_food_establishment_contact_single(cur, conn):
   #deletes detail in the table
   estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
   estabid = search_food_establishment_id(cur, estabname_input)
   if(check_estabid_exists(cur, estabid) == 0):
    return
   contactnumIntForm = str(get_int_input("Enter Contact Number: "))
   if(check_estabid_exists(cur,estabid) == 1 and check_estabid_in_contact_exists(cur,estabid) == 1 and len(contactnumIntForm) == 11):
    cur.execute("DELETE FROM estab_contact WHERE estabid=? and contactnum=?",(estabid, contactnumIntForm))
    conn.commit()
    print("Successfully Deleted\n")
   else:
    print("There is no existing food establishment id with the same establishment id in contacts\n")
   return


def search_food_establishment(cur, conn):
    #search specific attributes of an establishment in the table
    estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
    estabid = search_food_establishment_id(cur, estabname_input)
    if(check_estabid_exists(cur, estabid) == 0):
        return

    branch_address_input = input("Enter Branch Address to search for (Leave empty if not specified): ")
    rating_input = input("Enter Rating to search for (Leave empty if not specified): ")
    rating = float(rating_input) if rating_input else None

    if(len(estabname_input) <= 50):
        estabname = estabname_input if estabname_input else None
    else:
        print("Invalid input for Establishment Name.")
        return
    if(len(branch_address_input) <= 50):
        branch_address = branch_address_input if branch_address_input else None
    else:
        print("Invalid input for Branch Address.")
        return

    search_query = "SELECT * FROM food_estab WHERE "
    search_values = []
    conditions = []

    if(estabid is not None):
        conditions.append("estabid=?")
        search_values.append(estabid)

    if(estabname is not None):
        conditions.append("estabname=?")
        search_values.append(estabname)

    if(branch_address is not None):
        conditions.append("branch_address=?")
        search_values.append(branch_address)

    if(rating is not None):
        conditions.append("rating=?")
        search_values.append(rating)

    search_query += " AND ".join(conditions)
    
    # Execute the search query
    cur.execute(search_query, search_values)

    rows = cur.fetchall()

    # Fetch column names from cursor description
    column_names = [desc[0] for desc in cur.description]

    # to print rows with null
    rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

    # Present data in table format
    print(tabulate(rows_with_null, headers=column_names, tablefmt="pretty"))

    return

def search_food_establishment_contact(cur, conn):
    #search specific attributes of an establishment contact in the table
    estabname_input = input("Enter Establishment Name <Establishment Name> - <General Location>: ")
    estabid = search_food_establishment_id(cur, estabname_input)
    if(check_estabid_exists(cur, estabid) == 0):
        return
    contactnumIntForm = (input("Enter Contact Number to search for (Leave empty if not specified): "))
    if(len(contactnumIntForm) <= 11):
        contactnumIntForm = contactnumIntForm if contactnumIntForm else None
    else:
        print("Invalid input for Contact Number.")
    search_query = "SELECT * FROM estab_contact WHERE "
    search_values = []
    conditions = []

    if(estabid is not None):
        conditions.append("estabid=?")
        search_values.append(estabid)

    if(contactnumIntForm is not None):
        conditions.append("contactnum=?")
        search_values.append(contactnumIntForm)

    search_query += " AND ".join(conditions)
    
    # Execute the search query
    cur.execute(search_query, search_values)

    rows = cur.fetchall()

    # Fetch column names from cursor description
    column_names = [desc[0] for desc in cur.description]

    # to print rows with null
    rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

    # Present data in table format
    print(tabulate(rows_with_null, headers=column_names, tablefmt="pretty"))

    return

#printing of details
def print_details(cur, table_name):
    """Retrieves the list of details from the database and prints in table format"""

    # Retrieve Contacts
    cur.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows from the cursor
    rows = cur.fetchall()

    # Fetch column names from cursor description
    column_names = [desc[0] for desc in cur.description]

    # to print rows with null
    rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

    # Present data in table format
    print(tabulate(rows_with_null, headers=column_names, tablefmt="pretty"))

# Instantiate Connection
try:
    conn = mariadb.connect(
        user="root",
        password="123123",
        host="127.0.0.1",
        port=3306,
        database="127projdb"
    )
except mariadb.Error as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)

# Instantiate Cursor
cur = conn.cursor()

# Close Connection
conn.close()
