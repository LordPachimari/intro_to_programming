# Name: Thien Nguyen Vanovich
# Student id: s3886505
# Attempted PASS, CREDIT, DI levels.
# Submission 4 (UPDATED DI LEVEL)


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
            if len(splittedLine) == 0:
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
            if len(splittedLine) == 0:
                continue
            if splittedLine[0].startswith('P'):
                product = Product(
                    splittedLine[0], splittedLine[1], float(splittedLine[2]), int(splittedLine[3]))
                self.products.append(product)
            else:
                # in the combo data, we count duplicated products and store the count under the product name key using a dictionary
                d = dict()
                for i in range(2, len(splittedLine)-1, 1):
                    d[splittedLine[i]] = d.get(splittedLine[i], 0)+1
                combo = Combo(
                    splittedLine[0], splittedLine[1], d, int(splittedLine[len(splittedLine)-1]))
                self.products.append(combo)

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
        self.discount = rate/100


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

        self.discount = rate/100

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
    print('Here is the list of our customers!')
    records.listCustomers()
    print('Here is the list of our products!')
    records.listProducts()
    print('')
    print("To make an order type -- 'order'")
    print("To list all orders type -- 'orders'")
    print("To change discount rate for a customer type -- 'rate'")
    print("To cange threshold for a wholesale customer type -- 'threshold'")
    print("To exit the program type -- 'exit'")
    print('')
    action = input("Type your action... ").lower().strip()
    while action != "order" and action != "exit" and action != "rate" and action != "threshold" and action != "orders":
        action = input("Please type an appropriate action ")
    if action == "order":
        return _order(records)
    elif action == "rate":
        return Rate(records)
    elif action == "threshold":
        return setThreshold(records)
    elif action == "orders":
        return listOrders(records)
    elif action == "exit":
        print("Thanks for using our service!")
        return


def _order(records):

    try:
        file = input('Enter order file name ')
        fhand = open(file)
    except:
        print("Something is wrong with the file/file name")
        return _order(records)

    for line in fhand:
        # for each line create order object and add them to'orders' list
        line = line.rstrip()
        # line = line.translate(line.maketrans('', '', ', '))
        splittedLine = line.split(', ')
        if len(splittedLine) == 0:
            continue
        d = dict()

        member = records.findCustomer(splittedLine[0])

        # pop the comment, if the comment exists.
        # if the length of splitted line is even, then the comment does exist
        if len(splittedLine) % 2 == 0:
            comment = splittedLine.pop()
        else:
            comment = None
        # Assume that an order may have multiple products, such as Linda, P3, 15, P1 20, COM1 5.
        try:
            # skip first value(customer name), and only focus on a product and its quantity. Skipping by 2 means we only care about the product name. Its quantity can be found by adding 1 to the index.
            for i in range(1, len(splittedLine)-1, 2):

                productRecord = records.findProduct(splittedLine[i])
                # checking whether the quantity input is correct and whether the product exists
                print("quantity", splittedLine[i+1])
                if int(splittedLine[i+1]) <= 0 or productRecord == None:
                    print("Incorrect product name or quantity")
                    continue
                # checking whether the price is negative for the product
                price = productRecord.getPrice()
                if price < 0:

                    print("Incorrect product name or quantity")
                    continue
                # checking whether the quantity ordered is not above available stock
                stock = int(productRecord.getStock())
                if stock < int(splittedLine[i+1]):

                    print(
                        'Not enough stock for ', splittedLine)
                    continue
                if member == None and price == 0:

                    print('Sorry, no free items for new customers')
                    continue

                d[splittedLine[i]] = int(splittedLine[i+1])

        except:
            _input = input(
                'Incorrect product name or quantity, would you like to continue? (Y/N)')
            if _input.lower() == "y":
                return _order(records)
            else:
                return menu(records)
        print(splittedLine[0], ' purchased ')
        totalPrice = 0

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
            if comment == None:
                new_order = Order(newID, d)
            else:
                new_order = Order(newID, d, comment)
            records.addNewOrder(new_order)
            newCustomer = RetailCustomer(
                newID, splittedLine[0], "R", 10, totalPrice)
            records.addNewCustomer(newCustomer)
        else:
            totalPrice = totalPrice - member.getDiscount(totalPrice)
            print('Total price ', totalPrice)
            new_order = Order(member.ID, d)
            if comment == None:
                new_order = Order(member.ID, d)
            else:
                new_order = Order(member.ID, d, comment)
            records.addNewOrder(new_order)
    inp = input("Would you like to make a new order? (Y/N)")
    if inp.lower() == "y":
        return _order(records)
    else:
        return menu(records)


