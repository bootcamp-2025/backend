import io, os
from minio import Minio
from minio.commonconfig import ENABLED
from minio.error import S3Error


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

async def upload_image(id_movie: str, file)->str:
    data= await file.read()
    obj_name= f"{id_movie}/{file.filename}"

    client.put_object(BUCKET, obj_name, io.BytesIO(data), length=len(data))
    return obj_name