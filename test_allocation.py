from datetime import date, timedelta
import pytest
from model import Batch, OrderLine, allocate, OutOfStock

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)

def test_prefers_warehouse_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)
    
    allocate(line, [in_stock_batch, shipment_batch])
    
    assert(in_stock_batch.available_quantity == 90)
    assert(shipment_batch.available_quantity == 100)

def test_prefers_earlier_batches():
    fastest_batch = Batch("fastest-batch", "RETRO-CLOCK", 100, today)
    average_batch = Batch("average-batch", "RETRO-CLOCK", 100, tomorrow)
    slow_batch = Batch("slow-batch", "RETRO-CLOCK", 100, later)
    line = OrderLine("oref", "RETRO-CLOCK", 10)
    
    allocate(line, [fastest_batch, average_batch, slow_batch])
    
    assert(fastest_batch.available_quantity == 90)
    assert(average_batch.available_quantity == 100)
    assert(slow_batch.available_quantity == 100)
    
def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)   
    
    allocation = allocate(line, [in_stock_batch, shipment_batch]) 
    
    assert(allocation == in_stock_batch.reference)

def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch  = Batch("in-stock-batch", "RETRO-CLOCK", 10, today)
    line = OrderLine("oref", "RETRO-CLOCK", 11)
    
    with pytest.raises(OutOfStock, match="RETRO-CLOCK"):
        allocate(line, [batch])
    
    
    