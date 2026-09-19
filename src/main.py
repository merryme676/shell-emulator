#!/usr/bin/env python3
# ↑ Шебанг: говорит системе, что это Python 3-скрипт

"""
Эмулятор командной оболочки UNIX.

Этап 1: REPL с базовыми командами-заглушками.
"""
# ↑ Docstring модуля — описание всего файла


# Импорт os — для работы с переменными окружения и путями
import os
# Импорт socket — для получения имени хоста (компьютера)
import socket
# Импорт sys — для вывода ошибок в stderr (поток ошибок)
import sys


def get_prompt():
    """
    Формирует приглашение к вводу на основе реальных данных ОС.

    Returns:
        str: Приглашение в формате username@hostname:cwd$
    """
    # ↑ Docstring: что делает функция и что возвращает

    # Пытаемся получить имя пользователя:
    # 1) из USER, 2) из LOGNAME, 3) запасное значение "user"
    username = os.getenv("USER") or os.getenv("LOGNAME") or "user"

    # Получаем имя хоста (например, "MacBook-Air-Meri")
    hostname = socket.gethostname()

    # Получаем текущую рабочую директорию (где сейчас программа)
    cwd = os.getcwd()

    # Получаем путь к домашней папке (обычно /Users/имя)
    home = os.path.expanduser("~")

    # Если мы внутри домашней папки — сокращаем путь до ~/...
    # (проверка "home and ..." защищает от пустой home)
    if home and cwd.startswith(home):
        # Отрезаем домашнюю часть и добавляем ~ в начало
        cwd = "~" + cwd[len(home):]

    # Собираем всё в строку вида meri@MacBook:~$
    return f"{username}@{hostname}:{cwd}$ "


def parse_command(line):
    """
    Разбирает строку ввода на команду и аргументы.

    Args:
        line (str): Строка, введённая пользователем.

    Returns:
        tuple: (команда, список аргументов) или (None, []) если пусто.
    """
    # strip() убирает пробелы по краям,
    # split() разбивает по любым пробельным символам
    # "ls  -la  /tmp" → ["ls", "-la", "/tmp"]
    parts = line.strip().split()

    # Если пользователь ввёл только пробелы — список пустой
    if not parts:
        return None, []

    # parts[0] — команда, parts[1:] — аргументы
    return parts[0], parts[1:]


def cmd_ls(args):
    """
    Заглушка команды ls.

    Args:
        args (list): Аргументы команды.
    """
    # Этап 1: просто печатаем имя команды и её аргументы
    print(f"ls: {args}")


def cmd_cd(args):
    """
    Заглушка команды cd.

    Args:
        args (list): Аргументы команды.
    """
    # Этап 1: то же самое — печатаем имя и аргументы
    print(f"cd: {args}")


def execute(command, args):
    """
    Выполняет команду по её имени.

    Args:
        command (str): Имя команды.
        args (list): Список аргументов.
    """
    # Если команда ls — вызываем заглушку ls
    if command == "ls":
        cmd_ls(args)
    # Если команда cd — вызываем заглушку cd
    elif command == "cd":
        cmd_cd(args)
    # Иначе — команда неизвестна
    else:
        print(f"{command}: command not found")


def repl():
    """Основной цикл Read-Eval-Print Loop."""
    # REPL: Read → Eval → Print → Loop
    # Работает, пока пользователь не введёт exit

    # Бесконечный цикл
    while True:
        try:
            # input() показывает приглашение и ждёт ввода
            line = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D (EOFError) или Ctrl+C (KeyboardInterrupt)
            print()   # пустая строка для аккуратности
            break     # выходим из цикла
        except Exception as exc:
            # Любая другая ошибка чтения — не падаем
            print(f"Input error: {exc}", file=sys.stderr)
            continue  # продолжаем цикл

        # Разбираем ввод на команду и аргументы — тоже в try
        try:
            command, args = parse_command(line)
        except Exception as exc:
            # Если парсер сломался — сообщаем и продолжаем
            print(f"Parse error: {exc}", file=sys.stderr)
            continue

        # Пустая строка — просто пропускаем
        if command is None:
            continue

        # Команда exit — выходим из цикла
        if command == "exit":
            break

        # Выполняем команду — в try, чтобы не упасть при ошибке
        try:
            execute(command, args)
        except Exception as exc:
            # Если команда упала — печатаем ошибку и продолжаем
            print(f"Command error: {exc}", file=sys.stderr)


def main():
    """Точка входа."""
    # Запускаем основной цикл
    repl()


# Выполняется, только если файл запущен напрямую
if __name__ == "__main__":
    main()
