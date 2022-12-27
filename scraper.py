from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd

#create empty lists to add book titles and prices to
titles = []
prices = []
categories = []
urls = []
category_assign = []

#go through the categories and compile a list of urls and category names
main_page = "http://books.toscrape.com/"
page = urlopen(main_page)
html = page.read().decode('utf-8')
soup = bs(html, 'html.parser')
category_div = soup.find('div', class_ = "side_categories")
category_data = category_div.find_all("a")
for cat in category_data:
    if str.strip(cat.text) == "Books":
        pass
    else:
        categories.append(str.strip(cat.text))
        urls.append(str.strip(cat.attrs.get("href")))
#combine urls and categories into a single list
category_looper = list(zip(categories, urls))
#print(category_looper)
#now loop through each page of each category, grabbing prices and titles
for entry in category_looper:
    url = "http://books.toscrape.com/"+entry[1]
    current_page = urlopen(url)
    html = current_page.read().decode("utf-8")
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div')
    #this looks for the div tag and within that, finds the text data for the range of pages of the category
    for div in divs:
        pager = div.find('li', class_ = "current")
        #if pager is equal to None, that means there is only 1 initial page for the category
        if pager == None:
            pass
        #if pager has data then there are multiple pages for that category, the data has been found, and the loop can be broken
        else:
            pager = (pager.text.strip())
            continue
    #these two lines find the tags containing title and price info
    books = soup.find_all('a')
    costs = soup.find_all('p', class_ = "price_color")
    #only one "a" tag has the book title, grab that attribute from the tag, append it to the titles list and break the loop
    for book in books:
        if "title" in book.attrs:
            titles.append(book.attrs.get('title'))
            category_assign.append(entry[0])
            continue
    #price is more simple, there's only one tag with the price data
    for price in costs:
        prices.append(price.text)
    #if pager still has a value of none, that means there was only one initial page and we can move on to the next category by passing
    if pager == None:
        pass
    #if pager does have a value, use its last value (the last page number) to create a range
    else:
        for i in [*range(2, int(pager[-1]) + 1)]:
            #this next line resets the url to a baseline 
            url = url = "http://books.toscrape.com/"+entry[1]
            #index needs to be removed in order to insert a specific page number
            url = url.replace("index.html", "")
            #insert a specific page number beginning with 2 (since we already grabbed the first page of every category)
            url = url+"page-"+str(i)+".html"
            #this print statement checks the url being scraped as the program runs (for debugging purposes)
            print(url)
            #this block is from above, it grabs title and price and assigns the title the category being scraped
            current_page = urlopen(url)
            html = current_page.read().decode("utf-8")
            soup = bs(html, 'html.parser')
            books = soup.find_all('a')
            costs = soup.find_all('p', class_ = "price_color")
            for book in books:
                if "title" in book.attrs:
                    titles.append(book.attrs.get('title'))
                    category_assign.append(entry[0])
                else: 
                    pass
            for price in costs:
                prices.append(price.text)
            

#convert everything to a dataframe
df = pd.DataFrame(list(zip(titles, prices, category_assign)))
#clean up the data by converting prices to floats and giving columns titles
df.rename(columns = {0:"Title",1:"Price",2:"Category"}, inplace = True)
df.Price = df.Price.apply(lambda x: x[1:])
df.Price = df.Price.astype(float)
#check for duplicates
print(df.duplicated(subset = "Title").sum())
#One duplicate title, drop one of the duplicates
df.drop_duplicates(inplace = True)
#double check for duplicates
print(df.duplicated().sum())
#check that df is 1000 entries, the number of books on the website
print(len(df))
#export df to csv
df.to_csv('data.csv', index = False)

### Let's make some graphs ###










