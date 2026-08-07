from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

EIA_API_KEY = os.getenv("EIA_API_KEY", "")
NOAA_TOKEN = os.getenv("NOAA_TOKEN", "")
NOAA_STATION = os.getenv("NOAA_STATION", "")
