import contextlib
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
    orderid: str
    sku: str
    quantity: int


@dataclass
class Batch:
    reference: str
    sku: str
    quantity: int
    lines: List[OrderLine]
    eta: int

    def __eq__(self, other):
        return other.reference == self.reference if isinstance(other, Batch) else False

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        return self.eta > other.eta

    def __lt__(self, other):
        return self.eta <= other.eta

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
    if any(i == order_line for i in batch.lines):
        return
    batch.lines.append(order_line)


def select_batch_for_order_line(order_line: OrderLine, batch_list: List[Batch]):
    with contextlib.suppress(StopIteration):
        return next(
            b for b in sorted(batch_list)
            if b.sku == order_line.sku
            and b.available_quantity > order_line.quantity
        )
