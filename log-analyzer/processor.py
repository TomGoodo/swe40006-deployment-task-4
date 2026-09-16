import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("log_analyzer")

INPUT_DIR = Path("/data/input")
OUTPUT_DIR = Path("/data/output")


def analyze_file(path: Path):
    text = path.read_text(errors="ignore")
    lines = text.splitlines()
    words = text.split()
    return {
        "file": path.name,
        "lines": len(lines),
        "words": len(words),
        "bytes": path.stat().st_size,
    }


def main():
    log.info("logging system starting up")
    log.info("reading input from %s", INPUT_DIR)
    log.info("writing output to %s", OUTPUT_DIR)

    if not INPUT_DIR.is_dir():
        log.error("input directory %s does not exist", INPUT_DIR)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in INPUT_DIR.iterdir() if p.is_file())
    if not files:
        log.warning("no files found in %s — nothing to process", INPUT_DIR)

    results = []
    for path in files:
        log.info("processing %s", path.name)
        results.append(analyze_file(path))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files_processed": len(results),
        "total_lines": sum(r["lines"] for r in results),
        "total_words": sum(r["words"] for r in results),
        "files": results,
    }

    out_path = OUTPUT_DIR / "report.json"
    out_path.write_text(json.dumps(report, indent=2))
    log.info("wrote report to %s", out_path)

    log.info("log analyzer finished:processed %d file(s)", len(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
