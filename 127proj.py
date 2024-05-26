import mariadb
import sys
from tabulate import tabulate

def print_menu():
    print("#-------------------------------------------------------------#")
    print("Main Menu")
    print("[1] Food Establishment")
    print("[0] Exit\n")
    print("#-------------------------------------------------------------#")

    ChoiceForMenu = input("\nEnter choice: ")
    return ChoiceForMenu

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
    print("[1] Delete All Contact Number Related To A Food Establishment")
    print("[2] Delete Single A Contact Number Related To A Food Establishment")
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

# Adds single food establishment
def add_food_establishment(cur,estabid, estabname, branch_address, rating):
    #adds the given details about food establishment to the food establishment table
    cur.execute("INSERT INTO food_estab(estabname, branch_address, rating) VALUES (?, ?, ?)",(estabname, branch_address, rating))
    return

# Adds single contact
def add_food_establishment_contact(cur, estabid, contactnum):
    #adds the given details about food establishment contact number to the food establishment contact number table
    cur.execute("INSERT INTO estab_contact(estabid, contactnum) VALUES (?, ?)",(estabid, contactnum))
    return

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

#delete instance of food establishment
def delete_food_establishment(cur, estabid, productid):
   """Deletes detail in the table"""
   print("removing all food products and its food type related to this fodd establishment")  #pagnapagsama sama na pakibura na lang nung product id 
   # rules to delete a food establishment
   # remove food_type because it uses product id as a fk
   # remove food_item because it uses establishment id as a fk
   # remove estab_contact because it uses establishment id as a fk it is in a different function dont worry 
   # after all that you can now remove the establishment
   cur.execute("DELETE FROM food_type WHERE productid=?", (productid,)) #needs to be deleted since it is estabid is a fk in this table
   cur.execute("DELETE FROM food_item WHERE estabid=?", (estabid,)) #needs to be deleted since it is estabid is a fk in this table
   cur.execute("DELETE FROM food_estab WHERE estabid=?",(estabid,))
   return

#delete all instance of food establishment contact number
def delete_food_establishment_contact(cur, estabid):
   """Deletes detail in the table"""
   cur.execute("DELETE FROM estab_contact WHERE estabid=?",(estabid,))
   return

#delete a single instance of food establishment contact number
def delete_food_establishment_contact_single(cur, estabid, contactnum):
   """Deletes detail in the table"""
   cur.execute("DELETE FROM estab_contact WHERE estabid=? and contactnum=?",(estabid, contactnum))
   return


def update_food_establishment(cur, estabid, estabname=None, branch_address=None, rating=None):
    #updates specific attributes of an establishment in the table

    update_query = "UPDATE food_estab SET "
    update_values = []

    if estabname is not None:
        update_query += "estabname=?, "
        update_values.append(estabname)

    if branch_address is not None:
        update_query += "branch_address=?, "
        update_values.append(branch_address)

    if(rating is not None):
        rating_array = [1,2,3,4,5]
        if(rating not in rating_array):
            print("Invalid Rating input.")
            return
        else:
            update_query += "rating=?, "
            update_values.append(rating)
            
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
    print("Successfully Updated Details")

    return

def search_food_establishment(cur, estabid=None, estabname=None, branch_address=None, rating=None):
    #search specific attributes of an establishment in the table
    
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
        rating_array = [1, 2, 3, 4, 5]
        if rating not in rating_array:
            print("Invalid Rating input.")
            return
        else:
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

def search_food_establishment_contact(cur, estabid=None, contactnum=None):
    #search specific attributes of an establishment contact in the table
    
    search_query = "SELECT * FROM estab_contact WHERE "
    search_values = []
    conditions = []

    if(estabid is not None):
        conditions.append("estabid=?")
        search_values.append(estabid)

    if(contactnum is not None):
        conditions.append("contactnum=?")
        search_values.append(contactnum)

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
        host="localhost",
        port=3306,
        user="127projdb",
        password="group5",
        database="127projdb"
    )
except mariadb.Error as e:
    print(f"Error connecting to the database: {e}")
    sys.exit(1)

# Instantiate Cursor
cur = conn.cursor()

