from app.models import Movie
from typing import Optional

async def get_movies(
        skip:int=0,
        limit:int=10,
        title: Optional[str]=None,
        year: Optional[str]=None,
        director: Optional[str]=None
):

    query={}
    return await Movie.find(query).skip(skip).limit(limit).to_list()