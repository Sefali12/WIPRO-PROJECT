"""
csv_reader.py
-------------
Loads data/test_data.csv into a list of dicts so tests can be
parametrized (data-driven testing) instead of hardcoding search terms.
"""

import csv
import os


def read_csv(filename: str = "test_data.csv"):
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", filename
    )
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
