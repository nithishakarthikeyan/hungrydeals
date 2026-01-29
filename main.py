from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import requests

from database import SessionLocal
from models import Deal

load_dotenv()

app = FastAPI(title="Winnipeg Restaurant Deals API")

YELP_API_KEY = os.getenv("YELP_API_KEY")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------
# Root
# --------------------
@app.get("/")
def root():
    return {"message": "API is running"}


# --------------------
# Restaurants (Yelp)
# --------------------
@app.get("/restaurants")
def get_restaurants():
    url = "https://api.yelp.com/v3/businesses/search"

    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }

    params = {
        "location": "Winnipeg",
        "categories": "restaurants",
        "limit": 10
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    clean_restaurants = []
    for business in data.get("businesses", []):
        clean_restaurants.append({
            "id": business.get("id"),
            "name": business.get("name"),
            "rating": business.get("rating"),
            "price": business.get("price", "N/A"),
            "address": ", ".join(business.get("location", {}).get("display_address", [])),
            "categories": [c["title"] for c in business.get("categories", [])],
            "image": business.get("image_url")
        })


    return {"restaurants": clean_restaurants}


# --------------------
# Database Dependency
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------
# Deals
# --------------------
@app.get("/deals")
def get_all_deals(db: Session = Depends(get_db)):
    deals = db.query(Deal).all()
    return {
        "deals": [
            {
                "restaurant_id": d.restaurant_id,
                "title": d.title,
                "description": d.description,
                "valid_until": d.valid_until
            }
            for d in deals
        ]
    }


@app.get("/deals/{restaurant_id}")
def get_deals_for_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db)
):
    deals = (
        db.query(Deal)
        .filter(Deal.restaurant_id == restaurant_id)
        .all()
    )

    return {
        "deals": [
            {
                "title": d.title,
                "description": d.description,
                "valid_until": d.valid_until
            }
            for d in deals
        ]
    }
