Critique Food Establishment Information System


Developers:
Bañares, Naddine Rose
Diares, Ken Vincent
Francisco, Clyde
Quejada, Roche
CMSC 127 ST6L


Specifications:
Critiqué is a simplified version of a food and establishment review system. The application allows users to create reviews for a food item or establishment, as well as update or delete them. Users can also generate view reports or search calls to easily access the existing information on all or a specific food item or establishment, as well as filter these results according to varying criteria. The application was created using Python, integrating MySQL and a MariaDB database.


The application recognizes two categories of users: administrator and customers. The administrator has full access to all privileges to the database and therefore functions, while the customer is restricted from modifying (updating and deleting) establishments, food products, food types, and other customers’ reviews; they can only add, update, and delete their own reviews. The feature for generating view reports is accessible by both the administrator and customers.


How to use:
To use the food review system, the following steps should be taken:
1. Unzip the Bañares_Diares_Francisco_Quejada_ST6L_application.zip file which contains a Python file critique.py containing the main program, an sql file 127projdb.sql containing dummy data, and this READme file containing the instructions to run the program.
2. Make sure that both Python and mariadb are installed on your device. You may download the latest version of Python via https://www.python.org/downloads/ and MariaDB via https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.4.2.
3. Open the critique.py file using your code editor. Change the password ‘password’ on LINE 14 to your password on mariadb and save the file. Alternatively, you can also run mysql -u root -p on your terminal and use the password: 123123
4. The application uses a dummy database 127projdb. If you wish to use your own, change the ‘database’ to the name of your database: database = “<database name>”. Make sure to save the file.
5. Go to a terminal and cd to the directory where you saved the python and sql files (it should originally be in the unzipped folder if no changes were made). Run the python file by typing “python critique.py” and pressing enter on the terminal. You can now explore the application and its specifications.
