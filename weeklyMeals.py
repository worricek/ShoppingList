#! /usr/bin/python3

import random,smtplib,datetime,csv,sys,time,requests,bs4
from gmailConnection import sendEmail


''' Randomly select 1 meal from Fish and Veggie and 5 meals from standard. 
    After selection the meal should be placed in last weeks meal file. Every time you run
    the 1st week gets moved to the 2nd week and 2nd week back to source meals. 
'''
#TODO Add descriptions to each Aisle
#TODO Cross reference the ingredients with the decided items to avoid double ups.
'''
Use cases:
- The item is already on the default list and therefore we dont need it. eg Lettuce, Sauce, mayo etc.
How? 
Check if the ingredient is on the default shopping list and dont write it to the list if it is. 

- The item is already on the default list however we therefore need more of it. eg Tuna for Tuna casserole.
How? 
- The item is not on the default list and has come through as an ingredient more than once, eg Rice and Cream.
'''
#TODO Why are there brackets and quotes everywhere?
#TODO Add the aisle descriptions to the shopping list.
#TODO Can we get the aisle from web?
#TODO Map the ingredient from a meal to the aisle its in and add it to that section of the list.
#DONE Add the ingredients to the shopping list in their aisle.
#DONE Remove the 'randoms' from the default shopping list. eg eschallots
#DONE Tidy up and number the list
#DONE Email the menu
#DONE Tidy up with functions (DONE)
#DONE Update the default shopping list (DONE)
#DONE Update the meal list with ingredients (DONE)
#DONE No later than Wednesday afternoon Get the ingredients from the website and update ingredients list (DONE)
#DONE Before Friday Get the final shopping list (DONE)
#TODO Categorise the days and the meals
#DONE Generate shopping list from meal ingredients
#DONE Add generic items to the shopping list
#DONE Get ingredients from the webpages and add to the list
#DONE Add a menu to the progam and create functions.
#TODO set this up for database access
#TODO Set this up with a GUI
#TODO Enable search for meal ideas based on ingredients.
#TODO Tidy up with functions
#TODO Order online

def setWeeklyMealPref_1():
#TODO Write the pref to a file and allow the user to see the current pref first. Then allow them to set items.
#TODO Match the preference with the meal.

    dailyPreference={'monday':'','tuesday':'','wednesday':'','thursday':'','friday':'','saturday':'','sunday':''}
    while True:
        if input('\nSet the daily preference (easy/medium/hard) ? > ') == 'y':
            with open('dailyPreference.csv','w',newline='') as prefFile:
                prefWriter = csv.writer(prefFile)
                for k,v in dailyPreference.items():
                    preference=input(k + ' preference ? > ')
                    if preference == '':
                        print('Keeping the same preference for this day!')
                        continue
                    elif preference not in ('easy','medium','hard'):
                        print('The choices are easy,medium or hard ... ')
                        break

                    dailyPreference[k]=preference
                    combined = [k,preference]
                    prefWriter.writerow(combined)
        else:
            break
    for k,v in dailyPreference.items():
        print(k,v)

def setDefaultShop_2():
    with open('shoppingGenList.csv','r') as shopFile, open('defaultGroceries.csv','w',newline='') as defaultGroceries:
        shopReader = csv.reader(shopFile)
        shopList = list(shopReader)
        defaultGroceryWriter = csv.writer(defaultGroceries)

        for aisle in range(0,len(shopList)):
            defaultGroceryWriter.writerow(['\nAisle ' + str(shopList[aisle]).split(',')[0] + str(shopList[aisle]).split(',')[1] + '\n'])
            for item in range(2,len(shopList[aisle])):
                wanted = input(shopList[aisle][item].ljust(30) + "     Add 'y' or 'enter' to skip? ")
                if wanted == 'y':
                    defaultGroceryWriter.writerow([str(shopList[aisle][item])])
                else:
                    continue

