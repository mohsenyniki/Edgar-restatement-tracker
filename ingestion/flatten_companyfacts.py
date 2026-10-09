import argparse
import json
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw" / "companyfacts"


def flatten(data):
    """Turn one companyfacts JSON into a table with one row per reported value.

    The JSON is nested: facts -> taxonomy -> concept -> units -> unit -> [values].
    Each value dict (val, start, end, accn, form, filed, ...) becomes a row, and the
    keys we walked through on the way down become columns.
    """
    rows = []
    for taxonomy, concepts in data["facts"].items():
        for concept, details in concepts.items():
            for unit, values in details["units"].items():
                for value in values:
                    rows.append({
                        "cik": data["cik"],
                        "entity_name": data["entityName"],
                        "taxonomy": taxonomy,
                        "concept": concept,
                        "unit": unit,
                        **value,
                    })

    df = pd.DataFrame(rows)
    # instant facts (e.g. Assets on a balance sheet date) have no start date
    for col in ["start", "end", "filed"]:
        df[col] = pd.to_datetime(df[col])
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten a saved companyfacts JSON into a table")
    parser.add_argument("cik", help="CIK of a company already fetched with fetch_companyfacts.py")
    args = parser.parse_args()

    path = RAW_DIR / f"CIK{args.cik.zfill(10)}.json"
    if not path.exists():
        print(f"{path.relative_to(REPO_ROOT)} not found. Run fetch_companyfacts.py first.", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        df = flatten(json.load(f))

    print(df.shape)
    print(df.dtypes)
    print(df.head())
