import re
import shutil
import threading
import logging
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Функція normalize
def normalize(filename):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    normalize_filename = filename.translate(TRANS) #транслітерація
    normalize_filename = normalize_filename.replace(r'[^A-Za-z0-9.]+', "_") #заміна не літер та не цифр на симовл "_"
    return normalize_filename

# Функція сортування та переміщення файлів
def sort_and_move_files(folder_path):
    image_ext = ['JPEG', 'PNG', 'JPG', 'SVG']
    document_ext = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    audio_ext = ['MP3', 'OGG', 'WAV', 'AMR']
    video_ext = ['AVI', 'MP4', 'MOV', 'MKV']
    archive_ext = ['ZIP', 'GZ', 'TAR']

    for file in folder_path.iterdir():
        if file.is_file():
            ext = file.suffix[1:].upper()
            if ext in image_ext:
                folder = 'images'
            elif ext in document_ext:
                folder = 'documents'
            elif ext in audio_ext:
                folder = 'audio'
            elif ext in video_ext:
                folder = 'video'
            elif ext in archive_ext:
                folder = 'archives'
            else:
                folder = 'other'

            new_filename = normalize(file.name)
            dest_folder = folder_path / folder
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(dest_folder / new_filename))
            logger.info(f'Moved "{file}" to "{dest_folder / new_filename}"')  #  логування

    # Після переміщення файлів перевіряємо порожність папки
    if not list(folder_path.iterdir()):
        logger.info(f'Removing empty folder: {folder_path}')
        folder_path.rmdir()

# Головна функція для обробки папки "Хлам"
def process_junk_folder(folder_path):
    threads = []
    for item in folder_path.iterdir():
        if item.is_dir():
            thread = threading.Thread(target=sort_and_move_files, args=(item,))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    user_input = input("Enter your path for sorted folder: ")
    junk_folder = Path(user_input)

    process_junk_folder(junk_folder)
    