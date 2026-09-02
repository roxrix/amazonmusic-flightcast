#!/usr/bin/env python3
"""Static checks for the Amazon Music × Flightcast browser deck."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
EXPECTED_SLIDES = 23


class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slide_ids: list[str] = []
        self.image_sources: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)
        classes = set((values.get("class") or "").split())
        if tag == "section" and "slide" in classes:
            self.slide_ids.append(element_id or "")
        if tag == "img" and values.get("src"):
            self.image_sources.append(values["src"] or "")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> None:
    if not INDEX.exists():
        fail("index.html is missing")
    if not (ROOT / "source-original.html").exists():
        fail("source-original.html is missing")
    if (ROOT / "source-original.html").stat().st_size < 1_000_000:
        fail("source-original.html does not look like the preserved self-contained source")

    html = INDEX.read_text(encoding="utf-8")
    parser = DeckParser()
    parser.feed(html)

    if len(parser.slide_ids) != EXPECTED_SLIDES:
        fail(f"expected {EXPECTED_SLIDES} slides, found {len(parser.slide_ids)}")
    expected_ids = [f"slide-{number}" for number in range(1, EXPECTED_SLIDES + 1)]
    if parser.slide_ids != expected_ids:
        fail(f"slide IDs are not sequential: {parser.slide_ids}")

    phrases = [
        "Amazon Music wants to highlight your show.",
        "Video podcasts are coming to Amazon Music.",
        "Flightcast sends your existing episodes there automatically.",
        "Amazon Music wants to highlight your show",
        "Four promotion options from Amazon Music",
        "Your show on a Times Square billboard",
        "About 3 weeks from submission to launch",
        "A tagline of 40 characters or less",
        "750,000 plays",
        "at least 250,000 followers",
        "reaches 100,000 impressions",
        "Email at least 100,000 people",
        "3000 × 3000 pixels",
        "until it plays 2 million times",
        "100,000 downloads per episode",
        "Keep the file under 500 MB.",
        "You do not need to film anything new.",
        "Ads from partner accounts",
        "Any TikTok account is eligible.",
        "professional or business Instagram account",
        "9:16, 16:9 or 1×1",
        "Amazon Music adds it.",
        "Everything you send goes live and receives impressions.",
        "Facebook, Threads, Instagram and TikTok.",
        "4 to 6 weeks",
        "Up to 3 to 6 months",
        "1 to 4 files a month",
        "Talya Levine Cooke",
        "VP of Growth and Partnerships",
        "https://airtable.com/appdYhHVLng6NfWgx/pagUkEDRA1gBfqUJt/form",
        "https://cal.com/talyalevine",
    ]
    missing = [phrase for phrase in phrases if phrase not in html]
    if missing:
        fail("required content missing: " + "; ".join(missing))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    confidentiality = [
        "Keep this repository private",
        "marked CONFIDENTIAL on every slide",
        "do not switch on GitHub Pages or any public hosting for it",
    ]
    if any(phrase not in readme for phrase in confidentiality):
        fail("README confidentiality wording is incomplete")
    readme_deck_wording = [
        "23-slide, 16:9 browser presentation",
        "23-page, 16:9 PDF export",
    ]
    if any(phrase not in readme for phrase in readme_deck_wording):
        fail("README browser deck and PDF status wording is incomplete")

    expected_images = [f"assets/images/image-{number:02d}.jpg" for number in range(1, 23)]
    if sorted(set(parser.image_sources)) != expected_images:
        fail("image references do not match image-01.jpg through image-22.jpg")
    missing_assets = [path for path in expected_images if not (ROOT / path).is_file()]
    expected_fonts = [f"assets/fonts/geist-{weight}.woff2" for weight in (400, 500, 600, 700)]
    missing_assets += [path for path in expected_fonts if not (ROOT / path).is_file()]
    if missing_assets:
        fail("missing assets: " + ", ".join(missing_assets))

    hooks = [
        'id="prev-slide"', 'id="next-slide"', 'id="slide-counter"',
        'id="progress-bar"', "ArrowRight", "ArrowLeft", "PageDown", "PageUp",
        "Home", "End", "location.hash", "hashchange", "scroll-snap-type",
        "prefers-reduced-motion", "@media print", "IntersectionObserver",
    ]
    absent_hooks = [hook for hook in hooks if hook not in html]
    if absent_hooks:
        fail("navigation/accessibility hooks missing: " + ", ".join(absent_hooks))

    if "—" in html:
        fail("index.html contains an em dash")
    if not re.search(r"@page\s*\{[^}]*size:\s*16in\s+9in", html):
        fail("print page is not configured to 16:9")

    print(f"PASS: {EXPECTED_SLIDES} sequential slides")
    print(f"PASS: {len(phrases)} required phrases and links")
    print("PASS: preserved source and README confidentiality wording")
    print(f"PASS: {len(expected_images)} referenced images and {len(expected_fonts)} fonts exist")
    print(f"PASS: {len(hooks)} navigation, state, motion, and print hooks")
    print("PASS: no em dashes in index.html")
    print("Verification complete.")


if __name__ == "__main__":
    main()
