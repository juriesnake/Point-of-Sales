import os
import datetime

margin = "  "

# returns list of products with their other attributes as list
def getproducts(csv):

    cod, prd, pri, qty = [], [], [], []

    # read the csv and save to list
    f = open("{}.csv".format(csv))
    firstRow = True
    for i, line in enumerate(f):
        if firstRow:
            firstRow = False
            continue
        temp = line.split(',')
        cod.append(temp[0].strip())
        prd.append(temp[1].strip())
        pri.append(float(temp[2].strip()))
        qty.append(int(temp[3].strip()))

    # get the length of longest product name used for formatting the menu
    # if length is less than 7, set it to 7 as default
    length = 0
    for productname in prd:
        if len(productname) > length:
            length = len(productname)
    if length < 7:
        length = 7

    # add space char to product name to make them all equal for displaying the menu
    for i, productname in enumerate(prd):
        size = len(productname)
        while(length > size):
            prd[i] += ' '
            size += 1

    return cod, prd, pri, qty, length

# displays the products as menu
def displaymenu(storename, cod, prd, pri, qty, length):
    os.system("cls")
    now = datetime.datetime.now()
    print("{0}Date: {1}{0}Time: {2}".format(margin, now.strftime("%Y.%m.%d"), now.strftime("%I:%M %p")), end = "\n\n")
    print(storename.center(len(margin) * 5 + length + 14))
    print("{0}{1}{0}{2}{0}{3}{0}{4}".format(margin, "Code", "Product".center(length), "Price".center(7), "Qty"))
    for i, value in enumerate(prd):
        print("{0}{1}{0}{2}{0}{3:7.2F}{0}{4:4}".format(margin, cod[i].center(4), prd[i], pri[i], qty[i]))
    print("")

# add and remove orders
def order(storename, cod, prd, pri, qty, length):
    code, quantity = [], []
    while(True):

        # display menu
        displaymenu(storename, cod, prd, pri, qty, length)

        # display current orders
        if len(code) > 0:
            print("{0}Current Orders".format(margin))
            print("{0}{1}{0}{2}{0}{3}{0}{4}".format(margin, "Code", "Qty", "Price", "Total"))
            for i, v in enumerate(code):
                indexCSV = cod.index(code[i])
                print("{0}{1}{0}{2:3}{0}{3:4}{0}{4:6}".format(margin,
                code[i].center(4), quantity[i], pri[indexCSV], pri[indexCSV] * quantity[i]))

        # get order
        print("\n{0}Order: ".format(margin), end = "")
        order = input().split('.')

        # Check orders
        if order[0].upper() == "X": # end orders
            break
        if len(order) > 2 or len(order) == 1: # invalid due to number of list
            error("Invalid! Format: tCODE.QUANTITY")
            continue

        # Assign to variables
        order[0] = order[0].strip().upper()
        try:
            order[1] = int(order[1])
        except:
            error("Quantity is not a number")
            continue

        # Check if CODE is in the MENU
        if order[0] not in cod: # if code is not existing in menu
            error("Does not exist in the MENU")
            continue

        # Check if QUANTITY is ZERO
        if order[1] == 0:
            error("No added or removed order")
            continue

        # index of CSV from order
        indexCSV = cod.index(order[0])

        # Check if selected order stocks is zero
        if qty[indexCSV] == 0:
            print("Out of Stock")
            input()
            continue

        # TRY if already in current orders, EXCEPT if not in the current orders
        try:
            indexCODE = code.index(order[0])
            temp = quantity[indexCODE] + order[1]
            if temp < 0:
                error("Quantity must not be negative")
                continue
            elif temp > qty[indexCSV]:
                error("Stock is not enough")
                continue
            else:
                quantity[indexCODE] = temp
                if quantity[indexCODE] == 0:
                    del code[indexCODE]
                    del quantity[indexCODE]
        except:
            if order[1] > qty[indexCSV]:
                error("Stock is not enough")
                continue
            elif order[1] > 0:
                code.append(order[0])
                quantity.append(order[1])

    # returns list of codes and quantity for their orders
    return code, quantity

# prints a receipt and update current stocks as list for next customer
def billing(code, quantity, cod, prd, pri, qty, length):

    while True:

        # show total but not yet efficient because needs to execute everytime input is wrong
        os.system("cls")
        print("\n{0}{1}".format(margin, "Bill"))
        total = 0
        for i, v in enumerate(code):
            indexCSV = cod.index(v)
            subtotal = pri[indexCSV] * quantity[i]
            total += subtotal
            print("{0}{1}{0}{2:3}{0}{3:4}{0}{4:6}".format(margin,
            code[i].center(4), quantity[i], pri[indexCSV], subtotal))
        print("{}Total: {}".format(margin, total))

        # conditions for payment
        try:
            print("{0}Cash: ".format(margin), end='')
            cash = int(input())
        except:
            continue

        if cash >= total:
            change = cash - total
            print("{0}Change: {1}".format(margin, change))
            showcashbreakdown(change)
            break
        else:
            error("Cash not enough")

    # payment
    # update stocks

    return qty

# update the sales csv as record of sales for the day
def updatesales():
    print("")

# update the product csv to change its stocks or quantity for the next use of the app
def updatestocks(code, quantity, cod, prd, pri, qty, csv):
    f = open("{}.csv".format(csv), 'w')
    print("Code,Product Name, Price, Quantity", file = f)
    for i, v in enumerate(cod):
        if cod[i] in code:
            # overwrite
            print("{},{},{},{}".format(cod[i], prd[i].strip(), pri[i], qty[i] - quantity[code.index(cod[i])]), file = f)
        else:
            print("{},{},{},{}".format(cod[i], prd[i].strip(), pri[i], qty[i]), file = f)

def showcashbreakdown(cash):
    denomination, qty = [], []

    if cash >= 1000:
        temp = int(cash // 1000)
        cash -= temp * 1000
        denomination.append("{:7.2F}".format(1000))
        qty.append(temp)
        temp = 0
    if cash >= 500:
        temp = int(cash // 500)
        cash -= temp * 500
        denomination.append("{:7.2F}".format(500))
        qty.append(temp)
        temp = 0
    if cash >= 100:
        temp = int(cash // 100)
        cash -= temp * 100
        denomination.append("{:7.2F}".format(100))
        qty.append(temp)
        temp = 0
    if cash >= 50:
        temp = int(cash // 50)
        cash -= temp * 50
        denomination.append("{:7.2F}".format(50))
        qty.append(temp)
        temp = 0
    if cash >= 20:
        temp = int(cash // 20)
        cash -= temp * 20
        denomination.append("{:7.2F}".format(20))
        qty.append(temp)
        temp = 0
    if cash >= 10:
        temp = int(cash // 10)
        cash -= temp * 10
        denomination.append("{:7.2F}".format(10))
        qty.append(temp)
        temp = 0
    if cash >= 5:
        temp = int(cash // 5)
        cash -= temp * 5
        denomination.append("{:7.2F}".format(5))
        qty.append(temp)
        temp = 0
    if cash >= 1:
        temp = int(cash // 1)
        cash -= temp * 1
        denomination.append("{:7.2F}".format(1))
        qty.append(temp)
        temp = 0
    if cash >= 0.25:
        temp = int(cash // 0.25)
        cash -= temp * 0.25
        denomination.append("{:7.2F}".format(0.25))
        qty.append(temp)
        temp = 0

    for i, v in enumerate(denomination):
        print("{0}{0}{1}: {2}".format(margin, denomination[i], qty[i]))

def error(msg):
    print("{}{}".format(margin, msg), end='')
    input()
