import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()  # Carga automáticamente tu .env

cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key    = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure     = os.getenv("CLOUDINARY_SECURE", "true").lower() in ["true", "1", "yes"]
)
