import ordering

def main():
    storename = "Jollibee"
    csvProducts = "Products"

    # read a products.csv as list
    # count longest product name and save to variable length used for formatting display of menu
    cod, prd, pri, qty, length = ordering.getproducts(csvProducts)

    # display a menu from dispaymenu() function
    # add and remove orders and return a orders as list
    code, quantity = ordering.order(storename, cod, prd, pri, qty, length)

    # payment and printing of receipt
    # updates the stocks
    if len(code) != 0:
        ordering.billing(code, quantity, cod, prd, pri, qty, length)

    ordering.updatestocks(code, quantity, cod, prd, pri, qty, csvProducts)

if __name__ == "__main__": main()

'''
READ ME
1. max PRICE is 9999.99 and max QTY is 999
2. file must be csv
'''
