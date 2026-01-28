from pydantic import BaseModel, Field
from datetime import datetime, timezone

class Expense(BaseModel):
    id: str
    date: str
    category: str
    amount: float
    currency: str = "BDT"
    note: str
    created_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "currency": self.currency,
            "note": self.note,
        }
         

