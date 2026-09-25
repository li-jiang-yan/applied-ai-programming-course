"""Offline lexical baseline; no third-party dependencies or model downloads."""
from pathlib import Path
import re

DATA = Path(__file__).resolve().parents[1] / "data"

def retrieve(question, k=2):
    query = set(re.findall(r"\w+", question.lower()))
    scored = []
    for path in sorted(DATA.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        words = set(re.findall(r"\w+", text.lower()))
        score = len(query & words) / max(len(query), 1)
        scored.append((score, path.name, text))
    return sorted(scored, key=lambda row: (-row[0], row[1]))[:k]

if __name__ == "__main__":
    for score, name, text in retrieve("refund request"):
        print(name, round(score, 3), text)
