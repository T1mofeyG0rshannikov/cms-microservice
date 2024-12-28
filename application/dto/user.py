from dataclasses import dataclass


@dataclass
class ChangeUserDTO:
    changed_email: bool
