

class WrongStockTypeException(Exception):

    def __init__(self):
        self.message = f"Stock Type can only be {Stock.STOCK_TYPES}."
        super().__init__(self.message)


class DuplicateStockException(Exception):

    def __init__(self):
        self.message = f"Stock already exists."
        super().__init__(self.message)


class WrongObjectTypeException(Exception):
    def __init__(self):
        self.message = f"Object type should be of {Stock}"
        super().__init__(self.message)


class WrongStockQuantityException(Exception):
    def __init__(self):
        self.message = f"Quantity should be greater than 0"
        super().__init__(self.message)


class StockNotFoundException(Exception):
    def __init__(self, stock_name):
        self.message = f"Stock not found with name: {stock_name}"
        super().__init__(self.message)


class OutOfStockException(Exception):
    def __init__(self):
        self.message = f"Ordered quantity not available at this time. " \
                       f"Try with lower quantity."
        super().__init__(self.message)


if __name__ == '__main__':
    from stocks import Stock