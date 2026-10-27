#!/usr/bin/env python3
"""Downloads a Google Fonts family into a project for a deck theme.

Writes the Latin and Cyrillic woff2 files to <project>/fonts and prints the
@font-face rules to paste into deck-theme.css. The deck then works offline."""

from __future__ import annotations

import argparse
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://fonts.googleapis.com/css2"
# Google serves woff2 with unicode ranges only to a modern browser.
AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SUBSETS = ("latin", "cyrillic")
FACE = re.compile(r"/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}", re.S)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("family", help='Google Fonts family, for example "Playfair Display"')
    parser.add_argument("project", type=Path, help="Deck project folder")
    parser.add_argument("--weights", default="400..700", help="a range like 400..700 or a list like 400;700")
    args = parser.parse_args()

    query = urllib.parse.urlencode({"family": f"{args.family}:wght@{args.weights}", "display": "swap"})
    try:
        css = fetch(f"{API}?{query}").decode("utf-8")
    except urllib.error.HTTPError as error:
        if error.code != 400:
            raise
        # A static family has no weight range; Google answers 400 to 400..700.
        raise SystemExit(f"Google Fonts refused {args.family} {args.weights}: "
                         "check the name, and list weights like 400;600 for a family that is not variable")
    slug = re.sub(r"[^a-z0-9]+", "-", args.family.lower()).strip("-")
    files: dict[str, bytes] = {}
    rules = []
    for subset, body in FACE.findall(css):
        if subset not in SUBSETS:
            continue
        url = re.search(r"url\((https://[^)]+\.woff2)\)", body).group(1)
        style = re.search(r"font-style:\s*(\w+)", body).group(1)
        # A static family serves one file per weight, so the weight is in the name.
        weight = re.search(r"font-weight:\s*([\d ]+);", body).group(1).replace(" ", "-")
        name = f"{slug}-{style}-{weight}-{subset}.woff2"
        files[name] = fetch(url)
        body = re.sub(r"url\([^)]+\)", f'url("fonts/{name}")', body)
        rules.append("@font-face {" + body.rstrip() + "\n}")
    if not rules:
        raise SystemExit(f"no Latin or Cyrillic files for {args.family}; check the family name")
    # Write only after every download succeeded, so a failed run leaves no partial set.
    fonts = args.project / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (fonts / name).write_bytes(data)
    print("\n".join(rules))


if __name__ == "__main__":
    main()
