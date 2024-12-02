from dataclasses import dataclass
from datetime import datetime

from domain.user.user import UserInterface


@dataclass
class IdeaInterface:
    id: int
    user: UserInterface
    category: str

    status: str
    finishe_date: datetime | str

    title: str
    description: str
    admin_answer: str
    
    user_id: int
