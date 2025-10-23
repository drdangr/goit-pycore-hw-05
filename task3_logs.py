#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Dict, List
import os

# --- 4. Парсинг одного рядка логу ---
def parse_log_line(line: str) -> dict:
    """
    Принимает строку лога формата:
    'YYYY-MM-DD HH:MM:SS LEVEL Message...'
    Возвращает словарь с ключами: date, time, level, message.
    Бросает ValueError, если строка не соответствует формату.
    """
    line = line.strip()
    if not line:
        raise ValueError("Пустая строка.")

    parts = line.split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Неверный формат лога: {line}")

    date, time, level, message = parts[0], parts[1], parts[2], parts[3]
    return {"date": date, "time": time, "level": level.upper(), "message": message}


# --- 5. Загрузка всех логов из файла ---
def load_logs(file_path: str) -> List[dict]:
    """
    Читает файл построчно, парсит каждую строку через parse_log_line.
    Пропускает пустые/битые строки, но НЕ падает.
    """
    logs: List[dict] = []
    malformed = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for raw in f:
            if not raw.strip():
                continue
            try:
                logs.append(parse_log_line(raw))
            except ValueError:
                malformed += 1
                # Можно логировать в stderr, но по заданию достаточно аккуратно игнорировать

    if malformed:
        print(f"⚠️ Пропущено некорректных строк: {malformed}")
    return logs


# --- 6. Фильтрация по уровню ---
def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    """
    Возвращает только записи с указанным уровнем (без учёта регистра).
    Использует функциональный стиль: filter + lambda.
    """
    lvl = level.upper()
    return list(filter(lambda rec: rec.get("level", "").upper() == lvl, logs))


# --- 7. Подсчёт количества по уровням ---
def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    """
    Считает количество записей для каждого уровня.
    Инициализируем стандартные уровни нулями,
    но также учитываем любые встреченные нестандартные уровни.
    """
    counts: Dict[str, int] = {lvl: 0 for lvl in ("INFO", "ERROR", "DEBUG", "WARNING")}
    for rec in logs:
        lvl = rec.get("level", "").upper()
        if not lvl:
            continue
        counts[lvl] = counts.get(lvl, 0) + 1
    return counts


# --- 8. Печать таблицы со статистикой ---
def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Выводит аккуратную таблицу: уровень | количество.
    Вначале стандартные уровни в фиксированном порядке,
    затем (если есть) нестандартные — по алфавиту.
    """
    standard_order = ["INFO", "DEBUG", "ERROR", "WARNING"]

    # Соберём итоговый порядок ключей
    present_keys = set(counts.keys())
    ordered = [lvl for lvl in standard_order if lvl in present_keys]
    extra = sorted(present_keys - set(standard_order))
    ordered.extend(extra)

    title_a, title_b = "Рівень логування", "Кількість"
    width_a = max(len(title_a), max((len(k) for k in ordered), default=0))
    width_b = len(title_b)

    print(f"{title_a:<{width_a}} | {title_b:<{width_b}}")
    print(f"{'-'*width_a}-|-{'-'*width_b}")
    for key in ordered:
        print(f"{key:<{width_a}} | {counts.get(key, 0):<{width_b}}")


def _print_level_details(level: str, logs: List[dict]) -> None:
    """Печатает раздел с подробностями по выбранному уровню."""
    if not logs:
        print(f"\nДеталі логів для рівня '{level.upper()}':\n(немає записів)")
        return

    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for rec in logs:
        print(f"{rec['date']} {rec['time']} - {rec['message']}")


def make_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Аналіз лог-файлів: статистика за рівнями та фільтрація за рівнем."
    )
    parser.add_argument(
        "file",
        help="Шлях до файлу логів (UTF-8)."
    )
    parser.add_argument(
        "level",
        nargs="?",
        help="(необов'язково) рівень логування для детального виводу (напр., info/error/debug/warning)"
    )
    return parser


def main() -> None:
    parser = make_argparser()
    args = parser.parse_args()

    file_path: str = args.file
    user_level: str | None = args.level

    # 1/9. Проверка существования файла + обработка ошибок чтения.
    if not os.path.exists(file_path):
        print(f"❌ Файл не знайдено: {file_path}")
        return
    if not os.path.isfile(file_path):
        print(f"❌ Це не файл: {file_path}")
        return

    try:
        logs = load_logs(file_path)
    except (OSError, UnicodeError) as e:
        print(f"❌ Помилка читання файлу: {e}")
        return

    # 3/7/8. Подсчёт и вывод таблицы
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # 2. Если пользователь указал уровень — вывод подробностей
    if user_level:
        level_logs = filter_logs_by_level(logs, user_level)
        _print_level_details(user_level, level_logs)


if __name__ == "__main__":
    main()
