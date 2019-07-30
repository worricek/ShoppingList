import csv

with open('shoppingGenList.csv','r') as shopFile, open('defaultGroceries.csv','w',newline='') as defaultGroceries:
    shopReader = csv.reader(shopFile)
    shopList = list(shopReader)
    defaultGroceryWriter = csv.writer(defaultGroceries)

    for aisle in range(0,len(shopList)):
        defaultGroceryWriter.writerow(['\nAisle ' + str(shopList[aisle][0]) + '\n'])
        for item in range(1,len(shopList[aisle])):
            wanted = input(shopList[aisle][item].ljust(30) + "     Add 'y' or 'enter' to skip? ")
            #print(shopList[aisle][item])
            if wanted == 'y':
                defaultGroceryWriter.writerow([str(shopList[aisle][item])])
            else:
                continue
