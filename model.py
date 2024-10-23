from dataclasses import dataclass
from datetime import date
from typing import Optional 

@dataclass(frozen=True)
class OrderLine:
    Orderid: str
    sku : str
    qty : int

class Batch:
    def __init__(self, ref : str, sku : str, qty : int, eta : Optional[date]):
        self.ref = ref
        self.sku = sku
        self.available_quantity = qty
        self.eta = eta
        
    def allocate(self, line : OrderLine):
        self.available_quantity -= line.qty