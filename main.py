import requests
from bs4 import BeautifulSoup

FutBin = requests.get('https://www.futbin.com/stc/cheapest', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
bs = BeautifulSoup(FutBin.text, 'html.parser')

players = dict()
for player in bs.find_all(class_="col-md-4 col-6 top-stc-players-col p-2 px-0"):
    players[player.find_next(class_="top-players-stc-title").get_text().split()[0]] = player.find_next(class_="price-holder-row").get_text().split()[0]
print(players)

foderPrice = {}

foders = input("יש לרשום את הרייטינג של הפודרים שיש לך. נספרים רק פודרים בין 84-91. יש להפריד עם רווח בין המספרים.\n")
arr = foders.split()
fodersSupply = dict()
for i in arr:
    if int(i) in range(84, 91):
        fodersSupply[i] = input(f"כמה פודרים {i} יש לך? ")

print(fodersSupply)


