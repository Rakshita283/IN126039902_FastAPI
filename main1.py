from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# -------------------------------
# Sample Data
# -------------------------------

products = [
    {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Phone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Shoes", "price": 3000, "category": "Fashion", "in_stock": False}
]

orders = []

# -------------------------------
# Pydantic Models
# -------------------------------

class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int


class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


# -------------------------------
# Home
# -------------------------------

@app.get("/")
def home():
    return {"message": "Welcome to Product API"}


# -------------------------------
# Get All Products
# -------------------------------

@app.get("/products")
def get_products():
    return products


# -------------------------------
# Filter Products
# -------------------------------

@app.get("/products/filter")
def filter_products(
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    in_stock: Optional[bool] = None
):
    filtered = products

    if category:
        filtered = [p for p in filtered if p["category"] == category]

    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    if in_stock is not None:
        filtered = [p for p in filtered if p["in_stock"] == in_stock]

    return filtered


# -------------------------------
# Compare Products
# -------------------------------

@app.get("/products/compare")
def compare_products(id1: int, id2: int):
    p1 = next((p for p in products if p["id"] == id1), None)
    p2 = next((p for p in products if p["id"] == id2), None)

    return {"product1": p1, "product2": p2}


# -------------------------------
# Get Product by ID
# -------------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return {"error": "Product not found"}


# -------------------------------
# Get All Orders
# -------------------------------

@app.get("/orders")
def get_orders():
    return orders


# -------------------------------
# Place Order
# -------------------------------

@app.post("/orders")
def place_order(order: Order):
    orders.append(order)
    return {"message": "Order placed successfully", "order": order}


# -------------------------------
# Submit Feedback
# -------------------------------

@app.post("/feedback")
def submit_feedback(feedback: CustomerFeedback):
    return {
        "message": "Feedback received",
        "data": feedback
    }
# -------------------------------
# Product Summary
# -------------------------------

@app.get("/products/summary")
def product_summary():
    total_products = len(products)
    total_price = sum(p["price"] for p in products)
    average_price = total_price / total_products if total_products > 0 else 0

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": total_products,
        "average_price": average_price,
        "categories_available": categories
    }