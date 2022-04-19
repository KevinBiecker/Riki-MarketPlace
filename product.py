from flask import jsonify


class Product:
    productList = []

    def __init__(self, title, description, price, bought):
        self.title = title
        self.description = description
        self.price = int(price)
        self.bought = int(bought)
        self.__class__.productList.append(self)


    def __repr__(self):
        return "title:% s description:% s price:% d" % (self.title, self.description, self.price)

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def buy_item(self):
        self.bought = 1

    def getJson(self):

        data = {
            'title': self.title,
            'description': self.description,
            'price': self.price
        }
        return data