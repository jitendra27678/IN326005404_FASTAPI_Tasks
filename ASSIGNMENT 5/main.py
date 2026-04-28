# =====================================
# FASTAPI INTERNSHIP — TASK 5 FINAL
# =====================================

from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

# =====================
# DATA
# =====================

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

orders = []
order_id = 1


# =====================
# CREATE ORDER (for testing Q4)
# =====================

@app.post("/orders")
def create_order(customer_name: str, product_name: str):
    global order_id

    order = {
        "order_id": order_id,
        "customer_name": customer_name,
        "product": product_name
    }

    orders.append(order)
    order_id += 1

    return {"message": "Order created", "order": order}


# =====================
# Q1 — SEARCH PRODUCTS
# =====================

@app.get("/products/search")
def search_products(keyword: str):

    results = [p for p in products if keyword.lower() in p["name"].lower()]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }


# =====================
# Q2 — SORT PRODUCTS
# =====================

@app.get("/products/sort")
def sort_products(
    sort_by: str = "price",
    order: str = "asc"
):

    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    reverse = (order == "desc")

    result = sorted(products, key=lambda p: p[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": result
    }


# =====================
# Q3 — PAGINATION
# =====================

@app.get("/products/page")
def paginate_products(
    page: int = 1,
    limit: int = 2
):

    start = (page - 1) * limit
    total = len(products)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "products": products[start:start + limit]
    }


# =====================
# Q4 — SEARCH ORDERS
# =====================

@app.get("/orders/search")
def search_orders(customer_name: str):

    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# =====================
# Q5 — SORT BY CATEGORY + PRICE
# =====================

@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {
        "total": len(result),
        "products": result
    }


# =====================
# Q6 — COMBINED API
# =====================

@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = products

    # SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # SORT
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    # PAGINATION
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }


# =====================
# HOME
# =====================

@app.get("/")
def home():
    return {"message": "FastAPI Task 5 Running "}