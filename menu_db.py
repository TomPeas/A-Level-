import pickle
from database_base import Database

tbl_dishes_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Dishes ( DishID text PRIMARY KEY, Dish text NOT NULL, Section text NOT NULL ) '''
tbl_prices_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Prices ( PriceID text PRIMARY KEY, Price real NOT NULL, Section text NOT NUll ) '''
tbl_menu_sql = ''' CREATE TABLE IF NOT EXISTS Santa_Menu (
ItemID text PRIMARY KEY,
DishID text NOT NULL,
PriceID text NOT NULL,
    FOREIGN KEY (DishID) REFERENCES Santa_Dishes(DishID),
    FOREIGN KEY (PriceID) REFERENCES Santa_Prices(PriceID)) '''

db = Database('Santa_Database.db')
db.create_table(tbl_dishes_sql)
db.create_table(tbl_prices_sql)
db.create_table(tbl_menu_sql)

insert_dish_sql = ''' INSERT INTO Santa_Dishes (DishID, Dish, Section) values (?,?,?)'''
insert_price_sql = ''' INSERT INTO Santa_Prices (PriceID, Price, Section) values (?,?,?)'''
insert_menu_sql = ''' INSERT INTO Santa_Menu (ItemID, DishID, PriceID) values (?,?,?)'''

def add_item(sql, id, name, type):
    id = id
    name = name
    type = type
    data = (id, name, type)
    db.update_table(sql, data)

def add_link(sql, DishID, PriceID):
    num = 000
    for i in range(len(DishID)):
        menuID = 'M' + str(num)
        dishID = DishID[i]
        priceID = PriceID[i]
        data = (menuID, dishID, priceID)
        db.update_table(sql, data)
        num += 1

with open('menu_details', 'rb') as infile:
    menu = pickle.load(infile)
    prices = pickle.load(infile)

# add all the starters
def write_database(catergory, sql, idenl):
    types = ['starters', 'soups', 'poultry_dishes', 'beef_dishes', 'pork_lamb_dishes', 'curry_dishes', 'seafood_dishes', 'vegertarian_dishes', 'rice_noodel_dishes', 'extra_dishes']
    pos = 0
    num = 000
    section = types[pos]
    ideez= []
    for each in catergory:
        for index in each:
            d_id = idenl + str(num)
            add_item(sql, d_id, index, section)
            num += 1
            ideez.append(d_id)
        pos += 1
        try:
            section = types[pos]
        except:
            break
    return ideez

DishIDs = write_database(menu, insert_dish_sql, 'D')
PriceIDs = write_database(prices, insert_price_sql, 'P')
add_link(insert_menu_sql, DishIDs, PriceIDs)