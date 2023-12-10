from pathlib import Path
import sys
import string
import os
import shutil
import zipfile
import tarfile
from concurrent.futures import ThreadPoolExecutor
import logging

CATEGORIES = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"],
}
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
TRANS = {}
result_know = []
result_dont_know = []
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
punct = string.punctuation + " "


def normalize(name: str):
    ext = name[name.rfind(".") :]
    n = name[: name.rfind(".")]
    name_out = ""
    for i in name:
        if i in punct:
            n = n.replace(i, "_")
    name_out = n + ext
    return name_out.translate(TRANS)


def delete_dir(path: Path):
    for root, dirs, _ in os.walk(path, topdown=False):
        for d in dirs:
            p = os.path.join(root, d)
            if not os.listdir(p):
                os.rmdir(p)


def get_categories(file: Path):
    ext = file.suffix.lower()
    for cat, exst in CATEGORIES.items():
        if ext in exst:
            result_know.append(ext)
            print(cat, file)
            return cat
    result_dont_know.append(ext)
    print("Other", file)
    return "Other"


def move_file(file: Path, category, root_dir: Path):
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(normalize(file.name)))


def process_file(file):
    category = get_categories(file)
    move_file(file, category, path)


def archives_unpack(sort_folder: Path):
    try:
        for root, _, files in os.walk(sort_folder):
            for file in files:
                if file.endswith(".zip"):
                    with zipfile.ZipFile(os.path.join(root, file), "r") as zip_ref:
                        zip_ref.extractall(os.path.join(root, file[:-4]))
                elif file.endswith((".tar", ".gz")):
                    with tarfile.open(os.path.join(root, file), "r") as tar_ref:
                        tar_ref.extractall(os.path.join(root, file[:-7]))
    except (shutil.ReadError, zipfile.BadZipFile, tarfile.ReadError):
        return None


def sort_folder(path: Path):
    with ThreadPoolExecutor() as executor:
        for element in path.glob("**/*"):
            if element.is_file():
                executor.submit(process_file,element)


def main():
    global path
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "Not param for folder"
    if not path.exists():
        return "Folder is not exists"
    with ThreadPoolExecutor() as executor:
        pass
    
    sort_folder(path)
    delete_dir(path)
    archives_unpack(path)


if __name__ == "__main__":
    print(main())
    print(f"Not idintifield {set(result_know)}")
    print(f"Idintifield {set(result_dont_know)}")
