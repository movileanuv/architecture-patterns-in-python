from dataclasses import dataclass
import unittest


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


class AllocationError(Exception):
    pass


def allocate(order_line: OrderLine, batch: Batch):
    pass


def select_batch_for_order_line():
    pass


class AllocationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.batch = Batch(reference="1", sku="A", quantity=2, lines=[], eta=0)
        self.order = Order(reference="z", lines=[])

    def test_allocate_line_to_batch_with_different_sku_fails(self):
        order_line = OrderLine(order=self.order, sku="B", quantity=1)
        self.assertRaises(AllocationError, allocate(order_line, self.batch))

    def test_allocate_line_to_batch_with_not_enough_quantity_fails(self):
        order_line = OrderLine(order=self.order, sku="A", quantity=3)
        self.assertRaises(AllocationError, allocate(order_line, self.batch))

    def test_allocate_line_to_corresponding_batch_with_sufficient_quantity_is_successful(self):
        order_line = OrderLine(order=self.order, sku="A", quantity=2)
        allocate(order_line, self.batch)
        self.assertEqual(0, self.batch.available_quantity)

    def test_cannot_allocate_line_to_batch_twice(self):
        order_line = OrderLine(order=self.order, sku="A", quantity=1)
        allocate(order_line, self.batch)
        allocate(order_line, self.batch)
        self.assertEqual(1, self.batch.available_quantity)
        self.assertEqual(1, len(self.batch.lines))


class BatchSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.batch_tuple = (
            Batch(reference="1", sku="A", quantity=1, lines=[], eta=0),
        )

    def test_no_sku_match_finds_no_batch(self):
        pass

    def test_not_enough_quantity_finds_no_batch(self):
        pass

    def test_warehouse_stock_is_selected_first(self):
        pass

    def test_earliest_eta_is_allocated_first(self):
        pass


class BatchTests(unittest.TestCase):
    def test_available_quantity(self):
        pass

    def test_warehouse_stock_is_true_if_eta_is_zero(self):
        pass

    def test_warehouse_stock_is_false_if_eta_is_not_zero(self):
        pass
