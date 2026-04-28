# ================================
# FASTAPI DAY 1 ASSIGNMENT
# All Tasks in One File (main.py)
# ================================

from fastapi import FastAPI

app = FastAPI()

# ================================
# BASE DATA (INITIAL PRODUCTS)
# ================================

products = [
    {"id": 1, "name": "Notebook", "price": 50, "category": "Stationery", "in_stock": True},
    {"id": 2, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Wireless Mouse", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 4, "name": "Headphones", "price": 1499, "category": "Electronics", "in_stock": False}
]

# ================================
# TASK 1 (Q1): ADD 3 MORE PRODUCTS
# ================================

products.extend([
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
])

# Endpoint to view all products
@app.get("/products")
def get_products():
    """
    Q1:
    Returns all products with total count
    """
    return {
        "products": products,
        "total": len(products)
    }

# ================================
# TASK 2 (Q2): FILTER BY CATEGORY
# ================================

@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    """
    Q2:
    Returns products filtered by category
    """
    result = [p for p in products if p["category"] == category_name]

    if not result:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }

# ================================
# TASK 3 (Q3): IN-STOCK PRODUCTS
# ================================

@app.get("/products/instock")
def get_instock():
    """
    Q3:
    Returns only products that are in stock
    """
    available = [p for p in products if p["in_stock"]]

    return {
        "in_stock_products": available,
        "count": len(available)
    }

# ================================
# TASK 4 (Q4): STORE SUMMARY
# ================================

@app.get("/store/summary")
def store_summary():
    """
    Q4:
    Returns store-level insights
    """
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }

# ================================
# TASK 5 (Q5): SEARCH PRODUCTS
# ================================

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    """
    Q5:
    Search products by keyword (case-insensitive)
    """
    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

# ================================
# BONUS TASK: DEALS (CHEAPEST + MOST EXPENSIVE)
# ================================

@app.get("/products/deals")
def get_deals():
    """
    BONUS:
    Returns cheapest and most expensive product
    """
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }

# ================================
# HOME ROUTE (OPTIONAL)
# ================================

@app.get("/")
def home():
    return {"message": "FastAPI Assignment Running Successfully "}