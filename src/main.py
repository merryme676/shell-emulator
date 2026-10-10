"""Эмулятор командной оболочки UNIX. Этап 2: конфигурация."""

import argparse
import base64
import os
import socket
import sys
import xml.etree.ElementTree as ET


CURRENT_VFS = None
CURRENT_DIR = None
START_TIME = None
HISTORY = []


class VfsNode:
    """
    Узел виртуальной файловой системы.

    Может быть папкой (is_dir=True) или файлом (is_dir=False).
    """

    def __init__(self, name, is_dir=False, parent=None):
        """
        Создаёт узел.

        Args:
            name: имя узла (папки или файла).
            is_dir: True если папка, False если файл.
            parent: родительский узел (или None для корня).
        """
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children = {}
        self.content = ""

    def add_child(self, node):
        """
        Добавляет дочерний узел.

        Args:
            node: узел для добавления.
        """
        self.children[node.name] = node
        node.parent = self

    def find_child(self, name):
        """
        Ищет дочерний узел по имени.

        Args:
            name: имя дочернего узла.

        Returns:
            VfsNode или None, если не найдено.
        """
        return self.children.get(name)

    def get_path(self):
        """
        Возвращает полный путь от корня.

        Returns:
            str: путь вида "/home/user/file.txt".
        """
        if self.parent is None:
            return "/"

        parts = []
        current = self
        while current.parent is not None:
            parts.append(current.name)
            current = current.parent

        return "/" + "/".join(reversed(parts))


def load_vfs(path):
    """
    Загружает VFS из XML-файла.

    Args:
        path: путь к XML-файлу.

    Returns:
        VfsNode или None при ошибке.
    """
    try:
        tree = ET.parse(path)
    except FileNotFoundError:
        print(f"Ошибка: файл VFS не найден: {path}", file=sys.stderr)
        return None
    except ET.ParseError as exc:
        print(f"Ошибка формата XML: {exc}", file=sys.stderr)
        return None

    root_xml = tree.getroot()
    root = VfsNode(root_xml.get("name", "vfs"), is_dir=True)

    build_tree(root_xml, root)

    return root


def build_tree(xml_node, vfs_node):
    """
    Рекурсивно строит дерево VFS из XML.

    Args:
        xml_node: XML-элемент.
        vfs_node: соответствующий узел VFS.
    """
    for child in xml_node:
        name = child.get("name", "unknown")

        if child.tag == "dir":
            dir_node = VfsNode(name, is_dir=True)
            vfs_node.add_child(dir_node)
            build_tree(child, dir_node)

        elif child.tag == "file":
            file_node = VfsNode(name, is_dir=False)
            file_node.content = decode_content(child)
            vfs_node.add_child(file_node)


def decode_content(xml_node):
    """
    Декодирует содержимое файла из XML.

    Args:
        xml_node: XML-элемент файла.

    Returns:
        str: содержимое файла.
    """
    text = (xml_node.text or "").strip()
    encoding = xml_node.get("encoding", "text")

    if encoding == "base64":
        try:
            raw = base64.b64decode(text)
            return raw.decode("utf-8", errors="replace")
        except Exception as exc:
            print(f"Ошибка base64: {exc}", file=sys.stderr)
            return ""

    return text


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
    Команда ls: показывает содержимое текущей папки.

    Args:
        args: список аргументов (пока не используются).
    """
    if CURRENT_DIR is None:
        print(f"ls: {args}")
        return

    if not CURRENT_DIR.is_dir:
        print(f"{CURRENT_DIR.name}: не папка")
        return

    if not CURRENT_DIR.children:
        return

    for name in sorted(CURRENT_DIR.children):
        print(name)


def cmd_cd(args):
    """
    Команда cd: переходит в папку.

    Args:
        args: список аргументов. args[0] — путь.
    """
    global CURRENT_DIR

    if CURRENT_DIR is None:
        print(f"cd: {args}")
        return

    if not args:
        CURRENT_DIR = CURRENT_VFS
        return

    target = args[0]

    if target == "/":
        CURRENT_DIR = CURRENT_VFS
        return

    if target == "..":
        if CURRENT_DIR.parent is not None:
            CURRENT_DIR = CURRENT_DIR.parent
        return

    child = CURRENT_DIR.find_child(target)
    if child is None:
        print(f"cd: {target}: папка не найдена")
        return

    if not child.is_dir:
        print(f"cd: {target}: не папка")
        return

    CURRENT_DIR = child


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
    global CURRENT_VFS, CURRENT_DIR, START_TIME

    import time
    START_TIME = time.time()

    args = parse_args()
    print_debug(args)

    if args.vfs:
        vfs_root = load_vfs(args.vfs)
        if vfs_root is not None:
            CURRENT_VFS = vfs_root
            CURRENT_DIR = vfs_root
            print(f"VFS загружена: {vfs_root.name}")

    if args.script:
        run_script(args.script)

    repl(args.prompt)


if __name__ == "__main__":
    main()
