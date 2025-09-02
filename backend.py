# backend.py
from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import core
import random
import time

app = FastAPI(title="Equity Backend")

# Allows connections from everywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AllocationItem(BaseModel):
    label: str
    weight: float

class AllocationResponse(BaseModel):
    data: list[AllocationItem]

@app.get("/country-allocation", response_model=AllocationResponse)
def get_country_allocation():
    df = core.country_allocation()
    df = df.rename(columns={"country": "label"})
    return {"data": df.to_dict(orient="records")}

@app.get("/sector-allocation", response_model=AllocationResponse)
def get_sector_allocation():
    df = core.sector_allocation()
    df = df.rename(columns={"sector": "label"})
    return {"data": df.to_dict(orient="records")}

@app.get("/random-test-data", response_model=AllocationResponse)
def get_random_test_data():
    """Generate random 7 numbers scaled to 100% for performance testing."""
    start_time = time.time()
    
    # Pre-generate random numbers for faster access
    random_numbers = [random.uniform(0.1, 1.0) for _ in range(7)]
    
    # Scale to 100% using vectorized operations
    total = sum(random_numbers)
    scaled_numbers = [num / total for num in random_numbers]
    
    # Create labels efficiently
    labels = [f"Category {i+1}" for i in range(7)]
    
    # Create data items
    data = [AllocationItem(label=label, weight=weight) for label, weight in zip(labels, scaled_numbers)]
    
    processing_time = time.time() - start_time
    
    # Add performance header for debugging
    return {
        "data": data,
        "performance": {
            "processing_time_ms": round(processing_time * 1000, 2),
            "timestamp": time.time()
        }
    }

@app.get("/random-test-data-fast", response_model=AllocationResponse)
def get_random_test_data_fast():
    """Ultra-fast random data generation using pre-computed values."""
    # Use a simple, fast random number generation
    import secrets
    
    # Generate 7 random integers and scale them
    random_ints = [secrets.randbelow(100) + 1 for _ in range(7)]
    total = sum(random_ints)
    scaled_numbers = [num / total for num in random_ints]
    
    labels = [f"Cat {i+1}" for i in range(7)]
    data = [AllocationItem(label=label, weight=weight) for label, weight in zip(labels, scaled_numbers)]
    
    return {"data": data}
