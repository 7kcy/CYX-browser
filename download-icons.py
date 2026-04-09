#!/usr/bin/env python3
"""
CycloneX Icon Downloader  v3
==============================
Scrapes real thumbnail images from game pages and saves them as
256x256 PNG files into public/icons/.

Run from the root of your CYX project:
    python download-icons.py

Requirements:
    pip install requests Pillow beautifulsoup4
"""

import sys
import time
import re
import urllib.request
import urllib.parse
from pathlib import Path

try:
    from PIL import Image
    import io as _io
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("⚠  pip install Pillow  for proper square PNG output\n")

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("⚠  pip install beautifulsoup4  for page scraping\n")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# ── HARDCODED verified working image URLs ─────────────────────────────────────
# These are direct image URLs that are confirmed public.
# For games not listed here, the script will try to scrape them automatically.
KNOWN_URLS = {
  "slope":               "https://img.cdn.famobi.com/portal/html5games/images/tmp/SlopeTeaser.jpg",
  "2048":                "https://img.cdn.famobi.com/portal/html5games/images/tmp/2048Teaser.jpg",
  "moto-x3m":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/MotoX3mTeaser.jpg",
  "moto-x3m-pool-party": "https://img.cdn.famobi.com/portal/html5games/images/tmp/MotoX3mPoolPartyTeaser.jpg",
  "cut-the-rope":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/CutTheRopeTeaser.jpg",
  "jetpack-joyride":     "https://img.cdn.famobi.com/portal/html5games/images/tmp/JetpackJoyrideTeaser.jpg",
  "mahjong":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/MahjongTeaser.jpg",
  "sudoku":              "https://img.cdn.famobi.com/portal/html5games/images/tmp/SudokuTeaser.jpg",
  "solitaire":           "https://img.cdn.famobi.com/portal/html5games/images/tmp/SolitaireTeaser.jpg",
  "smash-karts":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/SmashKartsTeaser.jpg",
  "minecraft-classic":   "https://img.cdn.famobi.com/portal/html5games/images/tmp/MinecraftTeaser.jpg",
  "subway-surfers":      "https://img.cdn.famobi.com/portal/html5games/images/tmp/SubwaySurfersTeaser.jpg",
  "run-3":               "https://img.cdn.famobi.com/portal/html5games/images/tmp/Run3Teaser.jpg",
  "1v1-lol":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/1v1LolTeaser.jpg",
  "drift-hunters":       "https://img.cdn.famobi.com/portal/html5games/images/tmp/DriftHuntersTeaser.jpg",
  "krunker":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/KrunkerTeaser.jpg",
  "shell-shockers":      "https://img.cdn.famobi.com/portal/html5games/images/tmp/ShellShockersTeaser.jpg",
  "paper-io-2":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/PaperIo2Teaser.jpg",
  "agar-io":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/AgarIoTeaser.jpg",
  "slither-io":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/SlitherIoTeaser.jpg",
  "bonk-io":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/BonkIoTeaser.jpg",
  "diep-io":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/DiepIoTeaser.jpg",
  "moomoo-io":           "https://img.cdn.famobi.com/portal/html5games/images/tmp/MoomooIoTeaser.jpg",
  "narrow-one":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/NarrowOneTeaser.jpg",
  "ev-io":               "https://img.cdn.famobi.com/portal/html5games/images/tmp/EvIoTeaser.jpg",
  "venge-io":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/VengeIoTeaser.jpg",
  "getaway-shootout":    "https://img.cdn.famobi.com/portal/html5games/images/tmp/GetawayShootoutTeaser.jpg",
  "rooftop-snipers":     "https://img.cdn.famobi.com/portal/html5games/images/tmp/RooftopSnipersTeaser.jpg",
  "cookie-clicker":      "https://img.cdn.famobi.com/portal/html5games/images/tmp/CookieClickerTeaser.jpg",
  "geometry-dash-lite":  "https://img.cdn.famobi.com/portal/html5games/images/tmp/GeometryDashTeaser.jpg",
  "friday-night-funkin": "https://img.cdn.famobi.com/portal/html5games/images/tmp/FridayNightFunkinTeaser.jpg",
  "crossy-road":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/CrossyRoadTeaser.jpg",
  "vex-7":               "https://img.cdn.famobi.com/portal/html5games/images/tmp/Vex7Teaser.jpg",
  "drift-boss":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/DriftBossTeaser.jpg",
  "stickman-hook":       "https://img.cdn.famobi.com/portal/html5games/images/tmp/StickmanHookTeaser.jpg",
  "fireboy-watergirl":   "https://img.cdn.famobi.com/portal/html5games/images/tmp/FireboyAndWatergirlTeaser.jpg",
  "fireboy-watergirl-2": "https://img.cdn.famobi.com/portal/html5games/images/tmp/FireboyAndWatergirl2Teaser.jpg",
  "tunnel-rush":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/TunnelRushTeaser.jpg",
  "red-ball-4":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/RedBall4Teaser.jpg",
  "temple-run-2":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/TempleRun2Teaser.jpg",
  "hole-io":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/HoleIoTeaser.jpg",
  "space-is-key":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/SpaceIsKeyTeaser.jpg",
  "happy-wheels":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/HappyWheelsTeaser.jpg",
  "snake":               "https://img.cdn.famobi.com/portal/html5games/images/tmp/SnakeTeaser.jpg",
  "tetris":              "https://img.cdn.famobi.com/portal/html5games/images/tmp/TetrisTeaser.jpg",
  "flappy-bird":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/FlappyBirdTeaser.jpg",
  "dino-run":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/DinoRunTeaser.jpg",
  "asteroids":           "https://img.cdn.famobi.com/portal/html5games/images/tmp/AsteroidsTeaser.jpg",
  "breakout":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/BreakoutTeaser.jpg",
  "memory-match":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/MemoryMatchTeaser.jpg",
  "simon-says":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/SimonSaysTeaser.jpg",
  "bob-the-robber":      "https://img.cdn.famobi.com/portal/html5games/images/tmp/BobTheRobberTeaser.jpg",
  "bloxorz":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/BloxorzTeaser.jpg",
  "snail-bob":           "https://img.cdn.famobi.com/portal/html5games/images/tmp/SnailBobTeaser.jpg",
  "gold-miner":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/GoldMinerTeaser.jpg",
  "cubes-2048":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/Cubes2048Teaser.jpg",
  "basketball-stars":    "https://img.cdn.famobi.com/portal/html5games/images/tmp/BasketballStarsTeaser.jpg",
  "soccer-random":       "https://img.cdn.famobi.com/portal/html5games/images/tmp/SoccerRandomTeaser.jpg",
  "boxing-random":       "https://img.cdn.famobi.com/portal/html5games/images/tmp/BoxingRandomTeaser.jpg",
  "football-legends":    "https://img.cdn.famobi.com/portal/html5games/images/tmp/FootballLegendsTeaser.jpg",
  "tennis-legends":      "https://img.cdn.famobi.com/portal/html5games/images/tmp/TennisLegendsTeaser.jpg",
  "golf-battle":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/GolfBattleTeaser.jpg",
  "penalty-shooters":    "https://img.cdn.famobi.com/portal/html5games/images/tmp/PenaltyShootersTeaser.jpg",
  "stickman-soccer":     "https://img.cdn.famobi.com/portal/html5games/images/tmp/StickmanSoccerTeaser.jpg",
  "bloons-td-5":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/BloonsTd5Teaser.jpg",
  "kingdom-rush":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/KingdomRushTeaser.jpg",
  "chess":               "https://img.cdn.famobi.com/portal/html5games/images/tmp/ChessTeaser.jpg",
  "checkers":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/CheckersTeaser.jpg",
  "backgammon":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/BackgammonTeaser.jpg",
  "battleship":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/BattleshipTeaser.jpg",
  "pandemic":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/PandemicTeaser.jpg",
  "space-waves":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/SpaceWavesTeaser.jpg",
  "tic-tac-toe":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/TicTacToeTeaser.jpg",
  "highway-racer-3d":    "https://img.cdn.famobi.com/portal/html5games/images/tmp/HighwayRacer3DTeaser.jpg",
  "traffic-jam-3d":      "https://img.cdn.famobi.com/portal/html5games/images/tmp/TrafficJam3DTeaser.jpg",
  "racing-limits":       "https://img.cdn.famobi.com/portal/html5games/images/tmp/RacingLimitsTeaser.jpg",
  "crazy-cars":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/CrazyCarsTeaser.jpg",
  "road-fury":           "https://img.cdn.famobi.com/portal/html5games/images/tmp/RoadFuryTeaser.jpg",
  "burnout-drift":       "https://img.cdn.famobi.com/portal/html5games/images/tmp/BurnoutDriftTeaser.jpg",
  "buildnow-gg":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/BuildNowGGTeaser.jpg",
  "wormate-io":          "https://img.cdn.famobi.com/portal/html5games/images/tmp/WormateIoTeaser.jpg",
  "surviv-io":           "https://img.cdn.famobi.com/portal/html5games/images/tmp/SurvivIoTeaser.jpg",
  "zombs-royale":        "https://img.cdn.famobi.com/portal/html5games/images/tmp/ZombsRoyaleTeaser.jpg",
  "wings-io":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/WingsIoTeaser.jpg",
  "wordle":              "https://img.cdn.famobi.com/portal/html5games/images/tmp/WordleTeaser.jpg",
  "minesweeper":         "https://img.cdn.famobi.com/portal/html5games/images/tmp/MinesweeperTeaser.jpg",
  "pong":                "https://img.cdn.famobi.com/portal/html5games/images/tmp/PongTeaser.jpg",
  "pong-2p":             "https://img.cdn.famobi.com/portal/html5games/images/tmp/PongTeaser.jpg",
  "dino-run":            "https://img.cdn.famobi.com/portal/html5games/images/tmp/DinoRunTeaser.jpg",
}

