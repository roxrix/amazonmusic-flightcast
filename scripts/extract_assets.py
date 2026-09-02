#!/usr/bin/env python3
"""Extract embedded image/font data URIs from the original self-contained deck."""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
ASSETS = ROOT / "assets"
IMAGES = ASSETS / "images"
FONTS = ASSETS / "fonts"


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")
    IMAGES.mkdir(parents=True, exist_ok=True)
    FONTS.mkdir(parents=True, exist_ok=True)

    image_matches = list(re.finditer(r'<img\s+src="data:image/(jpeg|png|webp);base64,([^"]+)"', html))
    image_manifest = []
    for index, match in enumerate(image_matches, 1):
        image_type, payload = match.groups()
        extension = "jpg" if image_type == "jpeg" else image_type
        filename = f"image-{index:02d}.{extension}"
        (IMAGES / filename).write_bytes(base64.b64decode(payload))
        image_manifest.append({"index": index, "file": f"assets/images/{filename}", "bytes": (IMAGES / filename).stat().st_size})

    font_matches = list(re.finditer(r'@font-face\{font-family:"Geist";font-style:normal;font-weight:(\d+);src:url\(data:font/woff2;base64,([^\)]+)\)', html))
    font_manifest = []
    for match in font_matches:
        weight, payload = match.groups()
        filename = f"geist-{weight}.woff2"
        (FONTS / filename).write_bytes(base64.b64decode(payload))
        font_manifest.append({"weight": int(weight), "file": f"assets/fonts/{filename}", "bytes": (FONTS / filename).stat().st_size})

    manifest = {"images": image_manifest, "fonts": font_manifest}
    (ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"images": len(image_manifest), "fonts": len(font_manifest), "asset_bytes": sum(x["bytes"] for x in image_manifest + font_manifest)}, indent=2))


if __name__ == "__main__":
    main()
