"""
Ejemplo completo: UserId vs OrderId con typing.Annotated.

Muestra dónde se define que user.id es UserId y que get_order espera OrderId.
"""

from typing import Annotated

# 1. Definimos los "tipos etiquetados": mismo tipo (int), distinta semántica
UserId = Annotated[int, "userId"]
OrderId = Annotated[int, "orderId"]


# 2. User: su atributo .id está anotado como UserId
class User:
    def __init__(self, id: UserId, name: str):
        self.id: UserId = id  # aquí se define que user.id es UserId
        self.name = name


# 3. Order: su atributo .id está anotado como OrderId
class Order:
    def __init__(self, id: OrderId, total: float):
        self.id: OrderId = id
        self.total = total


# 4. get_user recibe UserId y devuelve User (y User.id es UserId)
def get_user(id: UserId) -> User:
    return User(id=id, name="Alice")


# 5. get_order recibe OrderId (aquí se define que get_order "espera" OrderId)
def get_order(id: OrderId) -> Order:
    return Order(id=id, total=99.0)


if __name__ == "__main__":
    # user.id es UserId porque User.id está anotado como UserId (paso 2)
    user = get_user(42)

    # get_order espera OrderId porque su parámetro está anotado así (paso 5)
    # Pasamos user.id (UserId) donde se espera OrderId → error de sentido, el checker puede avisar
    order = get_order(user.id)  # type checker puede marcar incompatibilidad UserId vs OrderId

    # Correcto: pasar un OrderId
    order_id: OrderId = 100
    order = get_order(order_id)
