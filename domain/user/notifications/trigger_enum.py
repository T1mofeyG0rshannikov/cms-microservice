from enum import StrEnum


class TriggerNames(StrEnum):
    sitecreated = "SITECREATED"
    emailverified = "EMAILVERIFIED"
    signedup = "SIGNEDUP"
