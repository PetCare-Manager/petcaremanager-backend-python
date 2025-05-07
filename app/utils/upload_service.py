from fastapi import UploadFile, HTTPException
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

async def upload_to_cloudinary(file: UploadFile, folder: str) -> str:
    """
    Sube el UploadFile a Cloudinary bajo el folder dado.
    Si la extensión no es de imagen, usa resource_type="raw" para conservar formatos.
    Devuelve la URL segura con extensión.
    """
    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            resource_type="auto"
        )
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo archivo: {e}")
