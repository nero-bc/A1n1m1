from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class AnimeData:
    attributes: Dict[str, Any] = field(default_factory=dict, init=False)
    def __init__(self, **kwargs):
        self.attributes = {}
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.attributes[key] = value
    def __repr__(self):
        attr_str = ', '.join(f"{key}={value}" for key, value in self.attributes.items())
        return f"{self.__class__.__name__}({attr_str})"
        
