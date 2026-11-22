import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".c", ".h", ".js", ".html", ".css"],
}

EXT_MAP = {}
for category, extensions in CATEGORIES.items():
    for ext in extensions:
        EXT_MAP[ext] = category


def get_unique_path(destination):
    if not destination.exists():
        return destination
    counter = 1
    while True:
        new_path = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not new_path.exists():
            return new_path
        counter += 1


def organize(folder):
    moved = 0
    skipped = 0
    errors = 0
    summary = {}

    with os.scandir(folder) as entries:
        files = [e for e in entries if e.is_file()]

    for entry in files:
        if entry.name in ("organizer.py", "organizer.log"):
            continue

        ext = Path(entry.name).suffix.lower()
        category = EXT_MAP.get(ext)

        if category is None:
            skipped += 1
            logging.info(f"Skipped (unknown type): {entry.name}")
            continue

        target_folder = Path(folder) / category
        target_folder.mkdir(exist_ok=True)
        destination = get_unique_path(target_folder / entry.name)

        try:
            shutil.move(entry.path, str(destination))
            moved += 1
            summary[category] = summary.get(category, 0) + 1
            logging.info(f"Moved: {entry.name} -> {destination}")
        except PermissionError:
            errors += 1
            logging.error(f"Permission denied: {entry.name}")
        except FileExistsError:
            errors += 1
            logging.error(f"File already exists: {entry.name}")
        except OSError as e:
            errors += 1
            logging.error(f"Error moving {entry.name}: {e}")

    print("\n===== Execution Summary =====")
    for category, count in summary.items():
        print(f"{category:<12}: {count}")
    print("-----------------------------")
    print(f"Total moved   : {moved}")
    print(f"Skipped       : {skipped}")
    print(f"Errors        : {errors}")
    print("Log file      : organizer.log")


if __name__ == "__main__":
    path = input("Enter folder path (press Enter for Downloads): ").strip()
    if path == "":
        path = str(Path.home() / "Downloads")

    if not os.path.isdir(path):
        print("Invalid folder path!")
    else:
        organize(path)