# Call function to print contacts in table format
while True:
    ChoiceForMenu = print_menu()

    #Options
    if ChoiceForMenu == "1":#Go for a transaction in food establishment
        while True:
            ChoiceForTransaction = NewTransaction()

            if ChoiceForTransaction == "1":
                estabname = (input("Enter Establishment Name: "))
                branch_address = (input("Enter Branch Address: "))
                rating = int(input("Enter Rating: "))
                rating_array = [1,2,3,4,5]
                if(len(estabname) > 50 or len(branch_address) > 50 or rating not in rating_array or len(estabid_input) > 5):
                    print("There has been a problem on one of the attribute inputted")
                else:
                    add_food_establishment(cur,estabid, estabname, branch_address, rating)
                    conn.commit()
                    print("Food Establishment Details Added To The Food Establishment Table\n")
            
            elif ChoiceForTransaction == "2":
                estabid = get_int_input("Enter Establishment ID: ")
                contactnumIntForm = str(int(input("Enter Contact Number: ")))
                if(len(contactnumIntForm) == 11 and check_estabid_exists(cur,estabid) == 1):
                    add_food_establishment_contact(cur, estabid, contactnumIntForm)
                    conn.commit()
                    print("A New Number For Establishment " + str(estabid) +" Is Added\n")
                else:
                    print("There has been a problem on one of the attribute inputted\n")
    
            elif ChoiceForTransaction == "3":
                estabid = get_int_input("Enter Establishment ID: ")
                if check_estabid_exists(cur, estabid) == 0:
                    print("Invalid Establishment ID.")
                else:
                    estabname_input = input("Enter Establishment Name to update for (Leave empty if do not want to update): ")
                    branch_address_input = input("Enter Branch Address to update for (Leave empty if do not want to update): ")
                    rating_input = input("Enter Rating to search for (Leave empty if do not want to update): ")
                    rating = int(rating_input) if rating_input else None

                    if(len(estabname_input) <= 50):
                        estabname = estabname_input if estabname_input else None
                    else:
                        print("Invalid input for Establishment Name.")
                    if(len(branch_address_input) <= 50):
                        branch_address = branch_address_input if branch_address_input else None
                    else:
                        print("Invalid input for Branch Address.")
                    update_food_establishment(cur, estabid, estabname, branch_address, rating)
                    conn.commit()
                    print("\n")

            elif ChoiceForTransaction == "4":
                estabid = get_int_input("Enter Establishment ID: ")
                productid = int(input("Enter Product ID: "))#remove later on when combined with all
                if(check_estabid_in_contact_exists(cur,estabid) == 0):
                    delete_food_establishment(cur,estabid, productid)
                    conn.commit()
                    print("Successfully Deleted\n")
                else:
                    print("Delete first the contact number that has the same establishment id\n")
            
            elif ChoiceForTransaction == "5":
                while True:
                    ChoiceForOptionDelete = print_option_delete()

                    if ChoiceForOptionDelete == "1":
                        estabid = get_int_input("Enter Establishment ID: ")
                        if(check_estabid_exists(cur,estabid) == 1 and check_estabid_in_contact_exists(cur,estabid) == 1):
                            delete_food_establishment_contact(cur,estabid)
                            conn.commit()
                            print("Successfully Deleted\n")
                        else:
                            print("There is no existing food establishment id with the same establishment id in contacts\n")
                    
                    elif ChoiceForOptionDelete == "2":
                        estabid = get_int_input("Enter Establishment ID: ")
                        contactnumIntForm = str(int(input("Enter Contact Number: ")))
                        if(check_estabid_exists(cur,estabid) == 1 and check_estabid_in_contact_exists(cur,estabid) == 1 and len(contactnumIntForm) == 11):
                            delete_food_establishment_contact_single(cur,estabid,contactnumIntForm)
                            conn.commit()
                            print("Successfully Deleted\n")
                        else:
                            print("There is no existing food establishment id with the same establishment id in contacts\n")
                    
                    elif ChoiceForOptionDelete == "0":
                        break

                    else:
                        print("Invalid Input")

            elif ChoiceForTransaction == "6":
                estabid = get_int_input("Enter Establishment ID: ")
                if check_estabid_exists(cur, estabid) == 0:
                    print("Invalid Establishment ID.")
                else:
                    estabname_input = input("Enter Establishment Name to search for (Leave empty if not specified): ")
                    branch_address_input = input("Enter Branch Address to search for (Leave empty if not specified): ")
                    rating_input = input("Enter Rating to search for (Leave empty if not specified): ")
                    rating = int(rating_input) if rating_input else None

                    if(len(estabname_input) <= 50):
                        estabname = estabname_input if estabname_input else None
                    else:
                        print("Invalid input for Establishment Name.")
                    if(len(branch_address_input) <= 50):
                        branch_address = branch_address_input if branch_address_input else None
                    else:
                        print("Invalid input for Branch Address.")
                    search_food_establishment(cur, estabid, estabname, branch_address, rating)
                    print("\n")
                    
            elif ChoiceForTransaction == "7":
                estabid = get_int_input("Enter Establishment ID: ")
                if check_estabid_exists(cur, estabid) == 0:
                    print("Invalid Establishment ID.")
                else:
                    contactnumIntForm = (input("Enter Contact Number to search for (Leave empty if not specified): "))
                    if(len(contactnumIntForm) <= 11):
                        contactnumIntForm = contactnumIntForm if contactnumIntForm else None
                    else:
                        print("Invalid input for Contact Number.")
                    search_food_establishment_contact(cur, estabid, contactnumIntForm)
                    print("\n")

            elif ChoiceForTransaction == "8":
                print_details(cur, "food_estab")
                print("\n")

            elif ChoiceForTransaction == "9":
                print_details(cur, "estab_contact")
                print("\n")

            elif ChoiceForTransaction == "0":
                break

            else:
                print("Invalid Choice")

    # Shows how much discount to get
    elif ChoiceForMenu == "0":
        break
    
    else:
        print("Invalid Choice")

# Close Connection
conn.close()
