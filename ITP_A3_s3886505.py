# Name: Thien Nguyen Vanovich
# Student id: s3886505
# Attempted PASS, CREDIT level.
# Submission 2

# In DI level, question 7, list of orders can have multiple orders made by the same customer with the identical products.
# This requires checking whether orders have identical product made by the same customer, and then combine the quantities made.
# Product name in the orders can be name or ID. Therefore, for each order where the product name is name, we have to convert the name into ID, to create a table as in the example.
# Additionaly, orders can have a customer ID, so we have to convert customer id to name


class Customer:
    def __init__(self, ID, name, category, discount=0.1, total=0):
        self.ID = ID
        self.name = name
        self.category = category
        self.discount = discount/100
        self.total = total

    def getID(self):
        return self.ID

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getDiscount(self, price):
        pass


class Product:
    def __init__(self, ID, name, price, stock):
        self.ID = ID
        self.name = name
        self.price = price
        self.stock = stock

    def getID(self):
        return self.ID

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getStock(self):
        return self.stock


class Order:

    def __init__(self, customer, products, comments=None):

        # we will store ID in customer property
        self.customer = customer
        self.products = products
        self.comments = comments

    def getCustomer(self):
        return self.customer

    def getProducts(self):
        return self.products


class Records:
    customers = []
    products = []
    orders = []

    def getProducts(self):
        return self.products

    def getCustomers(self):
        return self.customers

    def getOrders(self):
        return self.orders

    def readCustomers(self):
        fhand = open('customers.txt')
        for line in fhand:
            # for each line create customer object and add them to 'customers' list
            line = line.rstrip()
            line = line.translate(line.maketrans('', '', ","))
            splittedLine = line.split()
            if len(splittedLine) ==0:
                continue
            if (splittedLine[2].lower() == "r"):
                customer = RetailCustomer(
                    splittedLine[0], splittedLine[1], splittedLine[2], float(splittedLine[3]), int(splittedLine[4]))
            else:
                customer = WholesaleCustomer(
                    splittedLine[0], splittedLine[1], splittedLine[2], float(splittedLine[3]), int(splittedLine[4]))
            self.customers.append(customer)

    def readProducts(self):
        fhand = open('products.txt')
        for line in fhand:
            
            # for each line create product or combo object and add them to'products' or 'combos' list
            line = line.rstrip()

            line = line.translate(line.maketrans('', '', ','))
            splittedLine = line.split()
            if len(splittedLine) ==0:
                continue
            if splittedLine[0].startswith('P'):
                product = Product(
                    splittedLine[0], splittedLine[1], float(splittedLine[2]), int(splittedLine[3]))
                self.products.append(product)
            else:
                # in the combo data, we count duplicated products and store the count under the product name using a dictionary
                d = dict()
                for i in range(2, len(splittedLine)-1, 1):
                    d[splittedLine[i]] = d.get(splittedLine[i], 0)+1
                combo = Combo(
                    splittedLine[0], splittedLine[1], d, splittedLine[len(splittedLine)-1])
                print('combooooooo', d)
                self.products.append(combo)

    def readOrders(self):
        fhand = open('orders.txt')
        for line in fhand:
            # for each line create order object and add them to'orders' list
            line = line.rstrip()
            line = line.translate(line.maketrans('', '', ','))
            splittedLine = line.split()
            if len(splittedLine) ==0:
                continue
            d=dict()
            d[splittedLine[1]]=int(splittedLine[2])
            # if an order has comments

            if len(splittedLine) > 3:
                order = Order(
                    splittedLine[0], d, splittedLine[3])
                self.orders.append(order)
            # no comments
            else:
                order = Order(
                    splittedLine[0], d)
                self.orders.append(order)

    def findCustomer(self, _customer):
        # checking if customer is id or name,
        # then creating a search on the relevant property of a customer object
        if (_customer.startswith('C') and _customer[1].isnumeric()):
            for customer in self.customers:
                if customer.ID == _customer:
                    return customer
            return None
        else:
            for customer in self.customers:
                if customer.name.lower() == _customer.lower():
                    return customer
            return None

    def findProduct(self, _product):
        if (_product.startswith('P') and _product[1].isnumeric()) or (_product.startswith('COM')):
            for product in self.products:
                if product.ID == _product:
                    return product
            return None
        else:
            for product in self.products:
                if product.name.lower() == _product.lower():
                    return product
            return None

    def listCustomers(self):
        for customer in self.customers:
            print("{:<8} {:<8}".format(customer.ID, customer.name))

    def listProducts(self):
        for product in self.products:

            print("{:<8} {:<15} {:<8} {:<8}".format(product.ID,
                  product.name, "$%g" % float(product.getPrice()), product.getStock()))

    def addNewCustomer(self, customer):

        self.customers.append(customer)

    def addNewOrder(self, order):
        self.orders.append(order)

    def changeCustomerTotal(self, customer, total):
        self.findCustomer(customer).total += total

    def changeStock(self, productName, quantity):

        self.findProduct(productName).stock -= quantity


