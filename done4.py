"""Legacy script kept for compatibility.

Use run.py or `python -m dino_ai` going forward.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dino_ai.main import main


if __name__ == "__main__":
    main()
