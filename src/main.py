"""Эмулятор командной оболочки UNIX. Этап 1: REPL."""

import os
import socket
import sys


def get_prompt():
    """
    Формирует приглашение к вводу.

    Returns:
        str: Строка вида username@hostname:cwd$
    """
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


def repl():
    """Основной цикл Read-Eval-Print Loop."""
    while True:
        try:
            line = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as exc:
            print(f"Input error: {exc}", file=sys.stderr)
            continue

        try:
            command, args = parse_command(line)
        except Exception as exc:
            print(f"Parse error: {exc}", file=sys.stderr)
            continue

        if command is None:
            continue

        if command == "exit":
            break

        try:
            execute(command, args)
        except Exception as exc:
            print(f"Command error: {exc}", file=sys.stderr)


def main():
    """Точка входа."""
    repl()


if __name__ == "__main__":
    main()
