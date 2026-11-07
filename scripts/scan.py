#!/usr/bin/env python3
"""CLI-сканер: прогоняет текст через детерминированные метрики humanizer-ru.

Использование (из корня репо; у установленного скилла путь: <папка скилла>/scripts/scan.py):
    python skills/humanizer-ru/scripts/scan.py path/to/text.txt
    echo "ваш текст" | python skills/humanizer-ru/scripts/scan.py -
    python skills/humanizer-ru/scripts/scan.py text.txt --json --genre academic
"""

import argparse
import json
import sys
from pathlib import Path

# Добавляем путь к humanizer_metrics
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from humanizer_metrics.score import score_text
from humanizer_metrics.markdown import strip_markdown

def main():
    parser = argparse.ArgumentParser(description="Сканер чистоты текста humanizer-ru")
    parser.add_argument("input", help="Файл или - для stdin")
    parser.add_argument("--json", action="store_true", help="Вывод в JSON")
    parser.add_argument("--genre", default="general", choices=["general", "academic", "legal", "fiction", "news"])
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.input).read_text(encoding="utf-8")

    text = strip_markdown(text)
    result = score_text(text, genre=args.genre)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ЧИСТОТА: {result.get('score', 0)}/100")
        if args.verbose:
            for k, v in result.items():
                if k != "score":
                    print(f"  {k}: {v}")

    # Exit 1 if score below threshold for signals
    sys.exit(0 if result.get("score", 100) >= 70 else 1)

if __name__ == "__main__":
    main()
