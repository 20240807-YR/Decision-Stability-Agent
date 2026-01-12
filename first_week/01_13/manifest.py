from pathlib import Path

# manifest.py 위치: first_week/01_13/manifest.py
# data_csv 위치:     first_week/data_csv

BASE_DIR = Path(__file__).resolve().parents[1]  # 👉 first_week
DATA_DIR = BASE_DIR / "data_csv"

DATA_MANIFEST = {
    "battery_main": {
        "domain": "battery",
        "path": DATA_DIR / "Lithium-Ion Battery Cycle Life.csv",
        "description": "Battery main experiment (full cycle)"
    },
    "battery_short": {
        "domain": "battery",
        "path": DATA_DIR / "100_Cycle_Lithium-Ion Battery Cycle Life.csv",
        "description": "Battery short cycle comparison"
    },
    "ehr_main": {
        "domain": "ehr",
        "path": DATA_DIR / "ehr_disease_progression.csv",
        "description": "EHR main experiment"
    }
}