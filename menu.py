import mariadb
import sys
import datetime
from tabulate import tabulate

from review_functions import *
from establishment_functions import *
from fooditems import *

# comment
# Connecting to mariadb
mydb = mariadb.connect(
    user="root",
    password="123123",
    host="127.0.0.1",
    port=3306,
    database="127projdb"
)

cur = mydb.cursor()  # make the connection to execute SQL queries


def sqlprint(rows, cur):
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

        foodchoice = int(input("\nEnter choice: "))
        # if foodchoice==1:
        #     #fxn
        # elif foodchoice==2: #fxn
        if foodchoice == 0:
            adminmenu()
        else:
            print("\nInvalid input.")  # prompt


def modifyestab():
    while True:
        print("\nMODIFY ESTABLISHMENT")
        print("[1] Insert an Establishment") #added
        print("[2] Update an Establishment")
        print("[3] Delete an Establishment")
        print("[4] Search an Establishment")
        print("[0] Back")
        estabchoice = int(input("\nEnter choice: "))
        if estabchoice == 1:
            #print("fxn here") to require at least one contact on the establishment
            add_food_establishment(cur,mydb)
            print("Add Information for contact number")
            add_food_establishment_contact(cur,mydb)
        elif estabchoice == 2:
            while True:
                print("[1] Update information of an Establishment")
                print("[2] (Optional) Add an additional contact number for an Establishment")
                print("[0] Back")
                echoice = int(input("\nEnter choice: "))
                if echoice == 1:
                    update_food_establishment(cur,mydb)
                elif echoice == 2:
                    add_food_establishment_contact(cur,mydb)
                elif echoice == 0:
                    break
                else:
                    print("\nInvalid input.")
        elif estabchoice == 3:
            while True:
                    ChoiceForOptionDelete = print_option_delete()
                    if ChoiceForOptionDelete == "1":
                        delete_food_establishment(cur, mydb)
                    elif ChoiceForOptionDelete == "2":
                        delete_food_establishment_contact(cur, mydb)
                    elif ChoiceForOptionDelete == "3":
                        delete_food_establishment_contact_single(cur, mydb)
                    elif ChoiceForOptionDelete == "0":
                        break
                    else:
                        print("Invalid Input")
        elif estabchoice == 4:
            while True:
                SearchChoice = print_menu_search()
                if SearchChoice == "1":
                    search_food_establishment(cur, mydb)
                elif SearchChoice == "2":
                    search_food_establishment_contact(cur, mydb)
                elif SearchChoice == "0":
                    break
                else:
                    print("Invalid input.\n")
        elif estabchoice == 0:
            break
        else:
            print("\nInvalid input.")  # prompt


def modifyreview():
    while True:
        print("\nMODIFY REVIEW")
        print("\n[1] Update a FOOD Review")
        print("[2] Delete a FOOD Review")
        print("\n[3] Update an ESTABLISHMENT Review")
        print("[4] Delete an ESTABLISHMENT Review")
        print("\n[0] Back")
        reviewchoice = int(input("\nEnter choice: "))
        if reviewchoice == 1:
            print("\nFUNCTION HERE")
        elif reviewchoice == 2:
            print("\nFUNCTION HERE")
        elif reviewchoice == 3:
            print("\nFUNCTION HERE")
        elif reviewchoice == 4:
            print("\nFUNCTION HERE")
        elif reviewchoice == 0:
            break
        else:
            print("\nInvalid input.")  # prompt


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

        viewchoice = int(input("\nEnter choice: "))
        if viewchoice == 1:
            viewEstabs()
        elif viewchoice == 2:
            viewFoodItems()
        elif viewchoice == 3:
            viewFoodReviews()
        elif viewchoice == 0:
            return
        else:
            print("\nInvalid input.")  # prompt


def viewEstabs():
    while True:
        print("-----VIEW ESTABLISHMENTS-----")
        print("\n[1] All establishments")
        print("[2] Highly-rated establishments only")
        print("[0] Back")
        choice = int(input("\nEnter choice: "))

        if choice == 1:
            cur.execute("select * from user_reviews_foodestab") #updated source table
            rows = cur.fetchall()

            sqlprint(rows, cur)

        elif choice == 2:
            cur.execute("select * from user_reviews_foodestab where rating>=4") #updated source table
            rows = cur.fetchall()

            sqlprint(rows, cur)

        elif choice == 0:
            return

        else:
            print("\nInvalid input.")


def viewFoodItems():
    while True:
        print("\n-----VIEW FOOD ITEMS-----")

        estabname = input("Establishment name: ")

        cur.execute("select * from food_item where estabid in (select estabid from food_estab where estabname = ?)",
                    (estabname,))
        rows = cur.fetchall()

        sqlprint(rows, cur)

        if not rows:
            break
        else:
            # ------filter-----
            print("\n[1] Filter by food type")
            print("[2] Order by price: low to high")
            print("[3] Order by price: high to low")
            print("[0] Back")
            userinput = int(input("\nEnter choice: "))

            if userinput == 1:
                filter = input("Filter by food type: ")

                cur.execute(
                    "select * from food_item where productid in (select productid from food_type where foodtype = ?) and estabid in (select estabid from food_estab where estabname = ?)",
                    (filter, estabname))
                rows = cur.fetchall()

                sqlprint(rows, cur)
                break

            elif userinput == 2:
                cur.execute(
                    "select * from food_item where estabid in (select estabid from food_estab where estabname = ?) order by price asc",
                    (estabname,))
                rows = cur.fetchall()

                sqlprint(rows, cur)
                break

            elif userinput == 3:
                cur.execute(
                    "select * from food_item where estabid in (select estabid from food_estab where estabname = ?) order by price desc",
                    (estabname,))
                rows = cur.fetchall()

                sqlprint(rows, cur)
            else:
                return


