from dataclasses import dataclass
import time

@dataclass
class Event:
    """
    Represents a single event in the system.

    :param type: The type of the event
    :type type: str
    :param data: The data associated with the event
    :type data: dict
    :param source: Optional source identifier of the event
    :type source: str | None
    :param timestamp: The time the event was created
    :type timestamp: float
    """
    type: str
    data: dict
    source: str | None = None
    timestamp: float = time.time()