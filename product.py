from flask import jsonify
# The Product class is used for creating product objects. Each product object
# consists of the product's title, description, and price.


class Product:
    productList = []   # List for storing product objects

    def __init__(self, title, description, price, bought):
        self.title = title
        self.description = description
        self.price = int(price)
        self.bought = int(bought)
        self.__class__.productList.append(self)

    # Used for representing class objects as a string
    def __repr__(self):
        return "title:% s description:% s price:% d" % (self.title, self.description, self.price)

    # Retrieves the title of a product
    def get_title(self):
        return self.title

    # Retrieves the description of a product
    def get_description(self):
        return self.description

    def get_bought(self):
        return self.bought

    def buy_item(self):
        self.bought = 1

    def getJson(self):
        data = {
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'bought': self.bought
        }
        return data
