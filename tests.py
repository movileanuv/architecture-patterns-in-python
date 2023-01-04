import unittest

from model import *


class AllocationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.batch = Batch(reference="batch-001", sku="SMALL-TABLE", quantity=2, lines=[], eta=0)
        self.order = Order(reference="order-001", lines=[])

    def test_allocate_line_to_batch_with_different_sku_fails(self):
        order_line = OrderLine(orderid="order-001", sku="LAMP", quantity=1)
        with self.assertRaises(AllocationError):
            allocate(order_line, self.batch)

    def test_allocate_line_to_batch_with_not_enough_quantity_fails(self):
        order_line = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=3)
        with self.assertRaises(AllocationError):
            allocate(order_line, self.batch)

    def test_allocate_line_to_batch_with_not_enough_quantity_fails_2(self):
        order_line_1 = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=1)
        allocate(order_line_1, self.batch)
        order_line_2 = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=2)
        with self.assertRaises(AllocationError):
            allocate(order_line_2, self.batch)

    def test_allocate_line_to_corresponding_batch_with_sufficient_quantity_is_successful(self):
        order_line = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=2)
        allocate(order_line, self.batch)
        self.assertEqual(0, self.batch.available_quantity)

    def test_cannot_allocate_line_to_batch_twice(self):
        order_line = OrderLine(orderid="order-001", sku="SMALL-TABLE", quantity=1)
        allocate(order_line, self.batch)
        allocate(order_line, self.batch)
        self.assertEqual(1, self.batch.available_quantity)
        self.assertEqual(1, len(self.batch.lines))


class BatchSelectionTests(unittest.TestCase):
    def test_no_sku_match_finds_no_batch(self):
        batch = Batch(reference="batch-001", sku="TABLE", quantity=1, lines=[], eta=0)
        order_line = OrderLine(orderid="order-001", sku="LAMP", quantity=1)
        self.assertEqual(None, select_batch_for_order_line(order_line, [batch]))

    def test_not_enough_quantity_finds_no_batch(self):
        batch = Batch(reference="batch-001", sku="TABLE", quantity=1, lines=[], eta=0)
        order_line = OrderLine(orderid="order-001", sku="TABLE", quantity=2)
        self.assertEqual(None, select_batch_for_order_line(order_line, [batch]))

    def test_warehouse_stock_is_selected_first(self):
        in_stock_batch = Batch(reference="in-stock-batch", sku="TABLE", quantity=10, lines=[], eta=0)
        shipment_batch = Batch(reference="in-stock-batch", sku="TABLE", quantity=10, lines=[], eta=100)
        order_line = OrderLine(orderid="order-001", sku="TABLE", quantity=2)
        self.assertEqual(in_stock_batch, select_batch_for_order_line(order_line, [in_stock_batch, shipment_batch]))

    def test_earliest_eta_is_allocated_first(self):
        earliest = Batch(reference="in-stock-batch", sku="TABLE", quantity=10, lines=[], eta=10)
        medium = Batch(reference="in-stock-batch", sku="TABLE", quantity=10, lines=[], eta=100)
        latest = Batch(reference="in-stock-batch", sku="TABLE", quantity=10, lines=[], eta=1000)
        order_line = OrderLine(orderid="order-001", sku="TABLE", quantity=2)
        self.assertEqual(earliest, select_batch_for_order_line(order_line, [latest, medium, earliest]))


class BatchTests(unittest.TestCase):
    def test_available_quantity(self):
        line_1 = OrderLine(orderid="order-001", sku="TABLE", quantity=2)
        line_2 = OrderLine(orderid="order-001", sku="TABLE", quantity=5)
        batch = Batch(reference="batch-001", sku="TABLE", quantity=10, lines=[line_1, line_2], eta=0)
        self.assertEqual(3, batch.available_quantity)

    def test_warehouse_stock_is_true_if_eta_is_zero(self):
        batch = Batch(reference="batch-001", sku="TABLE", quantity=10, lines=[], eta=0)
        self.assertEqual(True, batch.warehouse_stock)

    def test_warehouse_stock_is_false_if_eta_is_not_zero(self):
        batch = Batch(reference="batch-001", sku="TABLE", quantity=10, lines=[], eta=10)
        self.assertEqual(False, batch.warehouse_stock)
