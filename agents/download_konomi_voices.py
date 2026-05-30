"""
鬥ｬ蝣ｴ縺薙・縺ｿwiki 縺九ｉ .m4a 繝懊う繧ｹ繝輔ぃ繧､繝ｫ繧剃ｸ諡ｬ繝繧ｦ繝ｳ繝ｭ繝ｼ繝峨☆繧九・
菫晏ｭ伜・:
  downloads/konomi_voices/base/          (繧｢繧､繝峨Ν隧ｳ邏ｰ 80莉ｶ)
  downloads/konomi_voices/theater_days/  (繧ｷ繧｢繧ｿ繝ｼ繝・う繧ｺ 50莉ｶ)
"""

import re
import time
import urllib.parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

TARGETS = [
    {
        "url": "https://seesaawiki.jp/konomi-wiki/d/%A5%A2%A5%A4%A5%C9%A5%EB%BE%DC%BA%D9",
        "subdir": "base",
    },
    {
        "url": "https://seesaawiki.jp/konomi-wiki/d/%a5%a2%a5%a4%a5%c9%a5%eb%be%dc%ba%d9%a1%ca%a5%b7%a5%a2%a5%bf%a1%bc%a5%c7%a5%a4%a5%ba%a1%cb",
        "subdir": "theater_days",
    },
]

BASE_DIR = Path(r"E:\irodori\downloads\konomi_voices")
SLEEP_SEC = 0.5
MAX_RETRIES = 2
FILENAME_MAX_LEN = 50

FORBIDDEN = re.compile(r'[\\/:*?"<>|]')


def sanitize(text: str, maxlen: int = FILENAME_MAX_LEN) -> str:
    text = text.strip()
    text = FORBIDDEN.sub("_", text)
    return text[:maxlen]


def collect_links(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    user_area = soup.find(class_="user-area")
    if not user_area:
        return []
    links = []
    for a in user_area.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".m4a"):
            text = a.get_text(strip=True)
            links.append({"url": href, "text": text})
    return links


def make_filename(idx: int, entry: dict) -> str:
    text = entry["text"]
    if text:
        name = f"{idx:03d}_{sanitize(text)}"
    else:
        # URL譛ｫ蟆ｾ縺ｮ繝輔ぃ繧､繝ｫ蜷埼Κ蛻・ｒ縺昴・縺ｾ縺ｾ菴ｿ縺・        name = urllib.parse.unquote(entry["url"].split("/")[-1])
        name = name.rsplit(".", 1)[0]  # 諡｡蠑ｵ蟄宣勁蜴ｻ
        name = sanitize(name)
    return name + ".m4a"


def download(session: requests.Session, url: str, dest: Path) -> bool:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=30)
            resp.raise_for_status()
            dest.write_bytes(resp.content)
            return True
        except Exception as e:
            print(f"  [attempt {attempt}] {e}")
            if attempt < MAX_RETRIES:
                time.sleep(1)
    return False


def process(target: dict, session: requests.Session) -> None:
    url = target["url"]
    subdir = BASE_DIR / target["subdir"]
    subdir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {target['subdir']} ===")
    print(f"  蜿門ｾ・ {url}")

    resp = session.get(url, timeout=30)
    resp.raise_for_status()

    links = collect_links(resp.text)
    print(f"  繝ｪ繝ｳ繧ｯ謨ｰ: {len(links)}")

    ok = fail = 0
    for idx, entry in enumerate(links, start=1):
        fname = make_filename(idx, entry)
        dest = subdir / fname

        if dest.exists() and dest.stat().st_size > 0:
            print(f"  [{idx:03d}] 繧ｹ繧ｭ繝・・(譌｢蟄・: {fname}")
            ok += 1
            continue

        success = download(session, entry["url"], dest)
        if success:
            size_kb = dest.stat().st_size / 1024
            print(f"  [{idx:03d}] OK ({size_kb:.1f}KB): {fname}")
            ok += 1
        else:
            print(f"  [{idx:03d}] FAIL: {entry['url']}")
            fail += 1

        time.sleep(SLEEP_SEC)

    print(f"  螳御ｺ・ {ok}莉ｶ謌仙粥 / {fail}莉ｶ螟ｱ謨・)


def main() -> None:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://seesaawiki.jp/",
        }
    )

    BASE_DIR.mkdir(parents=True, exist_ok=True)

    for target in TARGETS:
        process(target, session)

    print("\n蜈ｨ繝壹・繧ｸ蜃ｦ逅・ｮ御ｺ・)


if __name__ == "__main__":
    main()
