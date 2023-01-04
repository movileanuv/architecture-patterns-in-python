from dataclasses import dataclass


class AllocationError(Exception):
    pass


@dataclass
class Product:
    sku: str


@dataclass
class Customer:
    pass


@dataclass
class Order:
    reference: str
    lines: list


@dataclass
class OrderLine:
    order: Order
    sku: str
    quantity: int


@dataclass
class Batch:
    reference: str
    sku: str
    quantity: int
    lines: list
    eta: int

    @property
    def warehouse_stock(self):
        return self.eta == 0

    @property
    def available_quantity(self):
        return


def allocate(order_line: OrderLine, batch: Batch):
    pass


def select_batch_for_order_line():
    pass
