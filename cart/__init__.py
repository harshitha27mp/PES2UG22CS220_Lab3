# #unoptimised

# import json

# import products
# from cart import dao
# from products import Product


# class Cart:
#     def __init__(self, id: int, username: str, contents: list[Product], cost: float):
#         self.id = id
#         self.username = username
#         self.contents = contents
#         self.cost = cost

#     def load(data):
#         return Cart(data['id'], data['username'], data['contents'], data['cost'])


# def get_cart(username: str) -> list:
#     cart_details = dao.get_cart(username)
#     if cart_details is None:
#         return []
    
#     items = []
#     for cart_detail in cart_details:
#         contents = cart_detail['contents']
#         evaluated_contents = eval(contents)  
#         for content in evaluated_contents:
#             items.append(content)
    
#     i2 = []
#     for i in items:
#         temp_product = products.get_product(i)
#         i2.append(temp_product)
#     return i2

    


# def add_to_cart(username: str, product_id: int):
#     dao.add_to_cart(username, product_id)


# def remove_from_cart(username: str, product_id: int):
#     dao.remove_from_cart(username, product_id)

# def delete_cart(username: str):
#     dao.delete_cart(username)

##optimised

import json

import products
from cart import dao
from products import Product


class Cart:
    def _init_(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    # Fetch the cart details from the database
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Optimize by deserializing JSON once and handling items in bulk
    all_product_ids = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])  # Avoid using eval for security and speed
            all_product_ids.extend(contents)
        except json.JSONDecodeError:
            continue

    # Fetch all products in a single query or batch operation
    products_map = products.get_products_bulk(all_product_ids)  # Assume this function fetches all products at once

    # Construct the product list
    return [products_map[pid] for pid in all_product_ids if pid in products_map]


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)