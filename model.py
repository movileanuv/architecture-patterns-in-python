from dataclasses import dataclass

from typing import List


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


@dataclass(frozen=True)
class OrderLine:
    order: Order
    sku: str
    quantity: int


@dataclass
class Batch:
    reference: str
    sku: str
    quantity: int
    lines: List[OrderLine]
    eta: int

    @property
    def warehouse_stock(self):
        return self.eta == 0

    @property
    def available_quantity(self):
        return self.quantity - sum(i.quantity for i in self.lines)


def allocate(order_line: OrderLine, batch: Batch):
    if order_line.sku != batch.sku:
        raise AllocationError()
    if order_line.quantity > batch.available_quantity:
        raise AllocationError()
    batch.lines.append(order_line)


def select_batch_for_order_line():
    pass