def viewFoodReviews():
    while True:
        print("\n-----VIEW FOOD REVIEWS-----")
        print("\n[1] Filter by establishment")
        print("[2] Filter by food type")
        print("[0] Back")
        userinput = int(input("\nEnter choice: "))

        if userinput == 1:
            estabname = input("Establishment name: ")

            cur.execute(
                "select * from reviewssummary where estabid in (select estabid from food_estab where estabname = ?)",
                (estabname,))
            rows = cur.fetchall()

            # Fetch column names from cursor description
            column_names = [desc[0] for desc in cur.description]

            # to print rows with null
            rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

            # Present data in table format
            print(tabulate(rows_with_null, headers=column_names, tablefmt="coquette"))

            bymonth = input("\nFilter by month (Y/N)? ")

            if bymonth.lower() == "n":
                return
            else:
                month = input("\nEnter month in MM: ")
                cur.execute(
                    "select * from reviewssummary where estabid in (select estabid from food_estab where estabname = ?) and month(date_of_review)=?",
                    (estabname, month))
                rows = cur.fetchall()

                # Fetch column names from cursor description
                column_names = [desc[0] for desc in cur.description]

                # to print rows with null
                rows_with_null = [[cell if cell is not None else "NULL" for cell in row] for row in rows]

                # Present data in table format
                print("\n")
                print(tabulate(rows_with_null, headers=column_names, tablefmt="coquette"))

        elif userinput == 2:
            foodtype = input("Enter food type: ")

            cur.execute(
                "select * from reviewssummary where productid in (select productid from food_type where foodtype = ?)",
                (foodtype,))
            rows = cur.fetchall()

            sqlprint(rows, cur)

            if not rows:
                break
            else:
                bymonth = input("\nFilter by month (Y/N)? ")

                if bymonth.lower() == "n":
                    return
                else:
                    month = input("\nEnter month in MM: ")
                    cur.execute(
                        "select * from reviewssummary where productid in (select productid from food_type where foodtype = ?) and month(date_of_review)=?",
                        (foodtype, month))
                    rows = cur.fetchall()

                    sqlprint(rows, cur)
        elif userinput == 0:
            break
        else:
            print("\nInvalid input.")  # prompt


def adminmenu():
    while True:
        print("\nMAIN MENU")
        print("\n[1] Modify Food Item")  # modify=update and delete
        print("[2] Manage Establishment")
        print("[3] Modify Review")
        print("[4] Search Food Item")
        print("[5] View")
        print("[0] Exit")
        choice = int(input("\n""Enter choice: "))

        if choice == 1:
            newFoodItemTransaction(cur)
        elif choice == 2:
            modifyestab()
        elif choice == 3:
            modifyreview()
        elif choice == 4:
            search()
        elif choice == 5:
            view()
        elif choice == 0:
            print("Goodbye!")
            quit()
        else:
            print("\nInvalid input.")  # prompt


def customermenu(username, password):
    while True:
        print("\nMAIN MENU")

        print("\n[1] Review a Food Item")
        print("[2] Review an Establishment")
        print("[3] Update a Review")
        print("[4] Delete a Review")
        print("[5] Search Food Item")
        print("[6] View")
        print("[0] Exit")
        choice = int(input("\n""Enter choice: "))

        if choice == 1:
            addFoodItemReview(username, password)
        elif choice == 2:
            addFoodEstabReview(username, password)
        elif choice == 3:
            while True:
                print("\nUPDATE A REVIEW")
                print("\n[1] Food Establishment Review")
                print("[2] Food Item Review")
                print("[0] Back")
                update_choice = int(input("\nEnter choice: "))

                if update_choice == 1:
                    updateFoodEstabReview(username, password)
                elif update_choice == 2:
                    updateFoodItemReview(username, password)
                elif update_choice == 0:
                    break
                else:
                    print("\nInvalid input.")
        elif choice == 4:
            print("\nDELETE A REVIEW")
            print("\n[1] Delete a Food Establishment Review")
            print("[2] Delete a Food Item Review")
            print("[0] Back")
            delete_choice = int(input("\nEnter choice: "))

            if delete_choice == 1:
                deleteEstabReview(username, password)
            elif delete_choice == 2:
                deleteFoodReview(username, password)
            elif delete_choice == 0:
                break
            else:
                print("\nInvalid input.")
        elif choice == 5:
            search()
        elif choice == 6:
            view()
        elif choice == 0:
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
                print("Welcome back, admin " + username + "!")
                adminmenu()
            elif any(username in row and password in row for row in rows):
                print("\nWelcome back, user " + username + "!")
                customermenu(username, password)
            elif any(username in row for row in rows):
                print("\nIncorrect password for user " + username + ". Try again.")
            else:
                print("\nUser does not exist. Sign up instead.")
        elif login == 2:
            name = input("Name: ")
            username = input("Username: ")
            contact_number = input("Contact number: ")
            password = input("Password: ")
            confirmpw = input("Confirm Password: ")

            if confirmpw == password:
                cur.execute("insert into user (name, username, password) values (?, ?, ?)", (name, username, password))
                mydb.commit()
                cur.execute("select userid from user where username = ? and password = ?", (username, password))
                row = cur.fetchone()
                userid = row[0]
                cur.execute("insert into user_contact (userid, contactnum) values (?, ?)", (userid, contact_number))
                mydb.commit()
                print("\nUser " + username + " has been signed up.")
                customermenu(username, password)
            else:
                print("\nPasswords do not match. Try again.")
        elif login == 0:
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")
            main()
            break


main()