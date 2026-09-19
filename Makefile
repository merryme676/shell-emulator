# Makefile — автоматизация команд для проекта.
# Использование:
#   make run    — запустить эмулятор
#   make test   — запустить тесты
#   make lint   — проверить стиль кода
#   make clean  — очистить кэш

# .PHONY — объявляем, что цели run/test/lint/clean —
# это НЕ файлы, а просто команды.
# Без этого make будет искать файлы с такими именами.
.PHONY: run test lint clean

# make run — запускает эмулятор
# Отступы в Makefile — ТАБЫ, не пробелы!
run:
	python3 src/main.py

# make test — запускает тесты через pytest
# -v — подробный вывод (verbose)
test:
	python3 -m pytest tests/ -v

# make lint — проверяет стиль кода через flake8
# --max-line-length=80 — строки не длиннее 80 символов (правило Р2)
lint:
	python3 -m flake8 src/ tests/ --max-line-length=80

# make clean — удаляет кэш Python (__pycache__ и *.pyc)
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
