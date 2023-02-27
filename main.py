import requests
from bs4 import BeautifulSoup

# שליחת בקשת חיבור לאתר וקליטה של הפלט
FutBin = requests.get('https://www.futbin.com/stc/cheapest', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
bs = BeautifulSoup(FutBin.text, 'html.parser')

# חישוב מחירי פודר
foderPrices = dict()
for player in bs.find_all(class_="col-md-4 col-6 top-stc-players-col p-2 px-0"):
    rating = player.find_next(class_="top-players-stc-title").get_text().split()[0]
    price = player.find_next(class_="price-holder-row").get_text().split()[0]
    if price[-1] == 'K':
        price = int(float(price[:-1]) * 1000)
    elif price[-1] == 'M':
        price = int(float(price[:-1]) * 1000000)
    else:
        price = int(price)
    foderPrices[rating] = price

# קבלת פודרים של המשתמש
foders = input("יש לרשום את הרייטינג של הפודרים שיש לך. נספרים רק פודרים בין 84-91. יש להפריד עם רווח בין המספרים.\n")
arr = foders.split()
fodersSupply = dict()
for i in arr:
    if int(i) in range(84, 91):
        fodersSupply[i] = input(f"כמה פודרים {i} יש לך? ")
