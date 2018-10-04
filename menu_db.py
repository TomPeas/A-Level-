import pickle
import sql

with open('menu_details', 'rb') as infile:
    menu = pickle.load(infile)
    menu_prices = pickle.load(infile)