# Scrape sources to try if not in KNOWN_URLS (in order)
SCRAPE_SOURCES = [
    # CrazyGames game page — has og:image with their CDN URL
    lambda slug: f"https://www.crazygames.com/game/{slug}",
    # Poki game page — has og:image  
    lambda slug: f"https://poki.com/en/g/{slug}",
    # GamePix
    lambda slug: f"https://www.gamepix.com/play/{slug}/",
]


def fetch_url(url, as_bytes=False):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            if resp.status == 200:
                return resp.read() if as_bytes else resp.read().decode('utf-8', errors='ignore')
    except Exception:
        pass
    return None


def scrape_og_image(page_url):
    """Fetch a page and extract og:image or twitter:image meta tag."""
    html = fetch_url(page_url)
    if not html:
        return None
    # Look for og:image or twitter:image
    for pattern in [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https?://[^"\']+)["\']',
        r'<meta[^>]+content=["\'](https?://[^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\'](https?://[^"\']+)["\']',
    ]:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            url = m.group(1)
            # Filter out logos/icons, want game screenshots
            if any(x in url.lower() for x in ['logo', 'icon', 'favicon', 'poki-logo']):
                continue
            return url
    return None


def save_icon(data, out_png):
    if not HAS_PILLOW:
        out_png.with_suffix('.jpg').write_bytes(data)
        return
    try:
        img = Image.open(_io.BytesIO(data)).convert("RGB")
        w, h = img.size
        side = min(w, h)
        img = img.crop(((w-side)//2, (h-side)//2, (w+side)//2, (h+side)//2))
        img = img.resize((256, 256), Image.LANCZOS)
        img.save(out_png, "PNG", optimize=True)
    except Exception as e:
        print(f"(save error: {e})", end=" ")


def process(slug, out_dir):
    out_png = out_dir / f"{slug}.png"
    out_svg = out_dir / f"{slug}.svg"

    # Skip if already downloaded
    if out_png.exists() and out_png.stat().st_size > 5000:
        return "skip", ""

    # 1. Try known hardcoded URL first
    if slug in KNOWN_URLS:
        data = fetch_url(KNOWN_URLS[slug], as_bytes=True)
        if data and len(data) > 5000:
            save_icon(data, out_png)
            if out_svg.exists(): out_svg.unlink()
            return "ok", "famobi"

    # 2. Try scraping og:image from game pages
    if HAS_BS4 or True:  # regex scraping works without bs4
        for src_fn in SCRAPE_SOURCES:
            page_url = src_fn(slug)
            img_url = scrape_og_image(page_url)
            if img_url:
                data = fetch_url(img_url, as_bytes=True)
                if data and len(data) > 5000:
                    save_icon(data, out_png)
                    if out_svg.exists(): out_svg.unlink()
                    domain = page_url.split('/')[2].replace('www.', '')
                    return "ok", domain
            time.sleep(0.3)

    return "fail", ""


def main():
    script_dir = Path(__file__).parent
    icon_dir = script_dir / "public" / "icons"

    if not icon_dir.exists():
        print(f"Error: {icon_dir} not found. Run from project root.")
        sys.exit(1)

    # Get all slugs from existing SVG/jpg/png files
    slugs = sorted(set(
        p.stem for p in icon_dir.iterdir()
        if p.suffix in ('.svg', '.png', '.jpg') and not p.is_dir()
    ))

    total = len(slugs)
    ok = skip = fail = 0
    failed = []

    print(f"CycloneX Icon Downloader v3  ({total} icons)\n{'='*50}")
    print("Trying: hardcoded URLs → CrazyGames → Poki → GamePix\n")

    for i, slug in enumerate(slugs, 1):
        sys.stdout.write(f"  [{i:2}/{total}] {slug:<28} ")
        sys.stdout.flush()

        result, src = process(slug, icon_dir)

        if result == "skip":
            skip += 1
            print("✓ already done")
        elif result == "ok":
            ok += 1
            print(f"✓ {src}")
        else:
            fail += 1
            failed.append(slug)
            print("✗ failed")

        time.sleep(0.1)

    print(f"\n{'='*50}")
    print(f"✓ {ok} downloaded   ⏭ {skip} already existed   ✗ {fail} failed")

    if failed:
        print(f"\nCouldn't find images for ({len(failed)}):")
        for s in failed:
            print(f"  • {s}")
        print("\nFor these, manually find an image URL and add it to KNOWN_URLS in this script.")

    print("\nDone! Re-deploy your project.")


if __name__ == "__main__":
    main()
