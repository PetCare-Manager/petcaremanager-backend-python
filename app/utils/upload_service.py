from fastapi import UploadFile, HTTPException
import cloudinary.uploader

async def upload_to_cloudinary(file: UploadFile, folder: str) -> tuple[str, str]:
    """
    Sube el UploadFile a Cloudinary bajo el folder dado
    y devuelve la URL segura.
    """
    try:
        # file.file es un SpooledTemporaryFile
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            resource_type="auto"
        )
        return result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {e}")
