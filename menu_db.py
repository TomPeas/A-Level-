import pickle
import sql

with open('menu_details', 'rb') as infile:
    menu = pickle.load(infile)
    menu_prices = pickle.load(infile)

class Database:
    def __init__(self, db_name):
        with sql.connect(db_name) as self.connect:
            self.cursor = self.connect.cursor()
            self.connect.execute('PRAGMA foreign_keys = on')

    def create_table(self, sql):
        self.cursor.excecute(sql)
        self.connect.commit()

    def update_table(self, sql):
        self.cursor.excecute(sql)
        self.connect.commit()

tbl_dishes_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Dishes ( DishID text PRIMARY KEY, Dish text NOT NULL, Section text NOT NULL ) '''
tbl_prices_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Prices ( PriceID text PRIMARY KEY, Price real NOT NULL ) '''
tbl_menu_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Menu (ItemID text PRIMARY KEY,
DishID text NOT NULL,
PriceID text NOT NULL,
    FOREIGN KEY (DishID) REFERENCES tbl_dishes_sql(DishID)
    FOREIGN KEY (PriceID) REFERENCES tbl_prices_sql(PriceID)
    '''
tables = [tbl_dishes_sql, tbl_prices_sql, tbl_menu_sql]
db = Database('Santa_Database.db')
db.create_table(tbl_dishes_sql)

