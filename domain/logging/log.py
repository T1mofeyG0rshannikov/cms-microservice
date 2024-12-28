from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogInterface:
    date: datetime
