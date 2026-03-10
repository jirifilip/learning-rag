from dataclasses import dataclass
from typing import Any


@dataclass
class Event:
    additional_properties: dict[str, Any]


def event_handler(event: Event) -> None:
    pass