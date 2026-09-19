"""Тесты для эмулятора shell."""

# Импортируем стандартные библиотеки
import sys
import os

# Добавляем корень проекта в путь поиска модулей.
# Без этого Python не найдёт src.main.
# os.path.dirname(__file__) — папка, где лежит этот файл (tests/).
# os.path.join(..., "..") — поднимаемся на уровень выше (в корень).
# os.path.abspath(...) — делаем путь абсолютным.
# sys.path.insert(0, ...) — добавляем в начало списка путей поиска.
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

# Импортируем функцию, которую тестируем
from src.main import parse_command  # noqa: E402


def test_parse_simple_command():
    """Простая команда без аргументов."""
    # "ls" → ("ls", [])
    assert parse_command("ls") == ("ls", [])


def test_parse_with_args():
    """Команда с аргументами."""
    # "ls -la /tmp" → ("ls", ["-la", "/tmp"])
    assert parse_command("ls -la /tmp") == ("ls", ["-la", "/tmp"])


def test_parse_empty():
    """Пустая строка."""
    # "" → (None, [])
    assert parse_command("") == (None, [])


def test_parse_whitespace():
    """Строка из пробелов."""
    # "   " → (None, [])
    assert parse_command("   ") == (None, [])


def test_parse_extra_spaces():
    """Много пробелов между аргументами."""
    # "ls   -la    /tmp" → ("ls", ["-la", "/tmp"])
    assert parse_command("ls   -la    /tmp") == ("ls", ["-la", "/tmp"])
