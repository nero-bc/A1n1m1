from dataclasses import dataclass

@dataclass
class AiringData:
    title : str
    image : str
    anilist_id : int
    url : str
    status : str
    episode : int
    hat_notation : str
    airing : str
