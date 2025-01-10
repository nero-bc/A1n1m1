from dataclasses import dataclass

@dataclass
class AnimeData:
    title : str
    image : str
    id : int
    mail_id: int
    type : str
    score : int
    episodes : int
    duration : str
    status : str
    genres : str
    tags : str
    description : str

@dataclass
class AnimeLink:
    quality: str
    link: str

    def __hash__(self) -> int:
        return hash(self.url)

@dataclass
class ResultAnime:
    title: str
    id : int
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ResultAnime):
            return self.id == other.id
        return False

@dataclass
class latest:
    title : str
    id : int
    episode : int
    
@dataclass
class popular:
    title : str
    id : int

