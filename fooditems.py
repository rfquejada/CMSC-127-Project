# Module Imports
import mariadb
import sys
from tabulate import tabulate
###### Functions for Food Items

def check_productid_foodtype_exists(cur, productid, foodtype):
    #checks if the given estabid exists in the contacts table
    cur.execute("SELECT COUNT(*) FROM food_type WHERE productid = ? and foodtype = ?", (productid,foodtype))
    count = cur.fetchone()[0]
    return count > 0 

#Add Food Item
def addFoodItem(cur):
    name = input("Please input the name of the product: ")
    price = int(input("Please input the listed price: ")) #wraps the input with int
    estab = input("Please input the name of the establishment selling the product (i.e. Jollibee Vega): ") 
    estab = estab.split() #if the input is two words or more, turns the input into "like '%%'" format in order to not limit the user to input exactly what is in the db
    estabquery = "SELECT estabid from food_estab where estabname like '%"
    for string in estab:
        estabquery += (string + '%')
    estabquery += "'"
    cur.execute(estabquery)
    try:
        estabid = cur.fetchone()[0] #stores the estabid; if None, returns to menu and prints error msg
    except:
        return print("Establishment Not Found! Please add the establishment first before adding the item or check for possible spelling mistakes.")
    cur.execute("INSERT INTO `food_item` (`itemname`, `price`, `estabid`) VALUES (?,?,?)", (name, price, estabid))
    cur.execute("SELECT productid from food_item where itemname = ?", (name, )) #gets the newly create id to use in adding the food types
    itemid = cur.fetchone()[0]
    addFoodType(itemid, cur)
    return print("Food Item Added!")

#function that stores the loop of adding new food types
def addFoodType(itemid, cur): 
    addCheck = True #flag to keep the loop running until stopped by user
    while addCheck:
        foodtype = input("\nPlease input the type of the food: ")
        if not check_productid_foodtype_exists(cur, itemid, foodtype):
            cur.execute('INSERT INTO `food_type` (`productid`,`foodtype`) VALUES (?, ?)', (itemid, foodtype))
            print("Food Type Added!")
        else:
            print("This product already has this food type")

        while True:
            cont = input("\nAdd more food types? 1 for YES, 0 for NO: ")
            if cont == '0':
                addCheck = False
                break
            elif cont == '1':
                break
            else:
                print("Invalid Input!")
    return


#Update Food Item
def updateFoodItem(cur):
    itemid = searchFoodItem(cur, 1) #calls search func with flag 1 to get itemid
    if itemid == None: #if none, return to menu
        return

    while True: #catches invalid inputs
        print("#--------------------------------------------------#")
        choice = input("\nWhat to edit? \n[1] Item Name \n[2] Price \n[3] Add Food Type\n[4] Remove Food Type\n[0] Exit\n\nInput:")
        if choice == '1': #updates name of product
            name = input("Input new name: ")
            cur.execute('Update food_item set itemname = ? where productid = ?', (name, itemid))
            break
        elif choice == '2': #updates price of product
            price = input("Input new price: ")
            cur.execute('Update food_item set price = ? where productid = ?', (price, itemid))
            break
        elif choice == '3': #allows the user to add new types
            addFoodType(itemid, cur)
            break
        elif choice == '4': #allows the user to delete existing food types of the item
            deleteFoodType(itemid, cur)
            break
        elif choice == '0':
            return
        else:
            print("Invalid input!")
    
    return print("Item Updated!")

