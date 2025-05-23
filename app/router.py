from fastapi import APIRouter, Query, Form, File, UploadFile
from typing import Optional
from app.models import Movie
from app.crud import read_movies, create_movie, find_movie, upload_movie_image
from app.storage import client, BUCKET

router=APIRouter()

@router.post("/movies", response_model=Movie)
async def post_movie(
        title: str = Form(None),
        director: str | None = Form(None),
        year: int | None = Form(None),
        image_file: UploadFile | None = File(None)
):
    movie = Movie(title=title, director=director, year=year)
    movie= await create_movie(movie)
    
    if image_file: 
        await upload_movie_image(movie.id, image_file)

    return movie

@router.get("/movies", response_model=list[Movie])
async def get_movies(
        skip:int=Query(0, ge=0),
        limit:int=Query(10, le=100),
        title: Optional[str]=None,
        year: Optional[int]=None,
        director: Optional[str]=None
):

    return await read_movies(skip=skip, limit=limit, title=title, year=year, director=director)


@router.get("/movies/{id_movie}", response_model=Movie)
async def get_movie(
        id_movie: str
):

    return await find_movie(id_movie)