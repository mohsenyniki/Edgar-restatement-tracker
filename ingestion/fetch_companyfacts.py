import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

parser = argparse.ArgumentParser(description="Fetch company facts from SEC EDGAR")
parser.add_argument("cik", help="CIK of the company to fetch facts for")
args = parser.parse_args()

if not args.cik.isdigit():
    print("The input " + args.cik + " is not a valid CIK. CIK must be a number.", file=sys.stderr)
    sys.exit(1)
if len(args.cik) > 10:
    print("The input " + args.cik + " is too long. CIK must be at most 10 digits long.", file=sys.stderr)
    sys.exit(1)

# pad it to 10 digits starting with 0s
args.cik = args.cik.zfill(10)

# load and read the .env file
load_dotenv()
user_agent = os.getenv("SEC_USER_AGENT")
if not user_agent:
    print("SEC_USER_AGENT is not set in the .env file. Please set it to your name and email.", file=sys.stderr)
    sys.exit(1)
    
# http request to fetch company facts from SEC EDGAR
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{args.cik}.json"
headers = {"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"}

# network failures (no internet, timeout) raise an exception instead of returning a status code
try:
    response = requests.get(url, headers=headers, timeout=30)
except requests.exceptions.RequestException as e:
    print(f"Network error while contacting SEC: {e}. Try again.", file=sys.stderr)
    sys.exit(1)

# SEC answered, but maybe not with the data
if response.status_code == 403:
    print("SEC refused the request (403). Check SEC_USER_AGENT in .env.", file=sys.stderr)
    sys.exit(1)
if response.status_code == 404:
    print(f"No company facts for CIK {args.cik} (404).", file=sys.stderr)
    sys.exit(1)
if response.status_code != 200:
    print(f"Unexpected response from SEC: {response.status_code}.", file=sys.stderr)
    sys.exit(1)

# save under <repo root>/data/raw/companyfacts/, no matter which folder the script is run from
repo_root = Path(__file__).resolve().parent.parent
out_dir = repo_root / "data" / "raw" / "companyfacts"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / f"CIK{args.cik}.json"

with open(out_path, "w") as f:
    json.dump(response.json(), f)

size_mb = out_path.stat().st_size / 1_000_000
print(f"Saved {out_path.relative_to(repo_root)} ({size_mb:.1f} MB)")