#this comment is to test initial GitHub commit
from bs4 import BeautifulSoup as bs
import lxml
import requests
import pandas as pd

#grab the url for the webpage
r = requests.get('https://www.sciencedaily.com/releases/2022/12/221221135529.htm')

#create a soup object for parsing
soup = bs(r.content, 'lxml')

#look for the abstract id
abstract = soup.find(id = "abstract")
#check for data
print(abstract)