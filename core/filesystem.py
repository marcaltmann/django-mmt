from django.conf import settings


def create_user_directories(username: str) -> None:
    user_files_path = settings.BASE_DIR / "user_files"

    user_directory = user_files_path / username
    uploads_directory = user_directory / "uploads"
    downloads_directory = user_directory / "downloads"
    uploads_directory.mkdir(parents=True, exist_ok=True)
    downloads_directory.mkdir(parents=True, exist_ok=True)
