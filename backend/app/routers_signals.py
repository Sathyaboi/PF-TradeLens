from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from .indicators import advanced_signal



router = APIRouter(
    prefix="/signals",
    tags=["Signals"]
)


# ----------------------------
# Request Model
# ----------------------------
class SignalRequest(BaseModel):
    symbols: List[str]


# ----------------------------
# Response Model
# ----------------------------
class SignalResponse(BaseModel):
    symbol: str
    signal: str


# ----------------------------
# /signals/generate
# ----------------------------
@router.post("/generate", response_model=List[SignalResponse])
def generate_signals(request: SignalRequest):
    """
    Generates BUY / SELL / HOLD signals for a list of stock tickers
    using the advanced signal engine (SMA + RSI + MACD).
    """

    results = []

    if not request.symbols or len(request.symbols) == 0:
        raise HTTPException(status_code=400, detail="No symbols provided.")

    for symbol in request.symbols:
        try:
            signal = advanced_signal(symbol.upper())
            results.append(SignalResponse(symbol=symbol.upper(), signal=signal))
        except Exception:
            results.append(SignalResponse(symbol=symbol.upper(), signal="ERROR"))

    return results