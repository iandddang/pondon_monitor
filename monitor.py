from bs4 import BeautifulSoup
from settings import config
import requests

# global dictionary of monitor file that holds all the goodies
itemDict = {}

def check(pondonURL):
    print("CHECK START!")
    ## getting html from pondonurl
    request = requests.get(pondonURL)
    soup = BeautifulSoup(request.text, "lxml")

    getItems(soup, pondonURL)
    # saveItems()
    print("Check end.")

# this function is exactly the same as getItems except it updates values
# will return a string for discord to print
def update(pondonURL):
    global itemDict
    
    request = requests.get(pondonURL)
    soup = BeautifulSoup(request.text, "lxml")

    # uses base URL to get max page num
    pages = getPageNumbers(soup)

    # looping through each page of the base url and adding its items
    for pagenum in range(1,pages+1):

        request = requests.get(pondonURL + "&page=" + str(pagenum))

        #only recreate soup object if it is not at page 1
        if(pagenum > 1):
            soup = BeautifulSoup(request.text, "lxml")

        rows = soup.find_all('a', class_='list_items')

        # will check if item is already in dictionary and do stuff according to that
        for row in rows:
            # name of item
            name = row.contents[7].contents[3]

            # when sold out indices change
            if str(name) == "<br/>":
                name = row.contents[7].contents[2]

            # no apostrophes and weirdo charcters for python
            name = name.encode('ascii',errors='ignore').decode()

            #price of item
            value = row.contents[7].span.contents[0]
            value = value.replace("-","")
            value = value.strip()

            #sizes available
            sizes = row.contents[7].contents[-2].contents[0]
            sizes = sizes.strip()

            #link to item
            link = row['href']

            #picture link
            pictureURL = row.img['src']
            pictureURL = 'http://www.pondonstore.com' + pictureURL[1:]



            messageSent = ""

            # case in which current item is already in the dictionary
            if name in itemDict:
                if(itemDict[name].sizes == "SOLD OUT" and sizes != "SOLD OUT"):
                    messageSent = "RESTOCKED" + " " + name + " old size:"
                    messageSent += itemDict[name].sizes + " new size:" + sizes
                    # item has been restocked so update
                    itemDict[name].sizes = sizes
                    yield messageSent
                else:
                    # updates size regardless of event
                    itemDict[name].sizes = sizes
            else:
                # this is a new item so add it!
                messageSent = "New item has been added: " + name
                newItem = Item(name, value, sizes, link, pictureURL)
                itemDict[name] = newItem
                yield messageSent

def saveItems():
    # clears text file before writing
    open('items.txt','w').close()

    # writes all objects
    with open("items.txt", "w") as output:
        for name in itemDict:
            itemString = itemDict[name].name+"\t"+itemDict[name].price+"\t"
            itemString += itemDict[name].sizes+"\t"+itemDict[name].link+"\t"
            itemString += itemDict[name].picURL
            output.write(itemString+"\n")

def getPageNumbers(soup):
    rows = soup.find_all('div', class_='item_list_page')
    # finds maximum amount of pages thru html
    # .string pulls the content inside the tags
    pages = int(rows[0].contents[-3].string)
    return pages

def getItems(soup, baseURL):
    # uses base URL to get max page num
    pages = getPageNumbers(soup)

    # looping through each page of the base url and adding its items
    for pagenum in range(1,pages+1):

        request = requests.get(baseURL + "&page=" + str(pagenum))

        #only recreate soup object if it is not at page 1
        if(pagenum > 1):
            soup = BeautifulSoup(request.text, "lxml")

        rows = soup.find_all('a', class_='list_items')

        # will add all items regardless if sold out or not
        # this is useful for next iterations where it will check if items are sold out or not
        for row in rows:
            # name of item
            name = row.contents[7].contents[3]

            # when sold out indices change
            if str(name) == "<br/>":
                name = row.contents[7].contents[2]

            # no apostrophes and weirdo charcters for python
            name = name.encode('ascii',errors='ignore').decode()

            #price of item
            value = row.contents[7].span.contents[0]
            value = value.replace("-","")
            value = value.strip()

            #sizes available
            sizes = row.contents[7].contents[-2].contents[0]
            sizes = sizes.strip()

            #link to item
            link = row['href']

            #picture link
            pictureURL = row.img['src']
            pictureURL = 'http://www.pondonstore.com' + pictureURL[1:]

            newItem = Item(name, value, sizes, link, pictureURL)
            itemDict[name] = newItem



class Item:
    def __init__(self, name, price, sizes, link, picURL):
        self.name = name
        self.price = price
        self.sizes = sizes
        self.link = link
        self.picURL = picURL

if __name__ == "__main__":
    check(config.baseURL)
