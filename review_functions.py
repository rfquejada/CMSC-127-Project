import mariadb
import sys
import datetime
from tabulate import tabulate


def create_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="123123",
            host="127.0.0.1",
            port=3306,
            database="127projdb"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


#Function to execute queries
def execute_query(query, params):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

#Function to add a review for a food item
def addFoodItemReview(username, password):
    print("*****FOOD ITEM REVIEW*****")
    userid = fetchUserId(username, password)

    #Fetch estab id
    estabid = fetchEstabId()
    if estabid is None:
        print("Establishment not found.")
        return

    #Fetch productid
    productid = fetchProductId(estabid)
    if productid is None:
        print("Product not found.")
        return

    #Get user inputs
    rating = float(input("Enter rating (1-5): "))
    if(rating < 1 or rating > 5):
        print("Please enter a rating of 1 to 5 only.")
        return
    dateofreview = datetime.datetime.now()
    body = input("Enter review (200 characters): ")
    if len(body) > 200:
        print("Please shorten your review to 200 characters only.")
        return

    query = "insert into user_reviews_foodestab_item (`userid`, `estabid`, `productid`, `rating`, `date_of_review`, `body`) values (?, ?, ?, ?, ?, ?)"
    params = (userid, estabid, productid, rating, dateofreview, body)

    #Execute the query
    execute_query(query, params)

    # Updates the average rating of the food item
    getRatingQuery = "select avg(rating) from user_reviews_foodestab_item where estabid = ? and productid = ?"
    getRatingParam = (estabid, productid)
    avg_rating = fetch(getRatingQuery, getRatingParam)[0]
    updateFoodItemRating(avg_rating, estabid, productid)

def addFoodEstabReview(username, password):
    print("*****FOOD ESTABLISHMENT REVIEW*****")
    userid = fetchUserId(username, password)

    #Fetches estab id
    estabid = fetchEstabId()
    if estabid is None:
        print("Establishment not found.")
        return

    #User input
    rating = float(input("Enter rating (1-5): "))
    if(rating < 1 or rating > 5):
        print("Please enter a rating of 1 to 5 only.")
        return
    dateofreview = datetime.datetime.now()
    body = input("Enter review (200 characters): ")
    if len(body) > 200:
        print("Please shorten your review to 200 characters only.")
        return

    query = "insert into user_reviews_foodestab (`userid`, `estabid`, `rating`, `date_of_review`, `body`) values (?, ?, ?, ?, ?)"
    params = (userid, estabid, rating, dateofreview, body)

    #Execute the query
    execute_query(query, params)

    # Updates the average rating of the establishment
    getRatingQuery = "select avg(rating) from user_reviews_foodestab where estabid = ?"
    getRatingParam = (estabid,)
    avg_rating = fetch(getRatingQuery, getRatingParam)[0]
    updateEstabRating(avg_rating, estabid)

def updateFoodItemReview(username, password):
    print("*****EDIT FOOD ITEM REVIEW*****")
    userid = fetchUserId(username, password)

    #Fetches estabid
    estabid = fetchEstabId()
    if estabid is None:
        print("Establishment not found.")
        return

    #Fetch productid
    productid = fetchProductId(estabid)
    if productid is None:
        print("Product not found.")
        return

    query = "select rating, date_of_review, body from user_reviews_foodestab_item where userid = ? and estabid = ? and productid = ?"
    params = (userid, estabid, productid)
    reviews = fetchall(query, params)

    if reviews:
        review_data = [list(review) for review in reviews]

        # Add headers
        headers = ["Review Number", "Rating", "Date of Review", "Body"]

        # Add review number
        for i, _ in enumerate(review_data, start=1):
            review_data[i - 1].insert(0, i)

        print(tabulate(review_data, headers=headers, tablefmt="coquette"))

        review_number = int(input("Enter the review number you want to edit: "))
        if 1 <= review_number <= len(reviews):
            review_to_edit = reviews[review_number - 1]
            rating, date_of_review, body = review_to_edit

            #User inputs
            new_rating = float(input("Enter new rating: "))
            if (rating < 1 or rating > 5): return ("Please enter a rating of 1 to 5 only.")
            new_body = input("Enter new review: ")
            if (len(body) > 200): return ("Please shorten your review to 200 characters only.")

            query = "update user_reviews_foodestab_item set rating = ?, body = ? where date_of_review = ?"
            params = (new_rating, new_body, date_of_review)

            execute_query(query, params)

            # Updates the average rating of the establishment
            getRatingQuery = "select avg(rating) from user_reviews_foodestab_item where estabid = ? and productid = ?"
            getRatingParam = (estabid, productid)
            avg_rating = fetch(getRatingQuery, getRatingParam)[0]
            updateFoodItemRating(avg_rating, estabid, productid)

        else:
            print("Please enter a valid review number.")

    else:
        print("No reviews found for the specified food item.")

