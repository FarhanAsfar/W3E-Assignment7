from pydantic import BaseModel, Field
import datetime, timezone

class Expense(BaseModel):
    id: str
    date: str
    category: str
    amount: float
    currency: str
    note: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
         

