from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product
)

router = APIRouter()

# criar rota de buscar todos os itens
# sempre vai ter 2 atributos obrigatorios, o PATH e o RESPONSE
@router.get("/products/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    products = get_products(db)
    return products

# criar rota de buscar 1 item
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="você está querendo buscar um produto que não existe")
    return db_product

# criar rota de adiconar um item
@router.post("/products/", response_model=ProductResponse)
def create_one_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

# criar rota de deletar um item
@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_one_product(product_id: int, db: Session = Depends(get_db)):
    product_db = delete_product(product_id=product_id, db=db)
    if product_db is None:
        raise HTTPException(status_code=404, detail="você está querendo deletar um produto que não existe")    
    return product_db

# criar rota de fazer update nos itens
@router.put("/products/{product_id}", response_model=ProductResponse)
def atualizar_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_db = update_product(db=db, product_id=product_id, product=product)
    if product_db is None:
        raise HTTPException(status_code=404, detail="você está querendo fazer um update em um produto que não existe")    
    return product_db