def Rate(records):
    customer = input('Enter customer name or ID: ')
    while customer == "":
        customer = input('Enter customer name or ID: ')
    # finding whether the customer name exist in our customer list in records
    member = records.findCustomer(customer)
    if member is None:
        inp = input(
            'No customers found. Would you like to change customer name or ID? (Y/N)')
        if inp.lower() == "y":
            return Rate(records)
        else:
            return menu(records)

    rate = input('Enter new discount rate for the customer: ')
    while rate == "":
        rate = input('Enter new discount rate for the customer ')
    try:
        _rate = int(rate)
        if _rate < 0:
            inp = input(
                'Please, enter an appropriate discount rate. Would you like to repeat? (Y/N)')
            if inp.lower() == "y":
                return Rate(records)
            else:
                return menu(records)

        member.setRate(_rate)
        next = input("Rate for has successfully changed!. Go to menu? (Y/N)")
        if next.lower() == "y":
            return menu(records)
        else:
            print("Thanks for using our service")
            return

    except:
        inp = input('Invalid input. Would you like to continue? (Y/N)')
        if inp.lower() == "y":
            return Rate(records)
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
        threshold = input('Enter new threshold for the customer ')
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
        next = input("Threshold has successfully changed!. Go to menu? (Y/N)")
        if next.lower() == "y":
            return menu(records)
        else:
            print("Thanks for using our service")
            return

    except:
        inp = input('Invalid input. Would you like to continue? (Y/N)')
        if inp.lower() == "y":
            return setThreshold(records)
        else:
            return menu(records)

# DI level, question 7
# list of orders can have multiple orders made by the same customer with the identical products. This requires checking whether orders have identical product made by the same customer, and then combine the quantities made.
# Products in orders are stored in a dictionary, which adds more complexity to the code. Dictionary was choosen as an order can have muptiple products.
# Product name in the orders can be name or ID. Therefore, for each order where the product name is name, we have to convert the name into ID, to create a table like in the example.
# Additionaly, customer name can be name or ID, so we have to convert customer id to name, to create a table like in the example.


def listOrders(records):

    product_ids = []
    customer_names = []
    products = records.getProducts()
    customers = records.getCustomers()
    orders = records.getOrders()
    for product in products:
        product_ids.append(product.ID)
    for customer in customers:
        customer_names.append(customer.name)

    # We will store all the orders made by each customer in the list 'filtered_orders'. Orders are dicitonaries, where product name is a key and quantity is a value
    filtered_orders = []
    for name in customer_names:
        # Storing orders' product and quantity in a dictionary
        customer_orders = dict()
        for order in orders:
            # Note: customer can have name or ID
            if order.customer == name or records.findCustomer(order.customer).getName() == name:
                products = order.getProducts()
                for product in list(products):
                    if (product.startswith('P') and product[1].isnumeric()) or product.startswith('COM'):
                        customer_orders[product] = customer_orders.get(
                            product, 0) + products[product]
                    # if product name is name, we store it as ID
                    else:
                        productID = records.findProduct(product).getID()
                        customer_orders[productID] = customer_orders.get(
                            productID, 0) + products[product]
            else:
                continue
        filtered_orders.append(customer_orders)

    # Printing a row of product ids for the table view
    print('{:<8}'.format("   "), end='')
    for i in range(len(product_ids)):
        if i == len(product_ids)-1:
            print('{:<8}'.format(product_ids[i]))
            continue
        print('{:<8}'.format(product_ids[i]), end='')

    # Printing orders for each customer
    for i in range(len(filtered_orders)):
        print('{:<8}'.format(customer_names[i]), end='')
        for z in range(len(product_ids)):
            found = -1
            for product in list(filtered_orders[i]):
                if z == len(product_ids)-1 and product == product_ids[z]:
                    found += 2
                    print('{:<8}'.format(filtered_orders[i][product]))
                    break

                elif product == product_ids[z]:
                    found += 2
                    print('{:<8}'.format(filtered_orders[i][product]), end='')
                    break

                continue
            if found < 0 and z == len(product_ids)-1:
                print('{:<8}'.format('0'))
                continue
            elif found < 0:
                print('{:<8}'.format('0'), end='')
                continue
    inp = input('Go to menu?(Y/N)')
    if inp.lower() == 'y':
        return menu(records)
    else:
        print('Thanks for using our service!')
        return


def main():

    records = Records()
    try:
        records.readCustomers()
        records.readProducts()

    except:
        print('File cannot be opened:')
        return
    menu(records)


main()
