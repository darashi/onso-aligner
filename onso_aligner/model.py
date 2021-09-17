import os
import sys
from pathlib import Path
from urllib.request import urlretrieve

DEFAULT_CACHE_DIR = os.path.join(
    os.path.expanduser("~"), ".cache", "onso_aligner"
)
CACHE_DIR = os.environ.get("ONSO_ALIGNER_CACHE_DIR", DEFAULT_CACHE_DIR)
MODEL_URL = "https://github.com/julius-speech/segmentation-kit/raw/master/models/hmmdefs_monof_mix16_gid.binhmm"  # noqa: B950
MODEL_NAME = "hmmdefs_monof_mix16_gid.binhmm"


def retrieve(
    url: str = MODEL_URL, model_name: str = MODEL_NAME, force: bool = False
) -> Path:
    out_dir = Path(CACHE_DIR) / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    dest_path = out_dir / model_name

    if force or not os.path.exists(dest_path):
        print(f"Downloading: {url} to {dest_path}", file=sys.stderr)
        urlretrieve(url, dest_path)

    return dest_path
