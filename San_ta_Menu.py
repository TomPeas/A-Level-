import urllib.request
from bs4 import BeautifulSoup
import pickle

san_url = 'http://www.san-restaurant.com/san-finest-chinese-cuisine-take-away-menu.html'
the_page = urllib.request.urlopen(san_url)
soup = BeautifulSoup(the_page,'html.parser')
counter = 0
html_headers =  soup.findAll('h3')
headers = []
for each in html_headers[2:-3]:
    headers.append(each.text)
html_dishes_unrefined = soup.findAll('td')
html_dishes_refined = []
for each in html_dishes_unrefined[32:-24]:
    html_dishes_refined.append(each)

dishes = []
for each in html_dishes_refined[::3]: #finds the item names
    dishes.append(each.text)
while '\xa0' in dishes: #removes a un-needed string constantly repeated
    dishes.remove('\xa0')

prices = []
for each in html_dishes_refined[1::3]:#find the item prices
    prices.append(each.text)
while 'half £17.00' in prices: #removes an unessential item
    prices.remove('half £17.00')
prices[30] = '£5.50'

#organises items from a large list into a smaller list
def split(list,start, end):
    items = []
    for i in range(start, end):
        items.append(list[i])
    return items

#uses split function to divide up the menu
starters = split(dishes, 0, 22)
soups = split(dishes, 22, 30)
poultry_dishes = split(dishes, 30, 45)
beef_dishes = split(dishes, 45, 56)
pork_lamb_dishes = split(dishes, 56, 67)
curry_dishes = split(dishes, 67, 73)
seafood_dishes = split(dishes, 73, 94)
vegertarian_dishes = split(dishes, 94, 105)
rice_noodel_dishes = split(dishes, 105, 121)
extra_dishes = split(dishes, 121, 124)
menu = [starters, soups, poultry_dishes, beef_dishes, pork_lamb_dishes, curry_dishes, seafood_dishes, vegertarian_dishes, rice_noodel_dishes, extra_dishes]

#organises prices into corresponding menu catergories
starters_prices = split(prices, 0, 22)
soups_prices = split(prices, 22, 30)
poultry_dishes_prices = split(prices, 30, 45)
beef_dishes_prices = split(prices, 45, 56)
pork_lamb_dishes_prices = split(prices, 56, 67)
curry_dishes_prices = split(prices, 67, 73)
seafood_dishes_prices = split(prices, 73, 94)
vegertarian_dishes_prices = split(prices, 94, 105)
rice_noodel_dishes_prices = split(prices, 105, 121)
extra_dishes_prices = split(prices, 121, 124)
menu_prices = [starters_prices, soups_prices, poultry_dishes_prices, beef_dishes_prices, pork_lamb_dishes_prices, curry_dishes_prices, seafood_dishes_prices, vegertarian_dishes_prices, rice_noodel_dishes_prices, extra_dishes_prices]

with open("menu_details", 'wb') as outfile:
    pickle.dump(menu, outfile)
    pickle.dump(menu_prices, outfile)