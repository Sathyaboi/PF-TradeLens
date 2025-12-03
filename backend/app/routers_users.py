from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import schemas, crud, models

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# --------------------------
# Create a New User
# --------------------------
@router.post("/create", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user with email, risk tolerance, and horizon.
    """
    # Check duplicate email
    if user.email:
        existing = db.query(models.User).filter(models.User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    return crud.create_user(db, user)
