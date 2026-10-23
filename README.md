# Эмулятор shell

Эмулятор командной оболочки UNIX-подобной ОС.

## Требования

- Python 3.10+
- macOS / Linux

## Запуск

```bash
./run.sh
```

Или через Makefile:

```bash
make run
```

## Параметры командной строки

| Параметр | Описание | Пример |
|----------|----------|--------|
| `--vfs`  | Путь к VFS | `--vfs vfs/vfs.xml` |
| `--prompt` | Приглашение | `--prompt "my> "` |
| `--script` | Стартовый скрипт | `--script scripts/start.txt` |

Пример запуска со всеми параметрами:

```bash
./run.sh --vfs vfs/vfs.xml --prompt "my> " --script scripts/start.txt
```

## Команды

| Команда | Описание |
|---------|----------|
| `ls`    | Показать содержимое папки VFS |
| `cd`    | Перейти в папку VFS |
| `exit`  | Выход |
| `uptime` | Показать время работы |
| `history_list` | Показать историю команд |
| `mkdir` | Создать папку в VFS |
| `vfs-load` | Загрузить новую VFS из файла |

## Виртуальная файловая система (VFS)

Эмулятор работает с виртуальной файловой системой, которая
загружается из XML-файла. Все операции происходят **в памяти** —
реальные файлы на диске не изменяются.

### Формат XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<vfs name="test">
    <dir name="home">
        <file name="readme.txt">SGVsbG8=</file>
    </dir>
    <dir name="tmp" />
</vfs>
```

- `<vfs>` — корень VFS.
- `<dir name="...">` — папка.
- `<file name="...">` — файл.
- Атрибут `encoding="base64"` — для бинарных файлов.

### Тестовые VFS

| Файл | Что |
|------|-----|
| `vfs/minimal.xml` | Минимальный (1 файл) |
| `vfs/several.xml` | Несколько файлов в корне |
| `vfs/deep.xml` | 3+ уровня вложенности |
| `vfs/vfs.xml` | Основной тестовый VFS |

### Bash-скрипты для тестирования VFS

| Файл | Что делает |
|------|------------|
| `scripts/test_vfs_minimal.sh` | Тест `minimal.xml` |
| `scripts/test_vfs_several.sh` | Тест `several.xml` |
| `scripts/test_vfs_deep.sh` | Тест `deep.xml` |

## Тесты

```bash
make test
```

## Проверка стиля

```bash
make lint
```

## Этапы разработки

- [x] Этап 1. REPL
- [x] Этап 2. Конфигурация
- [x] Этап 3. VFS
- [x] Этап 4. Основные команды
- [x] Этап 5. Дополнительные команды