#Updates a review on food establishments
def updateFoodEstabReview(username, password):
    print("*****EDIT FOOD ESTABLISHMENT REVIEW*****")
    userid = fetchUserId(username, password)

    # Fetch estabid
    estabid = fetchEstabId()
    if estabid is None:
        print("Establishment not found.")
        return

    query = "select rating, date_of_review, body from user_reviews_foodestab where userid = ? and estabid = ?"
    params = (userid, estabid)
    reviews = fetchall(query, params)

    if reviews:
        review_data = [list(review) for review in reviews]

        #Add headers
        headers = ["Review Number", "Rating", "Date of Review", "Body"]

        #Add review number
        for i, _ in enumerate(review_data, start=1):
            review_data[i-1].insert(0, i)

        print(tabulate(review_data, headers=headers, tablefmt="coquette"))

        review_number = int(input("Enter the review number you want to edit: "))
        if 1 <= review_number <= len(reviews):
            review_to_edit = reviews[review_number - 1]
            rating, date_of_review, body = review_to_edit

            new_rating = float(input("Enter new rating: "))
            if (rating < 1 or rating > 5): return ("Please enter a rating of 1 to 5 only.")
            new_body = input("Enter new review: ")
            if (len(body) > 200): return ("Please shorten your review to 200 characters only.")

            query = "update user_reviews_foodestab set rating = ?, body = ? where date_of_review = ?"
            params = (new_rating, new_body, date_of_review)

            execute_query(query, params)

            # Updates the average rating of the establishment
            getRatingQuery = "select avg(rating) from user_reviews_foodestab where estabid = ?"
            getRatingParam = (estabid,)
            avg_rating = fetch(getRatingQuery, getRatingParam)[0]
            updateEstabRating(avg_rating, estabid)

        else:
            print("Please enter a valid review number.")

    else:
        print("No reviews found for the specified establishment.")

#Deletes a food item review
def deleteFoodReview(username, password):
    print("*****DELETE FOOD ITEM REVIEW*****")
    userid = fetchUserId(username, password)

    #Fetch estab id
    estabid = fetchEstabId()
    if estabid is None:
        print("Establishment not found.")
        return

    # Fetch productid
    productid = fetchProductId(estabid)
    if productid is None:
        print("Product not found.")
        return

    query = "select rating, date_of_review, body from user_reviews_foodestab_item where userid = ? and estabid = ? and productid = ?"
    params = (userid, estabid, productid)
    reviews = fetchall(query, params)

    if reviews:
        review_data = [list(review) for review in reviews]

        # Add headers
        headers = ["Review Number", "Rating", "Date of Review", "Body"]

        # Add review number
        for i, _ in enumerate(review_data, start=1):
            review_data[i - 1].insert(0, i)

        print(tabulate(review_data, headers=headers, tablefmt="coquette"))

        review_number = int(input("Enter the review number you want to delete: "))
        if 1 <= review_number <= len(reviews):
            review_to_delete = reviews[review_number - 1]
            rating, date_of_review, body = review_to_delete

            query = "delete from user_reviews_foodestab_item where estabid = ? and userid = ? and date_of_review = ? and productid = ?"
            params = (estabid, userid, date_of_review, productid)

            confirmation = input("\nAre you sure you want to delete it? (Y/N): ")
            if confirmation.lower() == "y":
                execute_query(query, params)

                # Updates the average rating of the establishment
                getRatingQuery = "select avg(rating) from user_reviews_foodestab_item where estabid = ? and productid = ?"
                getRatingParam = (estabid, productid)
                avg_rating = fetch(getRatingQuery, getRatingParam)[0]
                updateFoodItemRating(avg_rating, estabid, productid)
            elif confirmation.lower() == "n":
                return
            else:
                print("Invalid input.")

        else:
            print("Please enter a valid review number.")

    else:
        print("No reviews found for the specified food item.")


