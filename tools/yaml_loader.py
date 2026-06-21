from pathlib import Path
import yaml


def load_yaml_directory(directory: str) -> list[dict]:
    records = []

    path = Path(directory)

    for file in path.rglob("*.yml"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data:
                records.append(data)

        except Exception as e:
            print(f"ERROR: {file}: {e}")

    for file in path.rglob("*.yaml"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data:
                records.append(data)

        except Exception as e:
            print(f"ERROR: {file}: {e}")

    return records