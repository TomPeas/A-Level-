import urllib
import urllib.request
from bs4 import BeautifulSoup

san_url = 'http://www.san-restaurant.com/san-finest-chinese-cuisine-take-away-menu.html'
the_page = urllib.request.urlopen(san_url)
soup = BeautifulSoup(the_page,'html.parser')

html_headers =  soup.findAll('h3')
headers = []
for each in html_headers[2:-3]:
    headers.append(each.text)

<<<<<<< HEAD
html_dishes =  soup.findAll('td')
=======
html_dishes = []
for each in soup.findAll("td"):
    each.append(html_dishes.text)
print(html_dishes)
>>>>>>> bfb5abd2da3da18ba84e6ace0499357f24403847
