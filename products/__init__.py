# #unoptimesd
# from products import dao


# class Product:
#     def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.cost = cost
#         self.qty = qty

#     @staticmethod
#     def load(data):
#         return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


# def list_products() -> list[Product]:
#     # Fetch all products in one call
#     products_data = dao.list_products()

#     # Use a list comprehension for efficiency
#     return [Product.load(product) for product in products_data]


# def get_product(product_id: int) -> Product:
#     # Fetch product directly using the ID
#     product_data = dao.get_product(product_id)
#     if not product_data:
#         raise ValueError(f"Product with ID {product_id} not found")
#     return Product.load(product_data)


# def add_product(product: dict):
#     # Directly delegate adding product to the DAO
#     dao.add_product(product)


# def update_qty(product_id: int, qty: int):
#     # Validation to ensure no negative quantity
#     if qty < 0:
#         raise ValueError('Quantity cannot be negative')

#     # Fetch the current product only if needed (to minimize DB calls)
#     product_data = dao.get_product(product_id)
#     if not product_data:
#         raise ValueError(f"Product with ID {product_id} not found")

#     # Update the quantity in one step
#     dao.update_qty(product_id, qty)



##optimised

from products import dao

class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> "Product":
        """Load product data as a Product object."""
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0),
        )


# Cache for frequently accessed products
_product_cache = {}


def list_products() -> list[dict]:
    """Retrieve products as raw data."""
    # Fetch all products directly from DAO, bypassing unnecessary object creation
    products = dao.list_products()
    return products  # Avoid wrapping as Product objects unless necessary


def get_product(product_id: int) -> dict:
    """Retrieve a single product using cache for optimization."""
    if product_id in _product_cache:
        return _product_cache[product_id]  # Use cached data

    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")

    _product_cache[product_id] = product_data  # Add to cache
    return product_data


def add_product(product: dict):
    """Validate and add a new product."""
    required_keys = {'id', 'name', 'description', 'cost', 'qty'}
    if not required_keys.issubset(product.keys()):
        raise ValueError(f"Missing required product fields: {required_keys - product.keys()}")

    dao.add_product(product)
    # Invalidate the cache for consistency
    if product['id'] in _product_cache:
        del _product_cache[product['id']]


def update_qty(product_id: int, qty: int):
    """Update product quantity with basic validation."""
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")

    dao.update_qty(product_id, qty)
    # Optionally update cache if the product exists in the cache
    if product_id in _product_cache:
        _product_cache[product_id]['qty'] = qty
