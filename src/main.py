"""Эмулятор командной оболочки UNIX. Этап 2: конфигурация."""

import argparse
import os
import socket
import sys


def parse_args():
    """
    Разбирает параметры командной строки.

    Returns:
        argparse.Namespace: объект с полями vfs, prompt, script.
    """
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки UNIX",
    )
    parser.add_argument(
        "--vfs",
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--prompt",
        help="Пользовательское приглашение к вводу",
    )
    parser.add_argument(
        "--script",
        help="Путь к стартовому скрипту",
    )
    return parser.parse_args()


def print_debug(args):
    """
    Отладочный вывод параметров при запуске.

    Args:
        args: объект с полями vfs, prompt, script.
    """
    print("=== Параметры запуска ===")
    print(f"VFS:    {args.vfs}")
    print(f"Prompt: {args.prompt}")
    print(f"Script: {args.script}")
    print("=========================")


def get_prompt(custom_prompt=None):
    """
    Формирует приглашение к вводу.

    Args:
        custom_prompt: пользовательское приглашение (или None).

    Returns:
        str: строка приглашения.
    """
    if custom_prompt:
        return custom_prompt

    username = os.getenv("USER") or os.getenv("LOGNAME") or "user"
    hostname = socket.gethostname()
    cwd = os.getcwd()
    home = os.path.expanduser("~")

    if home and cwd.startswith(home):
        cwd = "~" + cwd[len(home):]

    return f"{username}@{hostname}:{cwd}$ "


def parse_command(line):
    """
    Разбирает строку ввода на команду и аргументы.

    Args:
        line: строка, введённая пользователем.

    Returns:
        Кортеж (команда, [аргументы]) или (None, []) если пусто.
    """
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def cmd_ls(args):
    """
    Заглушка команды ls.

    Args:
        args: список аргументов команды.
    """
    print(f"ls: {args}")


def cmd_cd(args):
    """
    Заглушка команды cd.

    Args:
        args: список аргументов команды.
    """
    print(f"cd: {args}")


def execute(command, args):
    """
    Выполняет команду по имени.

    Args:
        command: имя команды.
        args: список аргументов.
    """
    if command == "ls":
        cmd_ls(args)
    elif command == "cd":
        cmd_cd(args)
    else:
        print(f"{command}: command not found")


def process_line(line, custom_prompt=None):
    """
    Обрабатывает одну строку ввода.

    Args:
        line: строка с командой.
        custom_prompt: приглашение (для отображения в скрипте).

    Returns:
        bool: True если нужно продолжать, False если выход.
    """
    try:
        command, args = parse_command(line)
    except Exception as exc:
        print(f"Parse error: {exc}", file=sys.stderr)
        return True

    if command is None:
        return True

    if command == "exit":
        return False

    try:
        execute(command, args)
    except Exception as exc:
        print(f"Command error: {exc}", file=sys.stderr)

    return True


def read_script_file(path):
    """
    Читает файл стартового скрипта.

    Args:
        path: путь к файлу.

    Returns:
        list: список строк или None при ошибке.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {path}", file=sys.stderr)
        return None
    except Exception as exc:
        print(f"Ошибка чтения скрипта: {exc}", file=sys.stderr)
        return None


def report_script_error(line_number, message):
    """
    Сообщает об ошибке в стартовом скрипте.

    Args:
        line_number: номер строки в файле.
        message: описание ошибки.
    """
    print(
        f"[Ошибка скрипта, строка {line_number}]: {message}",
        file=sys.stderr,
    )


def process_script_line(line, line_number, known_commands):
    """
    Обрабатывает одну строку стартового скрипта.

    Args:
        line: строка из файла.
        line_number: номер строки в файле.
        known_commands: кортеж известных команд.

    Returns:
        int: 0 если успех, 1 если ошибка.
    """
    stripped = line.strip()
    if not stripped:
        return 0
    if stripped.startswith("#"):
        return 0
    print(f">>> {stripped}")
    try:
        command, args = parse_command(stripped)
    except Exception as exc:
        report_script_error(line_number, f"не удалось разобрать: {exc}")
        return 1
    if command is None:
        return 0

    if command == "exit":
        print("(скрипт остановлен командой exit)")
        return -1

    if command not in known_commands:
        report_script_error(line_number, f"неизвестная команда: {command}")
        return 1

    try:
        execute(command, args)
    except Exception as exc:
        report_script_error(line_number, f"команда упала: {exc}")
        return 1

    return 0


def run_script(path):
    """
    Выполняет команды из стартового скрипта.

    Args:
        path: путь к файлу скрипта.
    """
    lines = read_script_file(path)
    if lines is None:
        return

    known_commands = ("ls", "cd")
    errors_count = 0

    for line_number, line in enumerate(lines, start=1):
        result = process_script_line(line, line_number, known_commands)

        if result == -1:
            break

        if result == 1:
            errors_count += 1

    if errors_count > 0:
        print(f"Всего ошибок в скрипте: {errors_count}", file=sys.stderr)


def repl(custom_prompt=None):
    """
    Основной цикл Read-Eval-Print Loop.

    Args:
        custom_prompt: пользовательское приглашение (или None).
    """
    while True:
        try:
            line = input(get_prompt(custom_prompt))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as exc:
            print(f"Input error: {exc}", file=sys.stderr)
            continue

        if not process_line(line):
            break


def main():
    """Точка входа."""
    args = parse_args()
    print_debug(args)

    if args.script:
        run_script(args.script)

    repl(args.prompt)


if __name__ == "__main__":
    main()
