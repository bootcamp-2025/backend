from app.models import Movie, MovieUpdate
from app.storage import upload_image, delete_image_from_minio
from beanie import PydanticObjectId
from typing import Optional
from fastapi import UploadFile

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

async def upload_movie_image(
        movie_id: str,
        file: UploadFile
)->str:
    obj_name= await upload_image(movie_id, file)  
    return obj_name

async def find_movie(
        id_movie: str
):
    return await Movie.get(id_movie)

async def update_movie(movie_id: PydanticObjectId, data: MovieUpdate) -> Movie | None:
    movie = await Movie.get(movie_id)
    if not movie:
        return None

    update_data = data.dict(exclude_unset=True)  # Solo los campos que sí se enviaron
    for field, value in update_data.items():
        setattr(movie, field, value)

    await movie.save()
    return movie

async def remove_movie(movie_id: str) -> bool:
    movie = await Movie.get(movie_id)
    if not movie:
        return False
    # Eliminar imagen si existe
    if movie.image:
        await delete_image_from_minio(movie.image)

    # Eliminar la película
    await movie.delete()
    return True