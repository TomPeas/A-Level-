import pickle
import sqlite3

class Database:
    def __init__(self, db_name):
        with sqlite3.connect(db_name) as self.connect:
            self.cursor = self.connect.cursor()
            self.connect.execute('PRAGMA foreign_keys = on')

    def create_table(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def update_table(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

tbl_dishes_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Dishes ( DishID text PRIMARY KEY, Dish text NOT NULL, Section text NOT NULL ) '''
tbl_prices_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Prices ( PriceID text PRIMARY KEY, Price real NOT NULL ) '''
tbl_menu_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Menu (ItemID text PRIMARY KEY,
DishID text NOT NULL,
PriceID text NOT NULL,
    FOREIGN KEY (DishID) REFERENCES tbl_dishes_sql(DishID),
    FOREIGN KEY (PriceID) REFERENCES tbl_prices_sqL(PriceID)) '''

db = Database('Santa_Database.db')
db.create_table(tbl_dishes_sql)
db.create_table(tbl_prices_sql)
db.create_table(tbl_menu_sql)

insert_dish_sql = ''' INSERT INTO Santa_Dishes (DishID, Dish, Section) values (?,?,?)'''
insert_price_sql = ''' INSERT INTO Santa_Prices (PriceID, Price) values (?,?)'''

def add_item(sql, id, name, type):
    ID = id
    Name = name
    Type = type
    data = (ID, name)
    db.update_table(sql, data)

with open('menu_details', 'rb') as infile:#
    starters = pickle.load(infile)
    soups = pickle.load(infile)
    poultry_dishes = pickle.load(infile)
    beef_dishes = pickle.load(infile)
    starters = pickle.load(infile)-=[[-56]]
    starters = pickle.load(infile)
    starters = pickle.load(infile)
    starters = pickle.load(infile)
    starters = pickle.load(infile)
    starters = pickle.load(infile)



