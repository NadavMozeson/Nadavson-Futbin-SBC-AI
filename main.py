import itertools
import requests
from bs4 import BeautifulSoup

# רשימה של כל הרייטינגים של הפודרים
foderRatings = list(range(81, 92))

# שליחת בקשת חיבור לאתר וקליטה של הפלט
FutBin = requests.get('https://www.futbin.com/stc/cheapest', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
bs = BeautifulSoup(FutBin.text, 'html.parser')

# חישוב מחירי פודר
foderPrices = dict()
for player in bs.find_all(class_="col-md-4 col-6 top-stc-players-col p-2 px-0"):
    rating = int(player.find_next(class_="top-players-stc-title").get_text().split()[0])
    if rating in foderRatings:
        price = player.find_next(class_="price-holder-row").get_text().split()[0]
        if price[-1] == 'K':
            price = int(float(price[:-1]) * 1000)
        elif price[-1] == 'M':
            price = int(float(price[:-1]) * 1000000)
        else:
            price = int(price)
        foderPrices[rating] = price

# function to get all possible combinations of cards
def get_card_combinations(cards, n):
    return list(itertools.combinations_with_replacement(foderRatings, n))


# function to get the total price of a list of cards
def calculate_price(combo, user_cards):
    sum = 0
    count = dict()
    for x in foderRatings:
        count[x] = 0
    for x in user_cards:
        count[x] += 1
    for i in combo:
        if count[i] > 0:
            count[i] -= 1
        else:
            sum += foderPrices[i]
    return sum

def calculate_team_rating(player_ratings):
    team_total = sum(player_ratings)
    average_rating = team_total / 11
    team_total += sum([(rating - average_rating) for rating in player_ratings if rating > average_rating])
    return round(team_total) // 11

# function to find the cheapest combination to reach a specific average
def find_cheapest_combination(cards, target_average):
    card_combinations = get_card_combinations(foderRatings, 11)

    min_price = float('inf')
    min_price_combination = None

    for combo in card_combinations:
        if calculate_team_rating(combo) >= target_average:
            temp = calculate_price(combo, cards)
            if temp < min_price:
                min_price_combination = combo
                min_price = temp

    return min_price_combination

# קבלת פודרים של המשתמש
foders = input("יש לרשום את הרייטינג של הפודרים שיש לך. נספרים רק פודרים בין 84-91. יש להפריד עם רווח בין המספרים.\n")
arr = foders.split()
fodersSupply = dict()
for i in arr:
    if int(i) in foderRatings:
        fodersSupply[i] = input(f"כמה פודרים {i} יש לך? ")



# example usage
user_cards = []
for x in fodersSupply.keys():
    while int(fodersSupply[x]) > 0:
        user_cards.append(int(x))
        fodersSupply[x] = int(fodersSupply[x]) - 1
target_average = int(input("איזה רייטינג אתה מעוניין שיהיה לקבוצה?\n"))

# find the cheapest combination to reach the target average
cheapest_combination = find_cheapest_combination(user_cards, target_average)
amount = dict()
for x in cheapest_combination:
    if x in amount.keys():
        amount[x] += 1
    else:
        amount[x] = 1

amount_keys = list(amount.keys())
amount_keys.sort()
for i in amount_keys:
    print(f"{i} x{amount[i]}")
