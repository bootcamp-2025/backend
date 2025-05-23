from app.models import Movie
from app.storage import upload_image
from fastapi import UploadFile
from typing import Optional

async def read_movies(
        skip:int=0,
        limit:int=10,
        title: Optional[str]=None,
        year: Optional[str]=None,
        director: Optional[str]=None
):
    query={}
    if title: 
        query["title"] = {"$regex": title, "$options": "i"}

    if year: 
        query["year"] = int(year)

    if director: 
        query["director"] = {"$regex": director, "$options": "i"}

    return await Movie.find(query).skip(skip).limit(limit).to_list()

async def create_movie(
       movie: Movie        
)->Movie:
    movie.id= None
    return await movie.insert()

async def find_movie(
        id_movie: str
):
    return await Movie.get(id_movie)

async def upload_movie_image(
        id_movie: str,
        file: UploadFile
)->str:
    obj_name= await upload_image(id_movie, file)  
    return obj_name