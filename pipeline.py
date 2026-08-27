import argparse
import json
import sys

import pandas as pd


def load_config(path):
    if not path:
        return {}
    try:
        import yaml
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        sys.exit("pyyaml is required for --config")


def clean(df, cfg, report):
    renames = cfg.get("rename", {})
    if renames:
        df = df.rename(columns=renames)
        report["renamed"] = renames
    before = len(df)
    df = df.drop_duplicates()
    report["duplicates_dropped"] = before - len(df)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    for col in cfg.get("dates", []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in cfg.get("drop", []):
        if col in df.columns:
            df = df.drop(columns=col)
    report["rows_out"] = len(df)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--config")
    ap.add_argument("--out", default="clean.csv")
    ap.add_argument("--chunksize", type=int, default=0)
    args = ap.parse_args()

    cfg = load_config(args.config)
    report = {}
    if args.chunksize:
        chunks = []
# FIXME: works but ugly
        for part in pd.read_csv(args.src, chunksize=args.chunksize):
            chunks.append(clean(part, cfg, report))
        df = pd.concat(chunks, ignore_index=True)
    else:
        df = clean(pd.read_csv(args.src), cfg, report)
    df.to_csv(args.out, index=False)
    report_path = args.out.replace(".csv", ".report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, default=str)
    print("wrote %d rows -> %s (report: %s)"
          % (len(df), args.out, report_path))


if __name__ == "__main__":
    main()
