import mariadb
from tabulate import tabulate

#Connecting to mariadb
mydb = mariadb.connect(
    host="localhost", 
    port=3306,
    user="127projdb", 
    password="user", 
    database="127projdb"
)

cur = mydb.cursor() #make the connection to execute SQL queries

def sqlprint(rows,cur):
    if not rows:
        print("No results found.")
    else:
        # fetch column names from cursor description
        column_names = [desc[0] for desc in cur.description]

        # to print rows with null
        rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

        # present data in table format
        print(tabulate(rows_with_null, headers=column_names, tablefmt="coquette"))

def modifyfood():
    while True:
                print("\nMODIFY FOOD ITEM")
                print("\n[1] Update a Food Item") 
                print("[2] Delete a Food Item")
                print("[0] Back")

                foodchoice=int(input("\nEnter choice: "))
                # if foodchoice==1:
                #     #fxn
                # elif foodchoice==2: #fxn   
                if foodchoice==0: 
                    adminmenu()
                else:
                    print("\nInvalid input.") #prompt

def modifyestab():
    while True: 
            print("\nMODIFY ESTABLISHMENT")
            print("\n[1] Update an Establishment") 
            print("[2] Delete an Establishment")
            print("[0] Back")
            estabchoice=int(input("\nEnter choice: "))
            if estabchoice==1:
                print("fxn here")
            elif estabchoice==2: 
                print("fxn here")
            elif estabchoice==0:
                break
            else:
                print("\nInvalid input.") #prompt

def modifyreview():
    while True:
            print("\nMODIFY REVIEW")
            print("\n[1] Update a FOOD Review") 
            print("[2] Delete a FOOD Review")
            print("\n[3] Update an ESTABLISHMENT Review") 
            print("[4] Delete an ESTABLISHMENT Review")
            print("\n[0] Back")
            reviewchoice=int(input("\nEnter choice: "))
            if reviewchoice==1:
                print("\nFUNCTION HERE")
            elif reviewchoice==2: 
                print("\nFUNCTION HERE")
            elif reviewchoice==3: 
                print("\nFUNCTION HERE")
            elif reviewchoice==4: 
                print("\nFUNCTION HERE")
            elif reviewchoice==0:
                break 
            else:
                print("\nInvalid input.") #prompt

def search():
    while True:
        minprice = input("\nMinimum price (N/A if not applicable): ")
        if minprice.lower() == "n/a" or (minprice.strip() and minprice.isdigit()):
            break
        else:
            print("\nInvalid input. Please enter 'N/A' or a valid integer.")

    if minprice.lower() != "n/a":
        while True:
            maxprice = input("\nMaximum price: ")
            if maxprice.lower() == "n/a" or (maxprice.strip() and maxprice.isdigit()):
                if maxprice.lower() == "n/a" or int(maxprice) >= int(minprice):
                    break
                else:
                    print("\nMaximum price cannot be lower than the minimum. Try again.")
            else:
                print("\nInvalid input. Please enter 'N/A' or a valid integer.")

        foodtype = input("\nFood type (N/A if not applicable): ")
        while not foodtype.strip():
            print("\nInput required.")
            foodtype = input("\nFood type (N/A if not applicable): ")
    else:
        while True:
            maxprice = input("\nMaximum price (N/A if not applicable): ")
            if maxprice.lower() == "n/a" or (maxprice.strip() and maxprice.isdigit()):
                break
            else:
                print("\nInvalid input. Please enter 'N/A' or a valid integer.")

        if maxprice.lower() == "n/a":
            while True:
                foodtype = input("\nFood type: ")
                if foodtype.strip(): 
                    break
                else:
                    print("\nInput required.")
                cur.execute("SELECT * FROM food_item i NATURAL JOIN food_type t WHERE t.foodtype = ?", (foodtype,))
                rows = cur.fetchall()
                sqlprint(rows,cur)
        else:
            while True:
                foodtype = input("\nFood type (N/A if not applicable): ")
                if foodtype.strip():
                    break
                else:
                    print("\nInput required.")

    if minprice.lower() != "n/a" and maxprice.lower() != "n/a" and foodtype.lower() != "n/a":
        cur.execute("SELECT * FROM food_item i NATURAL JOIN food_type t WHERE ((i.price BETWEEN ? AND ?) AND t.foodtype = ?)", (minprice, maxprice, foodtype))
    elif minprice.lower() != "n/a" and maxprice.lower() != "n/a" and foodtype.lower() == "n/a":
        cur.execute("SELECT * FROM food_item i WHERE i.price BETWEEN ? AND ?", (minprice, maxprice))
    elif minprice.lower() == "n/a" and maxprice.lower() != "n/a" and foodtype.lower() != "n/a":
        cur.execute("SELECT * FROM food_item i NATURAL JOIN food_type t WHERE (t.foodtype = ?)", (foodtype,))
    elif minprice.lower() != "n/a" and maxprice.lower() == "n/a" and foodtype.lower() != "n/a":
        cur.execute("SELECT * FROM food_item i NATURAL JOIN food_type t WHERE (t.foodtype = ?)", (foodtype,))
    elif minprice.lower() != "n/a" and maxprice.lower() == "n/a" and foodtype.lower() == "n/a":
        cur.execute("SELECT * FROM food_item i WHERE i.price >= ?", (minprice,))
    elif minprice.lower() == "n/a" and maxprice.lower() != "n/a" and foodtype.lower() == "n/a":
        cur.execute("SELECT * FROM food_item i WHERE i.price <= ?", (maxprice,))
    elif minprice.lower() == "n/a" and maxprice.lower() == "n/a" and foodtype.lower() != "n/a":
        cur.execute("SELECT * FROM food_item i NATURAL JOIN food_type t WHERE (t.foodtype = ?)", (foodtype,))
    else:
        cur.execute("SELECT * FROM food_item")

    rows = cur.fetchall()
    sqlprint(rows, cur)


