from dataclasses import dataclass

@dataclass    
class CharacterData:
    image : str
    name : str
    native : str
    id : int
    voice_actors : list
    url : str
