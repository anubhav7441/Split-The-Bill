import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"
    VISION_API_KEY = os.environ.get("VISION_API_KEY", "")
    VISION_MODEL = os.environ.get("VISION_MODEL", "claude-sonnet-4-5")
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg", "webp"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), "flask_session")
    SESSION_PERMANENT = False
