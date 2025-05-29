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

async def update_movie(
    movie_id: PydanticObjectId,
    data: MovieUpdate,
    image_file: UploadFile | None = None
) -> Movie | None:
    movie = await Movie.get(movie_id)
    if not movie:
        return None

    # Aquí accedemos correctamente al dict
    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(movie, field, value)

    if image_file:
        # Borrar imagen anterior si existe
        if movie.image:
            await delete_image_from_minio(movie.image)
            await delete_movie_directory(str(movie.id, image_file))

        # Subir nueva imagen
        image_path = await upload_image(str(movie.id), image_file)
        movie.image = image_path

    await movie.save()
    return movie

async def remove_movie(movie_id: str) -> bool:
    movie = await Movie.get(movie_id)
    if not movie:
        return False
    # Eliminar imagen si existe
    if movie.image:
        await delete_image_from_minio(movie.image)

    if movie.image:
        await delete_movie_directory(str(movie.id))

    # Eliminar la película
    await movie.delete()
    return True

async def delete_bucket(bucket_name: str) -> None:
    try:
        # Eliminar objetos dentro del bucket
        objects = client.list_objects(bucket_name, recursive=True)
        for obj in objects:
            await asyncio.to_thread(client.remove_object, bucket_name, obj.object_name)

        # Eliminar el bucket
        await asyncio.to_thread(client.remove_bucket, bucket_name)
        print(f"Bucket '{bucket_name}' eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el bucket: {e}")

#opción para mostrar todas las películas
async def get_all_movies():
    return await Movie.find_all().to_list()