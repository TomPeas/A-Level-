import urllib
import urllib.request
from bs4 import BeautifulSoup

san_url = 'http://www.san-restaurant.com/main-menu.html'
the_page = urllib.request.urlopen(san_url)
soup = BeautifulSoup(the_page,'html.parser')

'''
print(soup.title.text)
for each in soup.findAll('td'):
    print(each.text)

for each in soup.findAll('h3'):
    print(each.text)
'''

html_headers = soup.findAll('h3')[1:-3] #gets all but the first and last 3 entries which I don't need
headers = []
for each in html_headers:
    headers.append(each.text)
print(headers)

counter = 0
html_dishes = soup.findAll('td')
dishes = []
for each in html_dishes:
    dishes.append(each.text)
while '\xa0' in dishes: #removes a un-needed string constantly repeated
    dishes.remove('\xa0')
for each in dishes[73:-18]:




