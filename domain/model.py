from dataclasses import dataclass
from datetime import date
from typing import List, Optional 

@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku : str
    qty : int

class Batch:
    def __init__(self, ref : str, sku : str, qty : int, eta : Optional[date]):
        self.reference = ref
        self.sku = sku
        self._purchased_quantity = qty
        self._allocations = set()
        self.eta = eta
        
    def allocate(self, line : OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line : OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
    
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
    
    def can_allocate(self, line : OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

def allocate(line : OrderLine, batches : List[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of Stock for sku {line.sku}')

class OutOfStock(Exception):
    pass