def getWeeklyMenu_3():

    def generateShoppingList():
        with open('defaultGroceries.csv','r') as itemFile, open('lastMeals.csv','r') as mealFile, \
            open('finalShoppingList.csv','w',newline='') as listFile:
            itemReader = csv.reader(itemFile)
            mealReader = csv.reader(mealFile)
            listWriter = csv.writer(listFile)
            counter = 0
            for meal in mealReader:
                #print(meal)
                for ingredient in range(1, len(meal)):
                    #print(meal[ingredient])
                    if 'http' in meal[ingredient]:
                        url = meal[ingredient]
                        res = requests.get(url)
                        res.raise_for_status()
                        soupValue = ('.ingredient-description')
                        soup = bs4.BeautifulSoup(res.text)
                        ingredientElem = soup.select(soupValue)
                        for item in ingredientElem:
                            listWriter.writerow([item.getText()])
                    else:
                        listWriter.writerow([meal[ingredient]])
                #print('Ingredients for ' + meal[0] + ' are ' + meal[1])
                #listWriter.writerow([meal])
                counter+=1
            for item in itemReader:
                listWriter.writerow(item)
    weeklyMenu=[]
    with open('lastMeals.csv','r') as lastMeals:
        lastMealContents=lastMeals.readlines()
        print('\nLast weeks meals were ... \n')
        for h in range(0,len(lastMealContents)):
            print(str(h)+'   '+ lastMealContents[h])
    with open('mealList.csv', 'r') as mealFile:
        mealContents=mealFile.readlines()
    with open('lastMeals.csv','w') as lastMeals:
        index=0
        while True:
            meals=''
            while True:
                mealRandom=random.randint(0, len(mealContents)-1)
                if mealContents[mealRandom] in weeklyMenu or mealContents[mealRandom] in lastMealContents:
                    continue
                weeklyMenu.append(mealContents[mealRandom])
                index+=1
                if index==7:
                    print ('This weeks Meals are ...\n')
                    for i in range(0,len(weeklyMenu)):
                        print(str(i)+'   '+ str(weeklyMenu[i]).split(',')[0])
                        meals+=str(weeklyMenu[i]).split(',')[0] +'\n'
                    break
            if input('\nChange em up? (y/n):') == 'y':
                mealRandom=input('\nWhich meal would you like to change fancy pants? :')
                del weeklyMenu[int(mealRandom)]
                index-=1
                continue
            else:
                break
        print ('The final meal list is ...\n')
        for j in range(0,len(weeklyMenu)):
            print(str(j)+'   '+str(weeklyMenu[j]).split(',')[0])
            lastMeals.write(weeklyMenu[j])
    print('\nGenerating final shopping list ...\n')
    time.sleep(5)
    generateShoppingList()
    print('Final shopping list completed. Email it or print finalshoppinglist.csv')
    #with open('finalShoppingList.csv','r') as listFile:
    finalList = [line.rstrip('\n') for line in open('finalShoppingList.csv')]
    messageBody = 'WEEKLY MENU \n\n'
    messageBody += meals + '\n\n'
    messageBody += 'SHOPPING LIST \n\n'
    for item in range(0,len(finalList)):
        messageBody+=str(finalList[item])+'\n'
    #print(messageBody)

    #print(messageBody)#listReader = csv.reader(listFile)
    #finalList = list(listReader)
    #lineList = [line.rstrip('\n') for line in open(fileName)]
    #finalString = ('\n'.join(finalList))
    messageSubject='Subject: Weekly meals for week ' + str(datetime.date.today()) + '\n'
    #messageBody=finalString
    message = '{}\n\n{}'.format(messageSubject,messageBody)
    #print('Final Shopping List ... ')
    #print(str(message))
    #print(messageBody)
    sendEmail('smtp.gmail.com',587,'dworrall','g0bst0pper04','dworrall@gmail.com','worricek@yahoo.com.au',messageSubject+messageBody)

'''                generateList = input('\nAre you ready to generate the final shopping list (y/n)?')
                if generateList == 'y':
                    generateShoppingList()
                    break
                elif generateList == 'n':
                    break
                else:
                    print("\nEnter either 'y' or 'n'\n")
                    continue
'''

def modifyMealList_4():
    print('\nThis function is in the pipeline ...\n')

def setEmailAddress_5():
    print('\nThis function is in the pipeline ... \n')

while True:
    print('\nShopping List ... Whats your poison ? \n')
    print('1 ... Set your weekly meal preference')
    print('2 ... Set your weekly default shopping list preference')
    print('3 ... Get your weekly menu and generate shopping list')
    #print('4 ... Generate this weeks shopping list')
    print('4 ... Get meal ideas and modify the meals in the meal list')
    print('5 ... Change the linked email address\n')
    print('9 ... Exit\n\n')
    try:
        selection = int(input('Enter your options > '))
        if selection == 1:
            setWeeklyMealPref_1()
        elif selection == 2:
            setDefaultShop_2()
        elif selection == 3:
            selection = input("\nBefore selecting meals, are you happy with your default grocery list 'y' or any other key to exit ")
            if selection != 'y':
                continue
            getWeeklyMenu_3()
        #elif selection == 4:
        #    generateShoppingList_4()
            #else:
             #   print('You need to confirm the weekly menu first ... Back to main menu.\n')
        elif selection == 4:
            modifyMealList_4()
        elif selection == 5:
            setEmailAddress_5()
        elif selection == 9:
            print('\nExiting ... \n\n')
            sys.exit()
        else:
            print('\nMust be a number between 1 and 5, try again!\n')

    except ValueError:
        print('\nMust be a number. try again!\n')
