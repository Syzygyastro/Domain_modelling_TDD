from datetime import date, timedelta
from domain.model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("Batch-001", sku, batch_qty, eta=today),
        OrderLine("order-123", sku, line_qty)
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-CHAIR", qty=20, eta=today)
    line = OrderLine("order-ref", "SMALL-CHAIR", 2)
    batch.allocate(line)
    assert(batch.available_quantity == 18)


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert not small_batch.can_allocate(large_line)


def test_can_allocate_if_available_equal_to_required():
    equal_batch, equal_line = make_batch_and_line("ELEGANT-LAMP", 10, 10)
    assert equal_batch.can_allocate(equal_line)
    

def test_cannot_allocate_if_skus_dont_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_line = OrderLine("order-123", "EXPENSIVE-SOFA", 10)
    
    assert  not batch.can_allocate(different_line)

def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    
    assert batch.available_quantity == 20
    
def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18