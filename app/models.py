
from beanie import Document
from typing import Optional

class Movie(Document):
    title: str
    director: Optional[str]
    year: int
    image: Optional[str] = None

    class Setting:
        name = "movies"
    
    