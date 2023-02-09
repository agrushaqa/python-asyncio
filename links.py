from dataclasses import dataclass


@dataclass
class Links:
    path: str
    name: str
    content: str = ""
    # is_url: bool
