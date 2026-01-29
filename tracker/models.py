from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Expense(BaseModel):
    id: str
    date: str
    category: str
    amount: float
    currency: str = "BDT"
    note: str
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "date": self.date,
    #         "category": self.category,
    #         "amount": self.amount,
    #         "currency": self.currency,
    #         "note": self.note,
    #         "created_at": self.created_at,
    #     }
         

