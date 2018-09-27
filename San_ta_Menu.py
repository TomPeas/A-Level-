import urllib
import urllib.request
from bs4 import BeautifulSoup

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

dish_numbers = []
for each in html_dishes_refined[2::3]: # finds the item numbers
    dish_numbers.append(each.text)

dishes = []
for each in html_dishes_refined[::3]: #finds the item names
    dishes.append(each.text)
while '\xa0' in dishes: #removes a un-needed string constantly repeated
    dishes.remove('\xa0')

prices = []
for each in html_dishes_refined[1::3]:#find the item prices
    str(each).strip()
    prices.append(each.text)
while 'half £17.00' in prices: #removes an unessential item
    prices.remove('half £17.00')


for i in range(len(dishes)):
    print('{0} {1} {2}'.format(dish_numbers[i-1], dishes[i-1], prices[i-1]))
