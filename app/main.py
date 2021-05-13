from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.crud import trade_crud
from app.database import get_db
from app.schemas import trade_schemas
from app.views import trade_views
from app.scripts.generate_random_trades import generate

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trade_views.router)


@app.get("/generate_10_random_trades/")
def generate_10_random_trades(db: Session = Depends(get_db)):
    success = generate(db, 10)
    if success is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return 200


