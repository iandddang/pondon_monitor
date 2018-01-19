from bs4 import BeautifulSoup
import requests

def main():
    ## getting html from pondonurl
    pondonURL = 'http://www.pondonstore.com/list.php?ctg=17'
    request = requests.get(pondonURL)

    itemArray = []
    soup = BeautifulSoup(request.text, "lxml")

    getItems(soup, itemArray)
    # for entries in itemdict:
    for Item in itemArray:
        print(Item.name + " " + Item.price + " " + Item.sizes)

def getItems(soup, itemArray):
    # rows = soup.find_all('div', class_='list_item_desc')
    rows = soup.find_all('a', class_='list_items')
    for row in rows:
        if row.contents[7].span.contents[0] != "SOLD OUT":
            # name of item
            name = row.contents[7].contents[3]
            #price of item
            value = row.contents[7].span.contents[0]
            value = value.replace("-","")
            value = value.strip()
            #sizes available
            size = row.contents[7].contents[6].contents[0]

            #link to item
            link = row['href']

            #picture link
            pictureLink = row.img['src']
            pictureLink = 'http://www.pondonstore.com' + pictureLink[1:]
            print(pictureLink)

            newItem = Item(name, value, size, link, pictureLink)
            itemArray.append(newItem)


# object to hold all needed item data
class Item:
    def __init__(self, name, price, sizes, link, picURL):
        self.name = name
        self.price = price
        self.sizes = sizes
        self.link = link
        self.picURL = picURL

if __name__ == "__main__":
    main()
