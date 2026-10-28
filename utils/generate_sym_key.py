import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESSIV

OUTPUT_FILE_NAME_NOT_PROVIDED = 1
OUTPUT_FILE_IS_NOT_AVAILABLE_ERROR = 2

SCRIPT_DIR = Path(__file__).resolve().parent
SECRET_DIR = SCRIPT_DIR.parent / "secrets"


def generate_sym_key():
    return AESSIV.generate_key(bit_length=256)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Ожидалось имя выходного файла в качестве параметра")
        sys.exit(OUTPUT_FILE_NAME_NOT_PROVIDED)

    SECRET_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(SECRET_DIR / sys.argv[1], "w") as f:
            f.write(generate_sym_key().hex())
    except FileNotFoundError:
        print("Ключ не был сгенерирован: ожибка доступа к файлу", file=sys.stderr)
        sys.exit(OUTPUT_FILE_IS_NOT_AVAILABLE_ERROR)

    print("Ключ был успешно сгенерирован")
    print()

    try:
        with open(SCRIPT_DIR / "generate_sym_key_warning.txt") as f:
            print(f.read())
    except FileNotFoundError:
        pass
