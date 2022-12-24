#this comment is to test initial GitHub commit
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd

#save the website url
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
#open the url
page = urlopen(url)
#read the website html
html = page.read().decode('utf-8')
#create a soup object
soup = bs(html, 'html.parser')
#check the html code
print(soup.prettify())