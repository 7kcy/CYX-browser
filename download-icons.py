#!/usr/bin/env python3
"""
CycloneX Icon Downloader  v4
==============================
Downloads real game cover images and saves them as 256x256 PNG files
into public/icons/. Skips games that are already downloaded.

Run from the root of your CYX project:
    python download-icons.py

Requirements:
    python -m pip install Pillow
"""

import sys
import time
import urllib.request
from pathlib import Path

try:
    from PIL import Image
    import io as _io
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("WARNING: Pillow not installed. Run: python -m pip install Pillow")
    print("Continuing anyway — images will be saved as .jpg without cropping.\n")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept":     "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer":    "https://www.google.com/",
}

# slug -> list of URLs to try in order (first working one wins)
GAMES = {
    # ── Already working on famobi ──────────────────────────────────────────
    "1v1-lol":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/1v1LolTeaser.jpg"],
    "2048":               ["https://img.cdn.famobi.com/portal/html5games/images/tmp/2048Teaser.jpg"],
    "agar-io":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/AgarIoTeaser.jpg"],
    "backgammon":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BackgammonTeaser.jpg"],
    "basketball-stars":   ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BasketballStarsTeaser.jpg"],
    "battleship":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BattleshipTeaser.jpg"],
    "bloxorz":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BloxorzTeaser.jpg"],
    "bob-the-robber":     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BobTheRobberTeaser.jpg"],
    "bonk-io":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BonkIoTeaser.jpg"],
    "boxing-random":      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BoxingRandomTeaser.jpg"],
    "breakout":           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BreakoutTeaser.jpg"],
    "buildnow-gg":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BuildNowGGTeaser.jpg"],
    "burnout-drift":      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BurnoutDriftTeaser.jpg"],
    "checkers":           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CheckersTeaser.jpg"],
    "chess":              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/ChessTeaser.jpg"],
    "cookie-clicker":     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CookieClickerTeaser.jpg"],
    "crazy-cars":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CrazyCarsTeaser.jpg"],
    "crossy-road":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CrossyRoadTeaser.jpg"],
    "cut-the-rope":       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CutTheRopeTeaser.jpg"],
    "diep-io":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DiepIoTeaser.jpg"],
    "dino-run":           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DinoRunTeaser.jpg"],
    "drift-boss":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DriftBossTeaser.jpg"],
    "drift-hunters":      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DriftHuntersTeaser.jpg"],
    "flappy-bird":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/FlappyBirdTeaser.jpg"],
    "football-legends":   ["https://img.cdn.famobi.com/portal/html5games/images/tmp/FootballLegendsTeaser.jpg"],
    "friday-night-funkin":["https://img.cdn.famobi.com/portal/html5games/images/tmp/FridayNightFunkinTeaser.jpg"],
    "getaway-shootout":   ["https://img.cdn.famobi.com/portal/html5games/images/tmp/GetawayShootoutTeaser.jpg"],
    "gold-miner":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/GoldMinerTeaser.jpg"],
    "happy-wheels":       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/HappyWheelsTeaser.jpg"],
    "hole-io":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/HoleIoTeaser.jpg"],
    "jetpack-joyride":    ["https://img.cdn.famobi.com/portal/html5games/images/tmp/JetpackJoyrideTeaser.jpg"],
    "kingdom-rush":       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/KingdomRushTeaser.jpg"],
    "mahjong":            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MahjongTeaser.jpg"],
    "minecraft-classic":  ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MinecraftTeaser.jpg"],
    "minesweeper":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MinesweeperTeaser.jpg"],
    "moomoo-io":          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MoomooIoTeaser.jpg"],
    "moto-x3m":           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MotoX3mTeaser.jpg"],
    "moto-x3m-pool-party":["https://img.cdn.famobi.com/portal/html5games/images/tmp/MotoX3mPoolPartyTeaser.jpg"],
    "narrow-one":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/NarrowOneTeaser.jpg"],
    "paper-io-2":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PaperIo2Teaser.jpg"],
    "penalty-shooters":   ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PenaltyShootersTeaser.jpg"],
    "racing-limits":      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RacingLimitsTeaser.jpg"],
    "red-ball-4":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RedBall4Teaser.jpg"],
    "rooftop-snipers":    ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RooftopSnipersTeaser.jpg"],
    "run-3":              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/Run3Teaser.jpg"],
    "shell-shockers":     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/ShellShockersTeaser.jpg"],
    "simon-says":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SimonSaysTeaser.jpg"],
    "slither-io":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SlitherIoTeaser.jpg"],
    "slope":              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SlopeTeaser.jpg"],
    "smash-karts":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SmashKartsTeaser.jpg"],
    "snail-bob":          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SnailBobTeaser.jpg"],
    "snake":              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SnakeTeaser.jpg"],
    "soccer-random":      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SoccerRandomTeaser.jpg"],
    "solitaire":          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SolitaireTeaser.jpg"],
    "space-is-key":       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SpaceIsKeyTeaser.jpg"],
    "space-waves":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SpaceWavesTeaser.jpg"],
    "stickman-hook":      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/StickmanHookTeaser.jpg"],
    "subway-surfers":     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SubwaySurfersTeaser.jpg"],
    "sudoku":             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SudokuTeaser.jpg"],
    "temple-run-2":       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TempleRun2Teaser.jpg"],
    "tennis-legends":     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TennisLegendsTeaser.jpg"],
    "tetris":             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TetrisTeaser.jpg"],
    "tic-tac-toe":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TicTacToeTeaser.jpg"],
    "tunnel-rush":        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TunnelRushTeaser.jpg"],
    "venge-io":           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/VengeIoTeaser.jpg"],
    "vex-7":              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/Vex7Teaser.jpg"],
    "wings-io":           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/WingsIoTeaser.jpg"],
    "wormate-io":         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/WormateIoTeaser.jpg"],

    # ── The 20 that failed — GamePix CDN + famobi fallbacks ───────────────
    "asteroids": [
        "https://img.gamepix.com/games/asteroids/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/AsteroidsTeaser.jpg",
    ],
    "bloons-td-5": [
        "https://img.gamepix.com/games/bloons-td-5/icon/256.jpg",
        "https://img.gamepix.com/games/bloons-tower-defense-5/icon/256.jpg",
    ],
    "cubes-2048": [
        "https://img.gamepix.com/games/cubes-2048/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/Cubes2048Teaser.jpg",
    ],
    "ev-io": [
        "https://img.gamepix.com/games/ev-io/icon/256.jpg",
        "https://img.gamepix.com/games/evio/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/EvIoTeaser.jpg",
    ],
    "fireboy-watergirl": [
        "https://img.gamepix.com/games/fireboy-and-watergirl/icon/256.jpg",
        "https://img.gamepix.com/games/fireboy-watergirl/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/FireboyAndWatergirlTeaser.jpg",
    ],
    "fireboy-watergirl-2": [
        "https://img.gamepix.com/games/fireboy-and-watergirl-2/icon/256.jpg",
        "https://img.gamepix.com/games/fireboy-watergirl-2/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/FireboyAndWatergirl2Teaser.jpg",
    ],
    "geometry-dash-lite": [
        "https://img.gamepix.com/games/geometry-dash-lite/icon/256.jpg",
        "https://img.gamepix.com/games/geometry-dash/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/GeometryDashTeaser.jpg",
    ],
    "golf-battle": [
        "https://img.gamepix.com/games/golf-battle/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/GolfBattleTeaser.jpg",
    ],
    "highway-racer-3d": [
        "https://img.gamepix.com/games/highway-racer-3d/icon/256.jpg",
        "https://img.gamepix.com/games/highway-racer/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/HighwayRacer3DTeaser.jpg",
    ],
    "krunker": [
        "https://img.gamepix.com/games/krunker-io/icon/256.jpg",
        "https://img.gamepix.com/games/krunker/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/KrunkerTeaser.jpg",
    ],
    "memory-match": [
        "https://img.gamepix.com/games/memory-match/icon/256.jpg",
        "https://img.gamepix.com/games/memory/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/MemoryMatchTeaser.jpg",
    ],
    "pandemic": [
        "https://img.gamepix.com/games/pandemic/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/PandemicTeaser.jpg",
    ],
    "pong": [
        "https://img.gamepix.com/games/pong/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/PongTeaser.jpg",
    ],
    "pong-2p": [
        "https://img.gamepix.com/games/pong/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/PongTeaser.jpg",
    ],
    "road-fury": [
        "https://img.gamepix.com/games/road-fury/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/RoadFuryTeaser.jpg",
    ],
    "stickman-soccer": [
        "https://img.gamepix.com/games/stickman-soccer/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/StickmanSoccerTeaser.jpg",
    ],
    "surviv-io": [
        "https://img.gamepix.com/games/surviv-io/icon/256.jpg",
        "https://img.gamepix.com/games/survivio/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/SurvivIoTeaser.jpg",
    ],
    "traffic-jam-3d": [
        "https://img.gamepix.com/games/traffic-jam-3d/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/TrafficJam3DTeaser.jpg",
    ],
    "wordle": [
        "https://img.gamepix.com/games/wordle/icon/256.jpg",
        "https://img.gamepix.com/games/wordle-unlimited/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/WordleTeaser.jpg",
    ],
    "zombs-royale": [
        "https://img.gamepix.com/games/zombs-royale/icon/256.jpg",
        "https://img.gamepix.com/games/zombsroyale/icon/256.jpg",
        "https://img.cdn.famobi.com/portal/html5games/images/tmp/ZombsRoyaleTeaser.jpg",
    ],
}