def view():
    while True:
                print("\nVIEW REPORTS")
                print("[1] Generate report on establishments")
                print("[2] Generate report on food items")
                print("[3] Generate report on food reviews")
                print("[0] Back")
                
                viewchoice=int(input("\nEnter choice: "))
                if viewchoice==1:
                    viewEstabs()
                elif viewchoice==2:
                    viewFoodItems()
                elif viewchoice==3: 
                    viewFoodReviews()
                elif viewchoice==0: 
                    return
                else:
                    print("\nInvalid input.") #prompt

def viewEstabs():
    while True:
        print("-----VIEW ESTABLISHMENTS-----")
        print("\n[1] All establishments")
        print("[2] Highly-rated establishments only")
        print("[0] Back")
        choice=int(input("\nEnter choice: "))

        if choice==1:
            cur.execute("select * from user_reviews_foodestab") #updated source table
            rows = cur.fetchall()

            sqlprint(rows,cur)
            
        elif choice==2:
            cur.execute("select * from user_reviews_foodestab where rating>=4") #updated source table
            rows = cur.fetchall()

            sqlprint(rows,cur)
        
        elif choice==0: 
            return
        
        else: print("\nInvalid input.")

def viewFoodItems():
    while True:
        print("\n-----VIEW FOOD ITEMS-----")

        estabname=input("Establishment name: ")

        cur.execute("select * from food_item where estabid in (select estabid from food_estab where estabname = ?)", (estabname,))
        rows = cur.fetchall()

        sqlprint(rows,cur)

        if not rows:
            break
        else:
        #------filter-----
            print("\n[1] Filter by food type")
            print("[2] Order by price: low to high")
            print("[3] Order by price: high to low")
            print("[0] Back")
            userinput=int(input("\nEnter choice: "))

            if userinput==1:
                filter=input("Filter by food type: ")
                
                cur.execute("select * from food_item where productid in (select productid from food_type where foodtype = ?) and estabid in (select estabid from food_estab where estabname = ?)", (filter,estabname))
                rows = cur.fetchall()

                sqlprint(rows,cur)
                break
                
            elif 2:
                cur.execute("select * from food_item where estabid in (select estabid from food_estab where estabname = ?) order by price asc", (estabname,))
                rows = cur.fetchall()

                sqlprint(rows,cur)
                break

            elif 3:
                cur.execute("select * from food_item where estabid in (select estabid from food_estab where estabname = ?) order by price desc", (estabname,))
                rows = cur.fetchall()

                sqlprint(rows,cur)
            else: return

