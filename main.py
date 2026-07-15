from fastapi import FastAPI
from models import Products
from config import session , engine
import database_models


app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

products = [
    
        Products(id=1, name="Product 1", description="Description 1", price=100, quantity=10),
        Products(id=2, name="Product 2", description="Description 2", price=200, quantity=20),
        Products(id=3, name="Product 3", description="Description 3", price=300, quantity=30)
    
]

@app.get("/")
def greet():
    return "Welcome to haarv tech academy"

@app.get("/products")
def get_products():
    db = session()
    db.query()

@app.get("/product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id == id:
            return product
    return "Product not found"

@app.post("/product")
def add_product(product:Products):
    products.append(product)
    return products

@app.put("/product")
def update_product(id: int , product: Products):
    for i in range(len(products)):
           if products[i].id == id:
            products[i] = product
            return "product updated sucessfully"
    return "product not found"

@app.delete("/product")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product deleted sucessfully"
    return "product not found"