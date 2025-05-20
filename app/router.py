from fastapi import APIRouter, Query, Form
from typing import Optional
from app.models import Movie
from app.crud import read_movies, create_movie

router=APIRouter()

@router.post("/movies", response_model=Movie)
async def post_movie(
        title: str = Form(None),
        director: str | None = Form(None),
        year: int | None = Form(None),
        image_file: str | None = Form(None)
):
    movie = Movie(title=title, director=director, year=year)
    return await create_movie(movie)

@router.get("/movies", response_model=list[Movie])
async def get_movies(
        skip:int=Query(0, ge=0),
        limit:int=Query(10, le=100),
        title: Optional[str]=None,
        year: Optional[int]=None,
        director: Optional[str]=None
):

    return await read_movies(skip=skip, limit=limit, title=title, year=year, director=director)