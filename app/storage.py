import io, os
from minio import Minio
from minio.commonconfig import ENABLED
from minio.error import S3Error
from fastapi import UploadFile


MINIO_ENDPOINT= os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY=os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.getenv("MINIO_SECRET_KEY")
BUCKET= "movies"

client= Minio(MINIO_ENDPOINT, 
              access_key=MINIO_ACCESS_KEY, 
              secret_key=MINIO_SECRET_KEY, 
              secure=False)

def init_storage(): 
    if not client.bucket_exists(BUCKET):
        client.make_bucket(BUCKET)
        client.set_bucket_versioning(
            BUCKET,
            {"Status": ENABLED}
        )

async def upload_image(movie_id: str, file: UploadFile)->str:
    data= await file.read()
    obj_name= f"{movie_id}/{file.filename}"

    client.put_object(
        BUCKET, obj_name, 
        io.BytesIO(data), 
        length=len(data),
        content_type=file.content_type
    )
    return obj_name

def delete_image_from_minio(obj_name: str) -> None:
    try:
        client.remove_object(BUCKET, obj_name)
    except Exception as e:
        print(f"Error al eliminar imagen de MinIO: {e}")