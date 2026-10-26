"""Meta publishing: Instagram Reels + Facebook Page video (Graph API).

Needs META_ACCESS_TOKEN plus META_IG_USER_ID (reels) and/or
META_FB_PAGE_ID (page videos). Each channel is independent: a missing
ID skips that channel only. Media must be publicly reachable by URL;
pass --public-base-url in CI (e.g. a release asset or CDN link).
"""
import time

import requests

import config

_API = "https://graph.facebook.com/v21.0"


def can_publish_ig():
    return bool(config.META_ACCESS_TOKEN and config.META_IG_USER_ID)


def can_publish_fb():
    return bool(config.META_ACCESS_TOKEN and config.META_FB_PAGE_ID)


def publish_instagram_reel(public_video_url, caption):
    if not can_publish_ig():
        print("INSTAGRAM: credentials missing, skipped")
        return None
    uid, tok = config.META_IG_USER_ID, config.META_ACCESS_TOKEN
    c = requests.post(
        f"{_API}/{uid}/media",
        data={"media_type": "REELS", "video_url": public_video_url,
              "caption": caption, "access_token": tok},
        timeout=60,
    ).json()
    cid = c.get("id")
    if not cid:
        print(f"INSTAGRAM: container failed: {c}")
        return None
    for _ in range(30):
        st = requests.get(f"{_API}/{cid}",
                          params={"fields": "status_code", "access_token": tok},
                          timeout=30).json()
        if st.get("status_code") == "FINISHED":
            break
        time.sleep(10)
    p = requests.post(f"{_API}/{uid}/media_publish",
                      data={"creation_id": cid, "access_token": tok},
                      timeout=60).json()
    mid = p.get("id")
    print(f"INSTAGRAM: published reel {mid}" if mid else f"INSTAGRAM: publish failed: {p}")
    return mid


def publish_facebook_video(mp4_path, meta):
    if not can_publish_fb():
        print("FACEBOOK: credentials missing, skipped")
        return None
    with open(mp4_path, "rb") as fh:
        r = requests.post(
            f"{_API}/{config.META_FB_PAGE_ID}/videos",
            data={"description": meta["description"] + "\n" + meta["hashtags"],
                  "access_token": config.META_ACCESS_TOKEN},
            files={"source": fh},
            timeout=300,
        ).json()
    vid = r.get("id")
    print(f"FACEBOOK: published video {vid}" if vid else f"FACEBOOK: failed: {r}")
    return vid
