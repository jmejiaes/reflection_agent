"""
Complete example: UserId vs OrderId with typing.Annotated.

Shows where user.id is defined as UserId and where get_order expects OrderId.
"""

from typing import Annotated

# 1. Define "tagged types": same type (int), different semantics
UserId = Annotated[int, "userId"]
OrderId = Annotated[int, "orderId"]


# 2. User: its .id attribute is annotated as UserId
class User:
    def __init__(self, id: UserId, name: str):
        self.id: UserId = id  # here we define that user.id is UserId
        self.name = name


# 3. Order: its .id attribute is annotated as OrderId
class Order:
    def __init__(self, id: OrderId, total: float):
        self.id: OrderId = id
        self.total = total


# 4. get_user accepts UserId and returns User (and User.id is UserId)
def get_user(id: UserId) -> User:
    return User(id=id, name="Alice")


# 5. get_order accepts OrderId (here we define that get_order "expects" OrderId)
def get_order(id: OrderId) -> Order:
    return Order(id=id, total=99.0)


if __name__ == "__main__":
    # user.id is UserId because User.id is annotated as UserId (step 2)
    user = get_user(42)

    # get_order expects OrderId because its parameter is annotated that way (step 5)
    # We pass user.id (UserId) where OrderId is expected → semantic error, checker can warn
    order = get_order(user.id)  # type checker may flag UserId vs OrderId incompatibility

    # Correct: pass an OrderId
    order_id: OrderId = 100
    order = get_order(order_id)
