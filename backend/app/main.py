from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import contract, company
from fastapi.middleware.cors import CORSMiddleware

from app.config import OUTPUT_DIR

app = FastAPI(title="Contract Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    contract.router,
    prefix="/api/contract",
    tags=["contract"]
)

app.include_router(
    company.router,
    prefix="/api/company",
    tags=["company"]
)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")
