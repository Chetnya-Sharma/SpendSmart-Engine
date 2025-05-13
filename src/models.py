from pydantic import BaseModel
from typing import List

class SpendProfile(BaseModel):
    groceries: float
    fuel: float
    dining: float
    travel: float

class Recommendation(BaseModel):
    card_name: str

class Transaction(BaseModel):
    date: str
    amount: float
    description: str

class ParsedStatement(BaseModel):
    transactions: List[Transaction]
