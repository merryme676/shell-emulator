"""Тесты для эмулятора shell"""

import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from src.main import parse_command


def test_parse_simple_command():
    """Простая команда без аргументов."""
    assert parse_command("ls") == ("ls", [])


def test_parse_with_args():
    """Команда с аргументами."""
    assert parse_command("ls -la /tmp") == ("ls", ["-la", "/tmp"])


def test_parse_empty():
    """Пустая строка."""
    assert parse_command("") == (None, [])


def test_parse_whitespace():
    """Строка из пробелов."""
    assert parse_command("   ") == (None, [])


def test_parse_extra_spaces():
    """Много пробелов между аргументами."""
    assert parse_command("ls   -la    /tmp") == ("ls", ["-la", "/tmp"])