class RetailCustomer(Customer):

    def __init__(self, ID, name, category, discount=0.1, total=0):
        super().__init__(ID, name, category, discount, total)

    def getDiscount(self, price):
        return price * self.discount

    def displayCustomer(self):
        print(self.ID, self.name)

    def setRate(self, rate):
        self.discountRate = rate/100


class WholesaleCustomer(Customer):
    threshold = 1000

    def __init__(self, ID, name, category, discount=0.1, total=0):
        super().__init__(ID, name, category, discount, total)

    def getDiscount(self, price):
        totalDiscount = 0
        if price >= self.threshold:
            totalDiscount = self.threshold * self.discount + \
                (price - self.threshold) * (self.discount + 0.05)
            return totalDiscount
        else:
            totalDiscount = price * self.discount
            return totalDiscount

    def setRate(self, rate):
        self.discountRate = rate/100

    def setThreshold(self, threshold):
        self.threshold = threshold


class Combo:
    def __init__(self, ID, name, products, stock):
        self.ID = ID
        self.name = name
        # products and its quantities are stored in a dictionary
        self.products = products
        self.stock = stock

    def getPrice(self):
        totalPrice = 0
        records = Records()
        for product in list(self.products):
            price = records.findProduct(product).getPrice()
            totalPrice += price * self.products[product]
        return totalPrice * 0.9

    def getStock(self):
        return self.stock


def menu(records):

    print('')
    print('======== MENU ========')
    print('')
    print('Here is the list of our customers!')
    records.listCustomers()
    print('Here is the list of our products!')
    records.listProducts()
    print("To make an order type -- 'order'")
    print("To list all orders type -- 'orders'")
    print("To change discount rate for a customer type -- 'rate'")
    print("To cange threshold for a customer type -- 'threshold'")

    print("To exit the program type -- 'exit'")
    print('')

    action = input("Type your action... ").lower().strip()
    while action != "order" and action != "exit" and action != "rate" and action != "threshold" and action != "orders":
        action = input("Please type an appropriate action ")
    if action == "order":
        return order(records)
    elif action == "rate":
        return setRate(records)
    elif action == "threshold":
        return setThreshold(records)
    elif action == "orders":
        return orders(records)
    elif action == "exit":
        print("Thanks for using our service!")
        return


def order(records):

    customer = input('Enter customer name or ID: ')
    while customer == "":
        customer = input('Enter customer name or ID: ')
    # finding whether the customer name exist in our customer list in records
    member = records.findCustomer(customer)

    products = input(
        'Please enter a/multiple product name or ID and its quantity: ')

    while products == "":
        products = input(
            'Please enter a/multiple product or multiple products and its quantity: ')
    # assume that the input for products is a string of '<product_name> <quantity>...'
    products = products.rstrip()
    products = products.translate(
        products.maketrans('', '', ',')).split()

    # storing product name and the quantity in dictionary
    d = dict()
# try:
    for i in range(0, len(products)-1, 2):
        # checking whether the quantity input is correct and whether the product exists
        productRecord = records.findProduct(products[i])
        if int(products[i+1]) <= 0 or productRecord == None:
            _input = input(
                'Incorrect product name or quantity, would you like to continue? (Y/N)')
            if _input.lower() == "y":
                return order(records)
            else:
                return menu(records)
        # checking whether the price is negative for the product
        price = productRecord.getPrice()
        if price < 0:
            _input = input(
                'Incorrect product name or quantity, would you like to continue? (Y/N)')
            if _input.lower() == "y":
                return order(records)
            else:
                return menu(records)
        # checking whether the quantity ordered is not above available stock
        stock = productRecord.getStock()
        if stock < int(products[i+1]):
            _input = input(
                'Not enough stock for one of the products. Please check our menu for the amount of stock available for the product. Would you like to continue? (Y/N)')
            if _input.lower() == "y":
                return order(records)
            else:
                return menu(records)
        d[products[i]] = int(products[i+1])
        if member == None and price == 0:
            _input = input(
                'Sorry, no free items for new customers, would you like to make a new order? (Y/N)')
            if _input.lower() == "y":
                return order(records)
            else:
                return menu(records)

    print(customer, ' purchased ')
    totalPrice = 0
    # except:
    #     _input = input(
    #         'Incorrect product name or quantity, would you like to continue? (Y/N)')
    #     if _input.lower() == "y":
    #         return order(records)
    #     else:
    #         return menu(records)
        

    for product in list(d):
        quantity = int(d[product])
        # find the product in the records to get its price
        productRecord = records.findProduct(product)
        # changing the stock for each product after the order
        records.changeStock(product, quantity)

        print(quantity, " x ", product)
        print('Unit price of', product, productRecord.getPrice())
        totalPrice += quantity * \
            float(productRecord.getPrice())

     # if customer is not on the list, then generate a new ID ('C' + customer list length +1)
    if member is None:
        print('Total price ',  totalPrice)
        newID = "C"+str(len(records.customers)+69)
    
        new_order = Order(newID, d)
        records.addNewOrder(new_order)
        newCustomer = RetailCustomer(
            newID, customer, "R", 10, totalPrice)
        records.addNewCustomer(newCustomer)
    else:
        totalPrice = totalPrice - member.getDiscount(totalPrice)
        print('Total price ', totalPrice)
        new_order = Order(member.ID, d)
        records.addNewOrder(new_order)
    return menu(records)


