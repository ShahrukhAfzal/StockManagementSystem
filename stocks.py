# Design a stock exchange system. There is a list of stocks given with following attributes
#     order_id
#     time
#     stock name
#     type(BUY/SELL)
#     quantity
#     price
# You need to output list of stocks in the following format sell_id, buy_id, quantity, price which will get executed.

# Order
#     - should maintain all the ordered(Sell/Buy) stocks w.r.t
#         - stock_id
#         - order_id
#         - user_id
#         - quantity
#         - amount

# Stock
#     - should maintain some sort of inventory
#         - time
#         - stock name
#         - quantity
#         - price

#     # type(BUY/SELL)
#     # order_id

# Buy
#     - check if the ordered stocks are available or not
#     - update count accordingly
#         - type(BUY/SELL)
#         - order_id

# Sell
#     - increase the stock quantity

import time
import uuid

from custom_exceptions import (WrongStockTypeException, DuplicateStockException, WrongObjectTypeException,
                               WrongStockQuantityException, StockNotFoundException, OutOfStockException)
from utils import SingletonMeta


class User:
    def __init__(self, username, balance=0, order_history=None):
        if order_history is None:
            order_history = list()
        self.username = username
        self.balance = balance
        self.order_history = order_history


class Order:
    STOCK_TYPES = ("buy", "sell")

    def __init__(self, stock_id, user_id, quantity, amount, stock_type):
        self.stock_id = stock_id
        self.user_id = user_id
        self.quantity = quantity
        self.amount = amount
        self.stock_type = stock_type
        self.order_id = self.generate_order_id(stock_type)

    @staticmethod
    def generate_order_id(stock_type):
        return "stock_" + f"{stock_type}_" + str(uuid.uuid1())[:4] + str(int(time.time()))

    @property
    def stock_type(self):
        return self._stock_type

    @stock_type.setter
    def stock_type(self, stock_type):
        if stock_type not in self.STOCK_TYPES:
            raise WrongStockTypeException
        else:
            self._stock_type = stock_type


class Stocks(metaclass=SingletonMeta):
    def __init__(self):
        self.objects = dict()

    def add(self, obj):
        if obj.__class__ != Stock:
            raise WrongObjectTypeException

        if self.objects.get(obj.name):
            raise DuplicateStockException

        self.objects[obj.name] = obj

    def get_stock(self, name):
        return self.objects.get(name)

    def __repr__(self):
        return f"Total stocks available {len(self.objects)}"


class Stock:

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price
        stocks = Stocks()
        stocks.add(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        stocks = Stocks()
        self._name = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise WrongStockQuantityException
        self._quantity = value

    def __repr__(self):
        return f"{self.name}"


# Buy
#     - check if the ordered stocks are available or not
#     - update count accordingly
#         - type(BUY/SELL)
#         - order_id


class Buy:
    def __init__(self, stock_name, quantity, user: User):
        self.validate(stock_name, quantity, user)
        self.order()

    def order(self):
        pass

    @staticmethod
    def validate(stock_name, quantity, user):
        stocks = Stocks()
        stock = stocks.get_stock(stock_name)
        if not user:
            raise Exception("No user passed")

        if not stock:
            raise StockNotFoundException(stock_name)

        if not Buy.check_available_quantity(stock, quantity):
            raise OutOfStockException

        if not Buy.check_available_balance(user, stock):
            raise Exception(f"Sorry, you don't have enough balance to buy {stock.name}")

        return True

    @staticmethod
    def check_available_quantity(stock, quantity):
        return stock.quantity >= quantity

    @staticmethod
    def check_available_balance(user, stock):
        return user.balance >= stock.price


# Sell
#     - increase the stock quantity
class Sell:
    pass


if __name__ == '__main__':
    s1 = Stock(name="stock1", quantity=10, price=999)
    s2 = Stock(name="stock2", quantity=1, price=674)
    print(Stocks())
