import urllib
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

#organises the dishes into the menu catergories
def menu_split(start, end):
    items = []
    for i in range(start, end):
        items.append(dishes[i])
    return items
starters = menu_split(0, 22)
soups = menu_split(22, 30)
poultry_dishes = menu_split(30, 45)
beef_dishes = menu_split(45, 56)
pork_lamb_dishes = menu_split(56, 67)
curry_dishes = menu_split(67, 73)
seafood_dishes = menu_split(73, 94)
vegertarian_dishes = menu_split(94, 105)
rice_noodel_dishes = menu_split(105, 121)
extra_dishes = menu_split(121, 124)

#organises prices into corresponding menu catergories
