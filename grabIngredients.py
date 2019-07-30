import requests,bs4,time

def bestRecipes():
    url = 'https://www.bestrecipes.com.au/recipes/minestrone-soup-recipe-4/kvd4e98m'

    res = requests.get(url)
    res.raise_for_status()
    soupValue = ('.ingredient-description')
    soup = bs4.BeautifulSoup(res.text)
    ingredientElem = soup.select(soupValue)
    for item in ingredientElem:
        print(item.getText())
        time.sleep(1)

def taste():
    url = 'https://www.taste.com.au/recipes/spaghetti-boscaiola/1398db68-b1e5-4701-93cc-a8357fc53cf0'

    res = requests.get(url)
    res.raise_for_status()
    soupValue = ('.ingredient-description')
    soup = bs4.BeautifulSoup(res.text)
    ingredientElem = soup.select(soupValue)
    for item in ingredientElem:
        print(item.getText())
        time.sleep(1)

def bbcGoodFood():
    url = 'https://www.bbcgoodfood.com/recipes/pasta-salmon-peas'

    res = requests.get(url)
    res.raise_for_status()
    soupValue = ('.ingredients-list_item')
    soup = bs4.BeautifulSoup(res.text)
    ingredientElem = soup.select(soupValue)
    for item in ingredientElem:
        print(item.getText())
        time.sleep(1)

taste()
