import sqlite3

class Database:
    def __init__(self, db_name):
        with sqlite3.connect(db_name) as self.connect:
            self.cursor = self.connect.cursor()
            self.connect.execute('PRAGMA foreign_keys = on')

    def create_table(self, sql): # Function to create a new table
        self.cursor.execute(sql)
        self.connect.commit()

    def update_table(self, sql, data): # Function to update a new table
        self.cursor.execute(sql, data)
        self.connect.commit()

    def find_password(self, data): # Function to find a password based of a specific user name
        self.cursor.execute(''' SELECT Password FROM Login_Info WHERE Username = ? ''', (data,))
        return self.cursor.fetchall()

    def find_username(self, data): # Function to find a username matching user data
        s_data = "('" + str(data) + "',)"  # When the the username is read from the database it is in this format
        self.cursor.execute(''' SELECT Username FROM Login_Info ''')
        stored_usernames = [str(each) for each in self.cursor.fetchall()]
        if s_data in stored_usernames:
            return True
        return False

    def find_all(self): # finds all instances of a dish
        self.cursor.execute(''' SELECT Dish FROM Santa_Dishes ''')
        return self.cursor.fetchall()

    def find_all_price(self):
        self.cursor.execute(''' SELECT Price FROM Santa_Prices ''')
        return self.cursor.fetchall()

    def find_all_section(self):
        self.cursor.execute(''' SELECT Section FROM Santa_Dishes ''')
        return self.cursor.fetchall()

    def find_items(self, data): # finds a specific instance of a dish
        self.cursor.execute(''' SELECT Dish FROM Santa_Dishes WHERE Section = ? ''', (data,))
        return self.cursor.fetchall()

    def find_dish_id(self, data):
        self.cursor.execute(''' SELECT DishID FROM Santa_Dishes WHERE Dish = ?''', (data,))
        return self.cursor.fetchall()

    def find_menu_price_id(self, data):
        self.cursor.execute(''' SELECT PriceID FROM Santa_Menu WHERE DishID = ?''', (data,))
        return self.cursor.fetchall()

    def find_price(self, data):
        self.cursor.execute(''' SELECT Price FROM Santa_Prices WHERE PriceID = ?''', (data,))
        return self.cursor.fetchall()