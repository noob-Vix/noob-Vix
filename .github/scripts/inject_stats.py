#!/usr/bin/env python3
"""Inject a yearly contributions row into the github-readme-stats SVG card.

The github-readme-stats "Contributed to" row is hardcoded to "last year",
so we compute the real current-year contribution count from the GitHub API
and inject a matching 5th stat row into the generated SVG.

Usage: python3 inject_stats.py <COUNT> <YEAR> <SVG_PATH>
"""
import re
import sys


def main() -> None:
    count, year, path = sys.argv[1], sys.argv[2], sys.argv[3]
    svg = open(path).read()

    # Bump card dimensions to fit the 5th row (170 -> 195)
    svg = re.sub(r'height="\d+"', 'height="195"', svg, count=1)
    svg = re.sub(r'viewBox="0 0 467 \d+"', 'viewBox="0 0 467 195"', svg, count=1)

    # The folder/book icon, matching github-readme-stats dark theme styles
    row = f"""</g><g transform="translate(0, 100)">
    <g class="stagger" style="animation-delay: 1050ms" transform="translate(25, 0)">
      
    <svg data-testid="icon" class="icon" viewBox="0 0 16 16" version="1.1" width="16" height="16">
      <path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
    </svg>
  
      <text class="stat  bold" x="25" y="12.5">Contributions ({year}):</text>
      <text
        class="stat  bold"
        x="224.01"
        y="12.5"
        data-testid="contribs"
      >{count}</text>
    </g>
  </g>"""

    # Append the new row immediately after the last stat row (the Issues row)
    pattern = re.compile(r'(data-testid="issues"[^>]*>\s*[^<]*</text>\s*</g>)')
    svg, n = pattern.subn(lambda m: m.group(1) + row, svg, count=1)
    if n == 0:
        raise SystemExit("ERROR: could not find issues row to inject after")

    open(path, "w").write(svg)
    print(f"Injected {count} contributions for {year}")


if __name__ == "__main__":
    main()