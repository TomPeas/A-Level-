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

for each in soup.findAll('h3' and 'td'):
    print(each)

