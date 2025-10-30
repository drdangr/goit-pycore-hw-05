#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from typing import Dict, List


# parse a _single_ log line into its components
def parse_log_line(line: str) -> dict:
    """
    expects log line in format:
    DATE TIME LEVEL MESSAGE

    returns a dict with keys: date, time, level, message
    raises ValueError on malformed lines
    """
    
    # check for empty line and malformed lines
    line = line.strip() # remove leading/trailing whitespace
    if not line:
        raise ValueError("Порожня строка") # empty line

    parts = line.split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Невірний формат лога: {line!r}") # malformed line

    # if all ok - unpack parts
    date, time, level, message = parts
    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


# load logs from file
def load_logs(file_path: str) -> List[dict]:
    """
    reads the log file line by line,
    parses each line,
    returns a list of log records (dicts).
    if error - counts and reports malformed lines.
    """
    logs: List[dict] = []
    malformed = 0

    with open(file_path, "r", encoding="utf-8") as fh:
        for raw in fh:
            if not raw.strip():
                continue # skip empty lines
            try:
                logs.append(parse_log_line(raw))
            except ValueError:
                malformed += 1 # count malformed lines

    if malformed:
        print(f"skiped lines: {malformed}")
    return logs


# log filtering by level
def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    """
    filters log records by level (case-insensitive).
    returns a list of matching records.
    used lambda + filter for functional style.
    """
    lvl = level.upper()
    return list(filter(lambda r: r.get("level", "").upper() == lvl, logs))


# count logs by level
def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    """
    returns a dict with counts of log records per level.
    """
    counts: Dict[str, int] = {}
    for rec in logs:
        lvl = rec.get("level", "").upper()
        if not lvl:
            continue # skip records without level
        counts[lvl] = counts.get(lvl, 0) + 1 # increment count
    return counts


# print log counts table (even not standard levels)
def display_log_counts(counts: Dict[str, int]) -> None:
    """
    displays a table of log levels and their counts.
    orders standard levels first, then _others_ alphabetically.
    """
    standard_order = ["INFO", "DEBUG", "ERROR", "WARNING"]
    keys = set(counts.keys())
    ordered: List[str] = []

    # first add standard levels in order
    for lvl in standard_order:
        if lvl in keys:
            ordered.append(lvl)

    # second - add other levels alphabetically
    for lvl in sorted(keys):
        if lvl not in standard_order:
            ordered.append(lvl)

    print("Рівень логування | Кількість")
    print(f"{'-'*16}-|-----------") # 16 is length of "Рівень логування"

    for k in ordered:
        print(f"{k:<16} | {counts.get(k, 0)}") # print count or 0


# CLI argument parser
def make_argparser() -> argparse.ArgumentParser:
    '''
    creates and returns the argument parser.
    using _argparse_ module. 
    '''
    # create parser with description for help
    p = argparse.ArgumentParser(
        description="Аналіз лог-файлів: статистика за рівнями та фільтрація за рівнем."
    )
    # adding first agument: file path
    p.add_argument("file", help="Шлях до файлу логів (UTF-8).")
    # optional second argument: level
    p.add_argument("level", nargs="?", help="(необов'язково) рівень логування для детального виводу: info/error/debug/warning/…",)
    return p


def main() -> None:
    parser = make_argparser()
    args = parser.parse_args()

    file_path: str = args.file
    user_level: str | None = args.level # optional!, may be None

    # Check if file exists and is a file
    if not os.path.exists(file_path):
        print(f"Файл не знайдено: {file_path}")
        return
    if not os.path.isfile(file_path):
        print(f"Це не файл: {file_path}")
        return

    # Load logs from file and handle read errors
    try:
        logs = load_logs(file_path)
    except (OSError, UnicodeError) as e:
        print(f"Помилка читання файлу: {e}")
        return

    # Count and display log levels
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # If user specified a level, filter and display those logs
    if user_level:
        level_logs = filter_logs_by_level(logs, user_level)
        print(f"\nДеталі логів для рівня '{user_level.upper()}':")

        # display filtered logs or message if none
        if not level_logs:
            print("(немає записів)")
        else:
            for rec in level_logs:
                print(f"{rec['date']} {rec['time']} - {rec['message']}")


if __name__ == "__main__":
    main()
