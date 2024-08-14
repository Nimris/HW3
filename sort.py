import shutil
import sys
from pathlib import Path
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from time import time
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def sort_dir(src_dir, dst_dir):
    for item in src_dir.iterdir():
        if item.name.startswith('$') or item.name.startswith('.'):
            continue  # Пропускаем системные и скрытые папки
        elif item.is_dir():
            sort_dir(item, dst_dir)
            #Thread(target=sort_dir, args=(item, dst_dir)).start()
        elif item.is_file():
            copy_file(item, dst_dir)
            extention_dir = Path(dst_dir) / Path(item.suffix.replace(".", ""))
            extention_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(item, extention_dir)

def copy_file(file, dst_dir):
    ext_dir = dst_dir / file.suffix.lstrip(".")
    ext_dir.mkdir(parents=True, exist_ok=True)
    try:
        if not (ext_dir / file.name).exists():
            shutil.copy(file, ext_dir / file.name)
    except shutil.Error as e:
        logging.error(f"Failed to copy {file}: {e}")

def main():
    if len(sys.argv) < 2:
        logging.error("Please provide source and (optional) destination directories.")
        sys.exit(1)
    src_dir = Path(sys.argv[1]).resolve()
    dst_dir = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else src_dir / 'dist'

    if not src_dir.exists():
        logging.error(f"The source path '{src_dir}' does not exist.")
        sys.exit(1)
    
    with ThreadPoolExecutor() as executor:
        executor.submit(sort_dir, src_dir, dst_dir)
    
    sort_dir(src_dir, dst_dir)
    logging.info(f"Files copied from {src_dir} and sorted to {dst_dir}.")
    
    
if __name__ == '__main__':
    start = time()
    main()
    end = time()
    logging.info(f"Execution time: {end - start:.2f} seconds.")