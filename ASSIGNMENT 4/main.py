# ================================
# FASTAPI INTERNSHIP PROJECT
# TASK 4 (CART SYSTEM)
# ================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ================================
# PRODUCT DATA
# ================================

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "in_stock": True}
]

cart = []
orders = []
order_id_counter = 1


# ================================
# HELPER
# ================================

def get_product(product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# ================================
# Q1 + Q4: ADD TO CART
# ================================

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    product = get_product(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # check duplicate
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * product["price"]

            return {
                "message": "Cart updated",
                "cart_item": item
            }

    new_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": product["price"] * quantity
    }

    cart.append(new_item)

    return {
        "message": "Added to cart",
        "cart_item": new_item
    }


# ================================
# Q2: VIEW CART
# ================================

@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": total
    }


# ================================
# Q5: REMOVE ITEM
# ================================

@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# ================================
# Q5 + BONUS: CHECKOUT
# ================================

class Checkout(BaseModel):
    customer_name: str
    delivery_address: str


@app.post("/cart/checkout")
def checkout(data: Checkout):

    global order_id_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    created_orders = []
    total = 0

    for item in cart:
        order = {
            "order_id": order_id_counter,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"],
            "delivery_address": data.delivery_address
        }

        total += item["subtotal"]
        orders.append(order)
        created_orders.append(order)
        order_id_counter += 1

    cart.clear()

    return {
        "message": "Order placed",
        "orders_placed": created_orders,
        "grand_total": total
    }


# ================================
# Q6: VIEW ORDERS
# ================================

@app.get("/orders")
def get_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }


# ================================
# HOME
# ================================

@app.get("/")
def home():
    return {"message": "FastAPI Task 4 Cart System Running 🚀"}