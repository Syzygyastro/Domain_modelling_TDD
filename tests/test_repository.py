from datetime import date, timedelta
from domain.model import Batch, OrderLine, allocate, OutOfStock
import adapters.repository as repository


def test_repository_can_save_a_batch(session):
    batch = Batch("batch-1", "RUSTY-NAIL", 100, eta=None)
    
    repo = repository.SqlRepository(session)
    repo.add(batch)
    session.commit()
    
    rows = list(session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    ))
    assert(rows == [("batch-1", "RUSTY-NAIL", 100, None)])

# def insert_order_line(session):
#     session.execute(
#         "INSERT INTO order_lines (orderid, sku, qty)"
#         ' VALUES ("order1", "GENERIC-SOFA", 12)'
#     )
#     [[orderline_id]] = session.execute(
#         "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
#         dict(orderid="order1", sku="GENERIC-SOFA"),
#     )
#     return orderline_id