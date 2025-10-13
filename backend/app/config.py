from pathlib import Path
from pydantic_settings import BaseSettings



BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = BASE_DIR / "app" / "templates" / "template.docx"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_DOCX_DIR = OUTPUT_DIR / "docx"
OUTPUT_DOCX_DIR.mkdir(exist_ok=True)

OUTPUT_PDF_DIR = OUTPUT_DIR / "pdf"
OUTPUT_PDF_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
