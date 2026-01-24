from typing import Optional

from pydantic import BaseModel


class MessageState(BaseModel):
    message: Optional[str] = None
    user_data: Optional[int] = None
    ai_data: Optional[int] = None