def try_download(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as r:
            if r.status == 200:
                data = r.read()
                if len(data) > 5000:
                    return data
    except Exception:
        pass
    return None


def save_icon(data, out_png):
    if not HAS_PILLOW:
        out_png.with_suffix('.jpg').write_bytes(data)
        return
    try:
        img = Image.open(_io.BytesIO(data)).convert("RGB")
        w, h = img.size
        side = min(w, h)
        img = img.crop(((w - side) // 2, (h - side) // 2,
                        (w + side) // 2, (h + side) // 2))
        img = img.resize((256, 256), Image.LANCZOS)
        img.save(out_png, "PNG", optimize=True)
    except Exception as e:
        print(f"(save err: {e})", end=" ")


def process(slug, urls, out_dir):
    out_png = out_dir / f"{slug}.png"
    out_svg = out_dir / f"{slug}.svg"

    # Skip already downloaded
    if out_png.exists() and out_png.stat().st_size > 5000:
        return "skip", ""

    for url in urls:
        data = try_download(url)
        if data:
            save_icon(data, out_png)
            if out_svg.exists():
                out_svg.unlink()
            return "ok", url.split('/')[2].replace('img.cdn.', '')
    return "fail", ""


def main():
    script_dir = Path(__file__).parent
    icon_dir = script_dir / "public" / "icons"

    if not icon_dir.exists():
        print(f"Error: {icon_dir} not found. Run from project root.")
        sys.exit(1)

    total = len(GAMES)
    ok = skip = fail = 0
    failed = []

    print(f"CycloneX Icon Downloader v4  ({total} games)\n{'='*52}")
    print("Skipping already-downloaded icons.\n")

    for i, (slug, urls) in enumerate(GAMES.items(), 1):
        sys.stdout.write(f"  [{i:2}/{total}] {slug:<28} ")
        sys.stdout.flush()

        result, src = process(slug, urls, icon_dir)

        if result == "skip":
            skip += 1
            print("- already done")
        elif result == "ok":
            ok += 1
            print(f"✓ {src}")
        else:
            fail += 1
            failed.append(slug)
            print("✗ failed")

        time.sleep(0.08)

    print(f"\n{'='*52}")
    print(f"✓ {ok} new   - {skip} skipped   ✗ {fail} failed")

    if failed:
        print(f"\nStill missing ({len(failed)}):")
        for s in failed:
            print(f"  • {s}")

    print("\nDone! Redeploy your project.")


if __name__ == "__main__":
    main()
