from dataclasses import dataclass

@dataclass    
class MangaData:
    image : str
    id : int
    name : str
    native : str
    status : str
    source : str
    format : str
    score : int
    chapters : int
    volumes : int
    description : str
    url : str

