import hashlib
from pathlib import Path


# Should be async too.
def generate_file_md5(path: Path, block_size=2**20) -> str:
    m = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def remove_file(sender, **kwargs):
    print("Removing file")
    print(sender)
    print(kwargs)

    return
    # downloads_directory = user.download_path()
    # file_path = downloads_directory / upload.filename

    # try:
    #     file_path.unlink()
    # except FileNotFoundError:
    #     print(f"File {upload.filename} does not exist.")
