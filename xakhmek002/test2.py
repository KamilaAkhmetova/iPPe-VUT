import sys

# Проверка на количество аргументов
if len(sys.argv) < 2:
    print("Usage: python test.py <program_file>")
    sys.exit(1)

# Извлекаем имя файла программы (XML) из аргументов командной строки
program = sys.argv[1]

# Чтение содержимого файла
try:
    with open(program, 'r', encoding='utf-8') as f:
        file_content = f.read()
    print(file_content)  # Вывод содержимого файла в консоль
except FileNotFoundError:
    print(f"Error: {program} not found.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