def setRate(records):
    customer = input('Enter customer name or ID: ')
    while customer == "":
        customer = input('Enter customer name or ID: ')
    # finding whether the customer name exist in our customer list in records
    member = records.findCustomer(customer)
    if member is None:
        inp = input(
            'No customers found. Would you like to change customer name or ID? (Y/N)')
        if inp.lower() == "y":
            return setRate(records)
        else:
            return menu(records)

    rate = input('Enter new discount rate for the customer: ')
    while rate == "":
        customer = input('Enter new discount rate for the customer ')
    try:
        _rate = int(rate)
        if _rate < 0:
            inp = input(
                'Please, enter an appropriate discount rate. Would you like to repeat? (Y/N)')
            if inp.lower() == "y":
                return setRate(records)
            else:
                return menu(records)

        member.setRate(_rate)
        print('checking whether the rate changed in the original object',
              records.findCustomer(customer).getDiscount(1000))

    except:
        inp = input('Invalid input. Would you like to continue? (Y/N)')
        if inp.lower() == "y":
            return setRate(records)
        else:
            return menu(records)


def setThreshold(records):
    customer = input('Enter customer name or ID: ')
    while customer == "":
        customer = input('Enter customer name or ID: ')
    # finding whether the customer name exist in our customer list in records
    member = records.findCustomer(customer)
    if member is None:
        inp = input(
            'No customers found. Would you like to change customer name or ID? (Y/N)')
        if inp.lower() == "y":
            return setThreshold(records)
        else:
            return menu(records)
    # checking whether the customer is WHOLESALE customer
    if member.getCategory().lower() != "w":
        inp = input(
            'Sorry, this customer is not a wholesale customer? Would you like to continue(Y/N)')
        if inp.lower() == "y":
            return setThreshold(records)
        else:
            return menu(records)
    threshold = input('Enter new threshold for the customer: ')
    while threshold == "":
        customer = input('Enter new threshold for the customer ')
    try:
        _threshold = int(threshold)
        if _threshold < 0:
            inp = input(
                'Please, enter an appropriate threshold. Would you like to repeat? (Y/N)')
            if inp.lower() == "y":
                return setThreshold(records)
            else:
                return menu(records)

        member.setThreshold(_threshold)
        print('checking whether the threshold changed in the original object',
              records.findCustomer(customer).threshold)

    except:
        inp = input('Invalid input. Would you like to continue? (Y/N)')
        if inp.lower() == "y":
            return setThreshold(records)
        else:
            return menu(records)


def orders(records):

    product_ids = []
    customer_names = []
    products = records.getProducts()
    customers = records.getCustomers()
    orders = records.getOrders()
    for product in products:
        product_ids.append(product.ID)
    for customer in customers:
        customer_names.append(customer.name)

    # We will store all the orders made by each customer in the list. Orders are dicitonaries, where product name is a key and quantity is a value
    filtered_orders = []
    for name in customer_names:
        # Storing orders product and quantity in a dictionary
        customer_orders = dict()
        for order in orders:
            #Note: customer have name or ID
            if order.customer == name or records.findCustomer(order.customer).getName() ==name:
                # Reminder: each order may have multiple products that are stored in dictionary, where product name is a key and quantity is a value
                products = order.getProducts()
                for product in list(products):
                    if (product.startswith('P') and product[1].isnumeric()) or product.startswith('COM'): 
                        customer_orders[product] = customer_orders.get(
                            product, 0) + products[product]
                    else:
                        productID = records.findProduct(product).getID()
                        customer_orders[productID] = customer_orders.get(
                            productID, 0) + products[product]
            else:
                continue
        filtered_orders.append(customer_orders)
    print('{:<8}'.format("   "), end='')
    for i in range(len(product_ids)):
        if i==len(product_ids)-1:
            print('{:<8}'.format(product_ids[i]))
            continue
        print('{:<8}'.format(product_ids[i]), end='')
    for i in range(len(filtered_orders)): 
   
      
        print('{:<8}'.format(customer_names[i]), end='')
        for z in range(len(product_ids)):
            quantity = -1

            for product in list(filtered_orders[i]):
                if z==len(product_ids)-1 and product == product_ids[z]:
                    quantity +=999
                    print('{:<8}'.format(filtered_orders[i][product])) 
                    break

                elif product == product_ids[z]:
                    quantity +=999
                    print('{:<8}'.format(filtered_orders[i][product]), end='')
                    break
                continue
            if quantity<0 and z==len(product_ids)-1:
                print('{:<8}'.format('0'))
                continue
            elif quantity<0:
                print('{:<8}'.format('0'), end='')
                continue
    inp = input('Go to menu?(Y/N)')
    if inp.lower()=='y':
        return menu(records)
    else:
        print('Thanks for using our service!')
        return

        
                    





def main():

    records = Records()
    try:
        records.readCustomers()
        records.readProducts()
        records.readOrders()

    except:
        print('File cannot be opened:')
        return
    menu(records)


main()
