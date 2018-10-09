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


