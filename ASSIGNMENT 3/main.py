# ================================
# FASTAPI INTERNSHIP PROJECT
# TASK 3 (CRUD OPERATIONS)
# ================================

from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ================================
# PRODUCT DATA
# ================================

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# ================================
# HELPER FUNCTION
# ================================

def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# ================================
# Q1: ADD PRODUCT (POST)
# ================================

class NewProduct(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool = True


@app.post("/products")
def add_product(product: NewProduct, response: Response):
    # duplicate check
    for p in products:
        if p["name"].lower() == product.name.lower():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product already exists"}

    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        **product.dict()
    }

    products.append(new_product)

    response.status_code = status.HTTP_201_CREATED
    return {
        "message": "Product added",
        "product": new_product
    }


# ================================
# Q2: UPDATE PRODUCT (PUT)
# ================================

@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: Optional[int] = None,
    in_stock: Optional[bool] = None
):
    product = find_product(product_id)

    if not product:
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated",
        "product": product
    }


# ================================
# Q3: DELETE PRODUCT
# ================================

@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):
    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {
        "message": f"Product '{product['name']}' deleted"
    }


# ================================
# Q5: PRODUCT AUDIT (IMPORTANT POSITION)
# ================================

@app.get("/products/audit")
def product_audit():
    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]

    stock_value = sum(p["price"] * 10 for p in in_stock_list)
    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }


# ================================
# BONUS: DISCOUNT API
# ================================

@app.put("/products/discount")
def apply_discount(
    category: str = Query(...),
    discount_percent: int = Query(..., ge=1, le=99)
):
    updated = []

    for p in products:
        if p["category"] == category:
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)

    if not updated:
        return {"message": f"No products found in category: {category}"}

    return {
        "message": f"{discount_percent}% discount applied",
        "updated_products": updated,
        "count": len(updated)
    }


# ================================
# GET ALL PRODUCTS
# ================================

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# ================================
# GET PRODUCT BY ID
# ================================

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = find_product(product_id)

    if not product:
        return {"error": "Product not found"}

    return product


# ================================
# HOME
# ================================

@app.get("/")
def home():
    return {"message": "FastAPI Task 3 Running 🚀"}