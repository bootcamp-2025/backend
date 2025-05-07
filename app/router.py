from fastapi import APIRouter, Query
from typing import Optional
from app.models import Movie
from app.crud import get_movies

router=APIRouter

@router.get("/movies", response_model=list[Movie])
async def read_movies(
        skip:int=Query(0, ge=0),
        limit:int=Query(10, le=100),
        title: Optional[str]=None,
        year: Optional[str]=None,
        director: Optional[str]=None
):

    return await get_movies(skip=skip, limit=limit, title=title, year=year, director=director)