#delete func for food type (similar to addFoodType)
def deleteFoodType(itemid, cur): 
    delCheck = True
    while delCheck:
        cur.execute("SELECT itemname 'Food Item', foodtype 'Food Type' from food_type t, food_item i where t.productid = ? and i.productid = ?", (itemid, itemid)) #fetches all food type assoc with item
        entries = cur.fetchall()
        count = len(entries) #gets count as each item must have 1 type, so delete will be disabled if only 1 type is left
        if count == 1:
            print("\nThis food item has only one food type left! Deleting its lone food type is not allowed.\n")
            return
        
        column_names = [desc[0] for desc in cur.description]
        print(tabulate(entries, headers=column_names, tablefmt="pretty")) #presents the table of possible values to the user
        foodtype = input("Please input the type of the food item to delete: ") #asks for what the user wants to delete
        cur.execute('DELETE FROM food_type where productid = ? AND foodtype = ?', (itemid, foodtype))

        while True:
            cont = input("Delete more food types of this item? 1 for YES, 0 for NO: ")
            if cont == '0':
                delCheck = False
                break
            elif cont == '1':
                break
            else:
                print("Invalid Input!")
    return

#Delete Food Item
def deleteFoodItem(cur):
    itemid = searchFoodItem(cur, 1) #gets id from search with 1 flag
    if itemid == None:
        return
    
    cur.execute("DELETE FROM food_type WHERE productid = ?", (itemid,)) #deletes all types
    cur.execute("DELETE FROM food_item WHERE productid = ?", (itemid,)) #deletes item
    return print("Item deleted!")

#Search Food Item
def searchFoodItem(cur, flag): #flag is for reusability of search: 1 is for id search, 0 is for printing of the row

    name = input("Input name of the item: ")
    name = name.split() #allows 2 or more worded names to be used in finding the item
    namequery = "SELECT * from food_item where itemname like '%"
    for string in name:
        namequery += (string + '%')
    namequery += "'"

    #finds the associated estab which the item is associated to
    estab = input("Which establishment is selling the product? (i.e. Jollibee Vega): ")
    estab = estab.split()
    namequery += ("AND estabid = (select estabid from food_estab where estabname like '%")
    for string in estab:
        namequery += (string + '%')
    namequery += ("' LIMIT 1)")
    cur.execute(namequery)
    
    #filters if the func was called to return all details of the product or the id only
    if flag == 0:
        #print row
        row = cur.fetchone()
        if row == None:
            return print("No record of product!")
        
        print("#------------------------- Food Details -------------------------#")
        print('Name: ', row[1] , '\nPrice: ', row[2], '\nRating: ', row[3])
        cur.execute("Select estabname from food_estab where estabid = ?", (row[4],)) #gets the name of the establishment assoc.
        storedEstabName = cur.fetchone()[0]
        print("Sold by: ", storedEstabName)
        cur.execute("SELECT foodtype from food_type where productid = ?", (row[0],)) #gets all food types of the item
        print("Food Type/s: ")
        for type in cur:
            print("[] ", type[0])
        print("#---------------------- End of Food Details ---------------------#")
        return 
    else:
        try:
            itemid = cur.fetchone()[0] #stores id
        except:
            print("Product not found!")
            return None
        return itemid #returns the id

def newFoodItemTransaction(cur):
    while True:
        print("#-------------------------------------------------------------#")
        print("[1] Add Food Item")
        print("[2] Edit Food Item")
        print("[3] Delete Food Item")
        print("[4] Search Food Item (Singular)")
        print("[0] Back to Main Menu")
        print("#-------------------------------------------------------------#")

        ChoiceForTransaction = input("\nWhat you want to do?\nEnter choice: ")

        if ChoiceForTransaction == "1":
            addFoodItem(cur)
        elif ChoiceForTransaction == "2":
            updateFoodItem(cur)
        elif ChoiceForTransaction == "3":
            deleteFoodItem(cur)
        elif ChoiceForTransaction == "4":
            searchFoodItem(cur, 0)
        elif ChoiceForTransaction == "0":
            return
        else:
            print("Invalid Choice")
    
# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="123123",
        host="127.0.0.1",
        port=3306,
        database="127projdb",
        autocommit=True
    )
except mariadb.Error as e:
    print("Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# Close Connection
conn.close()