def viewFoodReviews():
    while True:
        print("\n-----VIEW FOOD REVIEWS-----")
        print("\n[1] Filter by establishment")
        print("[2] Filter by food type")
        print("[0] Back")
        userinput=int(input("\nEnter choice: "))

        if userinput==1:
            estabname=input("Establishment name: ")
            
            cur.execute("select * from reviewssummary where estabid in (select estabid from food_estab where estabname = ?)", (estabname,))
            rows = cur.fetchall()

            # Fetch column names from cursor description
            column_names = [desc[0] for desc in cur.description]

            # to print rows with null
            rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

            # Present data in table format
            print(tabulate(rows_with_null, headers=column_names, tablefmt="coquette"))
            
            bymonth=input("\nFilter by month (Y/N)? ")

            if bymonth.lower()=="n":
                return
            else:
                month=input("\nEnter month in MM: ")
                cur.execute("select * from reviewssummary where estabid in (select estabid from food_estab where estabname = ?) and month(date_of_review)=?", (estabname,month))
                rows = cur.fetchall()

                # Fetch column names from cursor description
                column_names = [desc[0] for desc in cur.description]

                # to print rows with null
                rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

                # Present data in table format
                print("\n")
                print(tabulate(rows_with_null, headers=column_names, tablefmt="coquette")) 
                
        elif userinput==2:
            foodtype=input("Enter food type: ")
            
            cur.execute("select * from reviewssummary where productid in (select productid from food_type where foodtype = ?)", (foodtype,))
            rows = cur.fetchall()

            sqlprint(rows,cur) 
            
            if not rows:
                break
            else:
                bymonth=input("\nFilter by month (Y/N)? ")

                if bymonth.lower()=="n":
                    return
                else:
                    month=input("\nEnter month in MM: ")
                    cur.execute("select * from reviewssummary where productid in (select productid from food_type where foodtype = ?) and month(date_of_review)=?", (foodtype,month))
                    rows = cur.fetchall()

                    
                    sqlprint(rows,cur)   
        elif userinput==0: 
            break
        else:
            print("\nInvalid input.") #prompt
    
def adminmenu():
    while True:
        print("\nMAIN MENU")
        
        print("\n[1] Modify Food Item") #modify=update and delete
        print("[2] Modify Establishment")
        print("[3] Modify Review")
        print("[4] Search Food Item")
        print("[5] View")
        print("[0] Exit")
        choice=int(input("\n""Enter choice: "))

        if choice==1:
            modifyfood()
                       
        elif choice==2:
            modifyestab()

        elif choice==3:
            modifyreview()
        elif choice == 4:
            search()
        elif choice == 5:
            view()
        elif choice == 0:
            print("Goodbye!")
            quit()
        else:
            print("\nInvalid input.") #prompt

def customermenu():

    while True:
        print("\nMAIN MENU")
        
        print("\n[1] Review a Food Item")
        print("[2] Review an Establishment")
        print("[3] Update a Review")
        print("[4] Delete a Review")
        print("[5] Search Food Item")
        print("[6] View")
        print("[0] Exit")
        choice=int(input("\n""Enter choice: "))

        if choice==1:
            print("#fxn here")           
        elif choice==2:
            print("#fxn here")
        elif choice==3:
            print("#fxn here")
        elif choice == 4:
            print("#fxn here")
        elif choice == 5:
            search()
        elif choice == 6:
            view()
        elif choice==0:
            break
        else:
            print("\nInvalid input.")

def main():

    adminusername = "admin"
    adminpassword = "admin"

    while True:
        print("\nWelcome to the Food Review System!") 
        print("\n[1] Log in")
        print("[2] Sign up")
        print("[0] Exit")

        login = int(input("\nEnter choice: "))
        
        if login == 1:
            username = input("Username: ")
            password = input("Password: ")
            
            cur.execute("select username, password from user")
            rows = cur.fetchall()

            if (username, password) == (adminusername, adminpassword):
                print("Welcome back, admin "+username+"!")
                adminmenu()
            elif any(username in row and password in row for row in rows):
                print("\nWelcome back, user "+username+"!")
                customermenu()
            elif any(username in row for row in rows):
                print("\nIncorrect password for user "+ username+". Try again.")
            else:
                print("\nUser does not exist. Sign up instead.")
        elif login == 2:
            username = input("Username: ")
            password = input("Password: ")
            confirmpw = input("Confirm Password: ")

            if confirmpw == password:
                print("add_user(username, password)")  # Add the new user to the database
                print("\nUser " + username + " has been signed up.")
                customermenu()
            else:
                print("\nPasswords do not match. Try again.")
        elif login==0:
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")
            main()
            break

main()
