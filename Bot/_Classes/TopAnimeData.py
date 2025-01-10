from dataclasses import dataclass

@dataclass
class TopAnimeData:
    anime : list
    last_page : int
    has_next_page : bool
    total : int
