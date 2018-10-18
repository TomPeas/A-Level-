import pickle
import sql

with open('menu_details', 'rb') as infile:
    menu = pickle.load(infile)
    menu_prices = pickle.load(infile)


class Database:
    def __init__(self, db_name):
        with sql.connect(db_name) as self.connect:
            self.cursor = self.connect.cursor()

    def create_table(self, sql):
        self.cursor.excecute(sql)
        self.connect.commit()

    def update_table(self, sql):
        self.cursor.excecute(sql)
        self.connect.commit()

create_dishes_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Dishes ( DishID text PRIMARY KEY, Dish text NOT NULL, Section text NOT NULL ) '''
create_prices_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Prices ( PriceID text PRIMARY KEY, Price real NOT NULL ) '''
create_menu_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Menu (ItemID text PRIMARY KEY, DishID text FOREIGN KEY, PriceID text FOREIGN KEY ) '''


