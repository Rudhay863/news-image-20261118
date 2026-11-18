"""News-image entry: copy the committed entry.png to /output/entry.png.

Deterministic and offline (standard library only). The copy is verified
byte-for-byte with SHA-256 so a truncated write can never pass silently.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output,
as in the kit starter.
"""
import hashlib
import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


OUT.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, OUT)
assert sha256(SRC) == sha256(OUT), "copy verification failed"
print(f"copied {SRC} -> {OUT} (sha256 {sha256(OUT)})")
