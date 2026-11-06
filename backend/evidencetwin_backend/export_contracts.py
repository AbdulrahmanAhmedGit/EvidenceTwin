"""Export schema definitions only, never research data or runtime configuration."""
import argparse
import json
from pathlib import Path
from pydantic import TypeAdapter
from .contracts.registry import SCHEMAS

def export_contracts(output: Path) -> int:
    output.mkdir(parents=True, exist_ok=True)
    for name, schema in SCHEMAS.items():
        target = output / f"{name}.schema.json"
        target.write_text(json.dumps(TypeAdapter(schema).json_schema(), indent=2) + "\n", encoding="utf-8")
    return len(SCHEMAS)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(f"Exported {export_contracts(args.output)} contract definitions.")

if __name__ == "__main__":
    main()
