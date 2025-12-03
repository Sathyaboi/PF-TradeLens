from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import schemas, crud, models

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolios"]
)

# --------------------------
# Create Portfolio
# --------------------------
@router.post("/create", response_model=schemas.PortfolioOut)
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(get_db)):
    """
    Creates a new portfolio linked to a user.
    """
    user = db.query(models.User).filter(models.User.user_id == portfolio.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_portfolio(db, portfolio)


# --------------------------
# Add Ticker to a Portfolio
# --------------------------
@router.post("/add_ticker")
def add_ticker(ticker: schemas.TickerAdd, db: Session = Depends(get_db)):
    """
    Add a stock ticker + weight to a portfolio.
    """
    portfolio = db.query(models.Portfolio).filter(models.Portfolio.portfolio_id == ticker.portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    new_ticker = crud.add_ticker(db, ticker)
    return {"message": "Ticker added successfully", "ticker_id": new_ticker.id}


# --------------------------
# Get a portfolio with tickers
# --------------------------
@router.get("/{portfolio_id}", response_model=schemas.PortfolioDetailOut)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio_with_tickers(db, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio
