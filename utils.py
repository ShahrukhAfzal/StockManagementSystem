class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def print_order_helper_text(event, stock_type, order_quantity, stock):
    """
    Eg.
    Before buying 1 stock1 stock, 10 stocks are remaining.
    After buying 1 stock1 stock, 9 stocks are remaining.
    """
    transaction_type = "selling"
    if stock_type.lower() == 'buy':
        transaction_type = "buying"

    print(f"{event} {transaction_type} {order_quantity} {stock.name} {get_stock_verb(order_quantity)}, "
          f"{stock.quantity} {get_stock_verb(stock.quantity)} are remaining.")


def get_stock_verb(quantity):
    stock_verb = "stock"
    if quantity > 1:
        stock_verb = "stocks"

    return stock_verb