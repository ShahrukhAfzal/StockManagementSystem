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

from utils import SingletonMeta, print_order_helper_text


class User:
    def __init__(self, username, balance=0, order_history=None):

        if order_history is None:
            order_history = list()
        self.username = username
        self.balance = balance
        self.order_history = order_history

    def can_buy_stock(self, stock_price):
        return self.balance >= stock_price


class Order:
    def __init__(self, stock, quantity, user, stock_type):
        self.stock = stock
        self.user = user
        self.quantity = quantity
        self.order_amount = self.get_order_amount(stock, quantity)
        self.stock_type = stock_type

    @staticmethod
    def get_order_amount(stock, quantity):
        return stock.price * quantity

    @staticmethod
    def generate_order_id(stock_type):
        return "stock_" + f"{stock_type}_" + str(uuid.uuid1())[:4] + str(int(time.time()))


class Orders(metaclass=SingletonMeta):
    STOCK_TYPES = ("buy", "sell")

    def __init__(self, **kwargs):
        orders = kwargs.get("orders")
        if orders is None:
            self.orders = list()

    def create(self, stock, quantity, user, stock_type):
        order = Order(stock, quantity, user, stock_type)
        print_order_helper_text("Before", stock_type, quantity, stock)
        # print(f"Before {stock_type}ing quantity is {stock.quantity}")
        stock.update_stock(quantity, stock_type)
        self.orders.append(order)
        print_order_helper_text("After", stock_type, quantity, stock)

        # print(f"After {stock_type}ing quantity is {stock.quantity}")

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
        if not isinstance(obj, Stock):
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
        self.stock_id = None
        self.name = name
        self.quantity = quantity
        self.price = price
        stocks = Stocks()
        stocks.add(self)

    def update_stock(self, quantity, stock_type):
        if stock_type.lower() == 'buy':
            self.quantity -= quantity
        elif stock_type.lower() == 'sell':
            self.quantity += quantity

    def check_available_quantity(self, quantity):
        return self.quantity >= quantity

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise WrongStockQuantityException
        self._quantity = value

    def __repr__(self):
        return f"{self.name}"


class Buy:
    def __init__(self, stock_name, quantity, user: User):
        stocks = Stocks()
        stock = stocks.get_stock(stock_name)
        if not stock:
            raise StockNotFoundException(stock_name)
        self.validate(stock, quantity, user)
        self.order(stock, quantity, user)

    @staticmethod
    def order(stock, quantity, user):
        order = Orders()
        order.create(stock, quantity, user, stock_type="Buy")

    @staticmethod
    def validate(stock, quantity, user):
        if not (user and isinstance(user, User)):
            raise Exception("Invalid User")

        if not stock.check_available_quantity(quantity):
            raise OutOfStockException

        if not user.can_buy_stock(stock.price):
            raise Exception(f"Sorry, you don't have enough balance to buy {stock.name}")

        return True


class Sell:
    def __init__(self, stock_name, quantity, user: User):
        stocks = Stocks()
        stock = stocks.get_stock(stock_name)
        if not stock:
            raise StockNotFoundException(stock_name)
        self.order(stock, quantity, user)

    @staticmethod
    def order(stock, quantity, user):
        order = Orders()
        order.create(stock, quantity, user, stock_type="Sell")


if __name__ == '__main__':
    from custom_exceptions import (WrongStockTypeException, DuplicateStockException, WrongObjectTypeException,
                                   WrongStockQuantityException, StockNotFoundException, OutOfStockException)
    s1 = Stock(name="stock1", quantity=10, price=999)
    s2 = Stock(name="stock2", quantity=1, price=674)
    u1 = User("shahrukh", 10000)
    Buy(s1.name, 1, u1)
    Sell(s1.name, 2, u1)
