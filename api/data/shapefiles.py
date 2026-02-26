import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_shapefiles():
    file_path = BASE_DIR / "tl_2025_28_tract.zip"
    try:
        with zipfile.ZipFile(file_path, mode="r") as archive:
            archive.printdir()

    except zipfile.BadZipFile as error:
        print(error)


get_shapefiles()