def deleteEstabReview(username, password):
    print("*****DELETE FOOD ESTABLISHMENT REVIEW*****")
    userid = fetchUserId(username, password)

    #Fetch estabid
    estabid = fetchEstabId()
    if estabid is None:
        print("Establishment not found")
        return

    query = "select rating, date_of_review, body from user_reviews_foodestab where userid = ? and estabid = ?"
    params = (userid, estabid)
    reviews = fetchall(query, params)

    if reviews:
        review_data = [list(review) for review in reviews]

        # Add headers
        headers = ["Review Number", "Rating", "Date of Review", "Body"]

        # Add review number
        for i, _ in enumerate(review_data, start=1):
            review_data[i - 1].insert(0, i)

        print(tabulate(review_data, headers=headers, tablefmt="coquette"))

        review_number = int(input("Enter the review number you want to delete: "))
        if 1 <= review_number <= len(reviews):
            review_to_delete = reviews[review_number - 1]
            rating, date_of_review, body = review_to_delete

            query = "delete from user_reviews_foodestab where estabid = ? and userid = ? and date_of_review = ?"
            params = (estabid, userid, date_of_review)

            confirmation = input("\nAre you sure you want to delete it? (Y/N): ")
            if confirmation.lower() == "y":
                execute_query(query, params)

                # Updates the average rating of the establishment
                getRatingQuery = "select avg(rating) from user_reviews_foodestab where estabid = ?"
                getRatingParam = (estabid,)
                avg_rating = fetch(getRatingQuery, getRatingParam)[0]
                updateEstabRating(avg_rating, estabid)
            elif confirmation.lower() == "n":
                return
            else:
                print("Invalid input.")

        else:
            print("Please enter a valid review number.")

    else:
        print("No reviews found for the specified establishment.")

#Fetches the establishment id
def fetchEstabId():
    estabnameinput = input("Enter establishment name: ")
    search_query = "select estabid from food_estab where estabname = ?"
    result = fetch(search_query, (estabnameinput,))
    if result is None:
        return ("Establishment not found.")
    estabid = result[0]
    return estabid

#Fetches the product id
def fetchProductId(estabid):
    productnameinput = input("Enter product name: ")
    search_query = "select productid from food_item where itemname = ? and estabid= ?"
    productid_result = fetch(search_query, (productnameinput, estabid))
    if productid_result is None:
        print("Product not found.")
        return
    productid = productid_result[0]
    return productid

#Updates the rating of the food establishment
def updateEstabRating(newrating, estabid):
    query = "update food_estab set rating = ? where estabid = ?"
    params = (newrating, estabid)
    execute_query(query, params)

#Updates the rating of the food item
def updateFoodItemRating(newrating, estabid, productid):
    query = "update food_item set rating = ? where estabid = ? and productid = ?"
    params = (newrating, estabid, productid)
    execute_query(query, params)

#Fetches the id of the currently logged in user
def fetchUserId(username, password):
    query = "select userid from user where username = ? and password = ?"
    params = (username, password)

    user_id = fetch(query, params)
    return user_id[0]

def fetch(query, params):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def fetchall(query, params):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mariadb.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
