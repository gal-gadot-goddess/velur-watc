"""Metadata: title, description, hashtags from the design file name.

Slug format: <collection>-<code>.html, e.g. orbis-or10.html ->
collection ORBIS, calibre OR-10. Output is identical on every platform.
"""
import re

import config

HASHTAGS = ["#luxurywatch", "#watches", "#watchcollector", "#velaure", "#reels"]


def parse_slug(filename):
    stem = filename.lower().rsplit(".html", 1)[0]
    m = re.match(r"^([a-z]+)-([a-z0-9]+)$", stem)
    if not m:
        return stem.upper(), stem.upper()
    return m.group(1).upper(), m.group(2).upper()


def build(filename, music_name):
    collection, calibre = parse_slug(filename)
    title = f"{config.BRAND} {collection} — Luxury Watch Reel"
    description = (
        f"{config.BRAND} {collection} (Cal. {calibre}).\n"
        f"{config.TAGLINE}\n\n"
        f"Original design rendered live in code.\n"
        f"Music: {music_name}\n\n"
        "New design every day. Follow for the full collection."
    )
    tags = [collection.lower(), "luxury watch", config.BRAND.lower(), "watch design"]
    return {
        "title": title[:100],
        "description": description,
        "tags": tags,
        "hashtags": " ".join(HASHTAGS),
    }
