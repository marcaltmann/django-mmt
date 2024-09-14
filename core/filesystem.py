import hashlib
from pathlib import Path

from django.conf import settings


def create_user_directories(username: str) -> None:
    user_files_path = settings.BASE_DIR / "user_files"

    user_directory = user_files_path / username
    uploads_directory = user_directory / "uploads"
    downloads_directory = user_directory / "downloads"
    uploads_directory.mkdir(parents=True, exist_ok=True)
    downloads_directory.mkdir(parents=True, exist_ok=True)


def generate_file_md5(path: Path, block_size=2**20) -> str:
    m = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def get_upload_path(username: str) -> Path:
    return settings.BASE_DIR / "user_files" / username / "uploads"


def get_download_path(username: str) -> Path:
    return settings.BASE_DIR / "user_files" / username / "downloads"
