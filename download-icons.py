#!/usr/bin/env python3
"""
CycloneX Game Icon Downloader  v2
===================================
Downloads real game cover images and saves them as square PNG files
into public/icons/ (replacing the old SVG emoji placeholders).

Run from the root of your CYX project:
    python download-icons.py

Requirements: pip install Pillow
  (without Pillow it saves .jpg files instead of cropped PNGs)
"""

import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

try:
    from PIL import Image
    import io as _io
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("⚠  Pillow not installed — PNGs won't be square-cropped.")
    print("   For best results: pip install Pillow\n")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Referer":    "https://www.google.com/",
    "Accept":     "image/webp,image/apng,image/*,*/*;q=0.8",
}

# ──────────────────────────────────────────────────────────────────────────────
# slug -> (display_name, [url_primary, url_fallback1, url_fallback2, ...])
#
# Sources used:
#   famobi CDN  – public game portal, real cover art, no hotlink block
#   sz-games    – open-source GitHub game hub, has cover folder
#   gamemonetize– public game directory thumbnails
# ──────────────────────────────────────────────────────────────────────────────
GAMES = {
  "1v1-lol":            ("1v1.LOL",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/1v1LolTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/1v1lol.jpg"]),
  "2048":               ("2048",                 ["https://img.cdn.famobi.com/portal/html5games/images/tmp/2048Teaser.jpg",                "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/2048.jpg"]),
  "agar-io":            ("Agar.io",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/AgarIoTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/agario.jpg"]),
  "asteroids":          ("Asteroids",            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/AsteroidsTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/asteroids.jpg"]),
  "backgammon":         ("Backgammon",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BackgammonTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/backgammon.jpg"]),
  "basketball-stars":   ("Basketball Stars",     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BasketballStarsTeaser.jpg",     "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/basketball-stars.jpg"]),
  "battleship":         ("Battleship",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BattleshipTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/battleship.jpg"]),
  "bloons-td-5":        ("Bloons TD 5",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BloonsTd5Teaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/bloons-td5.jpg"]),
  "bloxorz":            ("Bloxorz",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BloxorzTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/bloxorz.jpg"]),
  "bob-the-robber":     ("Bob The Robber",       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BobTheRobberTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/bob-the-robber.jpg"]),
  "bonk-io":            ("Bonk.io",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BonkIoTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/bonk-io.jpg"]),
  "boxing-random":      ("Boxing Random",        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BoxingRandomTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/boxing-random.jpg"]),
  "breakout":           ("Breakout",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BreakoutTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/breakout.jpg"]),
  "buildnow-gg":        ("Buildnow.gg",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BuildNowGGTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/buildnow-gg.jpg"]),
  "burnout-drift":      ("Burnout Drift",        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/BurnoutDriftTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/burnout-drift.jpg"]),
  "checkers":           ("Checkers",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CheckersTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/checkers.jpg"]),
  "chess":              ("Chess",                ["https://img.cdn.famobi.com/portal/html5games/images/tmp/ChessTeaser.jpg",               "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/chess.jpg"]),
  "cookie-clicker":     ("Cookie Clicker",       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CookieClickerTeaser.jpg",       "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/cookie-clicker.jpg"]),
  "crazy-cars":         ("Crazy Cars",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CrazyCarsTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/crazy-cars.jpg"]),
  "crossy-road":        ("Crossy Road",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CrossyRoadTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/crossy-road.jpg"]),
  "cubes-2048":         ("Cubes 2048",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/Cubes2048Teaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/cubes-2048.jpg"]),
  "cut-the-rope":       ("Cut the Rope",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/CutTheRopeTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/cut-the-rope.jpg"]),
  "diep-io":            ("Diep.io",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DiepIoTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/diep-io.jpg"]),
  "dino-run":           ("Dino Run",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DinoRunTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/dino-run.jpg"]),
  "drift-boss":         ("Drift Boss",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DriftBossTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/drift-boss.jpg"]),
  "drift-hunters":      ("Drift Hunters",        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/DriftHuntersTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/drift-hunters.jpg"]),
  "ev-io":              ("Ev.io",                ["https://img.cdn.famobi.com/portal/html5games/images/tmp/EvIoTeaser.jpg",                "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/ev-io.jpg"]),
  "fireboy-watergirl":  ("Fireboy & Watergirl",  ["https://img.cdn.famobi.com/portal/html5games/images/tmp/FireboyAndWatergirlTeaser.jpg", "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/fireboy-watergirl.jpg"]),
  "fireboy-watergirl-2":("Fireboy & Watergirl 2",["https://img.cdn.famobi.com/portal/html5games/images/tmp/FireboyAndWatergirl2Teaser.jpg","https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/fireboy-watergirl-2.jpg"]),
  "flappy-bird":        ("Flappy Bird",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/FlappyBirdTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/flappy-bird.jpg"]),
  "football-legends":   ("Football Legends",     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/FootballLegendsTeaser.jpg",     "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/football-legends.jpg"]),
  "friday-night-funkin":("Friday Night Funkin",  ["https://img.cdn.famobi.com/portal/html5games/images/tmp/FridayNightFunkinTeaser.jpg",   "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/friday-night-funkin.jpg"]),
  "geometry-dash-lite": ("Geometry Dash Lite",   ["https://img.cdn.famobi.com/portal/html5games/images/tmp/GeometryDashTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/geometry-dash.jpg"]),
  "getaway-shootout":   ("Getaway Shootout",     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/GetawayShootoutTeaser.jpg",     "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/getaway-shootout.jpg"]),
  "gold-miner":         ("Gold Miner",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/GoldMinerTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/gold-miner.jpg"]),
  "golf-battle":        ("Golf Battle",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/GolfBattleTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/golf-battle.jpg"]),
  "happy-wheels":       ("Happy Wheels",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/HappyWheelsTeaser.jpg",         "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/happy-wheels.jpg"]),
  "highway-racer-3d":   ("Highway Racer 3D",     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/HighwayRacer3DTeaser.jpg",      "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/highway-racer-3d.jpg"]),
  "hole-io":            ("Hole.io",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/HoleIoTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/hole-io.jpg"]),
  "jetpack-joyride":    ("Jetpack Joyride",      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/JetpackJoyrideTeaser.jpg",      "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/jetpack-joyride.jpg"]),
  "kingdom-rush":       ("Kingdom Rush",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/KingdomRushTeaser.jpg",         "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/kingdom-rush.jpg"]),
  "krunker":            ("Krunker",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/KrunkerTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/krunker.jpg"]),
  "mahjong":            ("Mahjong",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MahjongTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/mahjong.jpg"]),
  "memory-match":       ("Memory Match",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MemoryMatchTeaser.jpg",         "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/memory-match.jpg"]),
  "minecraft-classic":  ("Minecraft Classic",    ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MinecraftTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/Minecraft.png"]),
  "minesweeper":        ("Minesweeper",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MinesweeperTeaser.jpg",         "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/minesweeper.jpg"]),
  "moomoo-io":          ("Moomoo.io",            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MoomooIoTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/moomoo-io.jpg"]),
  "moto-x3m":           ("Moto X3M",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MotoX3mTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/moto-x3m.jpg"]),
  "moto-x3m-pool-party":("Moto X3M Pool Party",  ["https://img.cdn.famobi.com/portal/html5games/images/tmp/MotoX3mPoolPartyTeaser.jpg",    "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/moto-x3m-pool-party.jpg"]),
  "narrow-one":         ("Narrow.one",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/NarrowOneTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/narrow-one.jpg"]),
  "pandemic":           ("Pandemic",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PandemicTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/pandemic.jpg"]),
  "paper-io-2":         ("Paper.io 2",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PaperIo2Teaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/paper-io-2.jpg"]),
  "penalty-shooters":   ("Penalty Shooters",     ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PenaltyShootersTeaser.jpg",     "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/penalty-shooters.jpg"]),
  "pong":               ("Pong",                 ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PongTeaser.jpg",                "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/pong.jpg"]),
  "pong-2p":            ("Pong 2P",              ["https://img.cdn.famobi.com/portal/html5games/images/tmp/PongTeaser.jpg",                "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/pong.jpg"]),
  "racing-limits":      ("Racing Limits",        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RacingLimitsTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/racing-limits.jpg"]),
  "red-ball-4":         ("Red Ball 4",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RedBall4Teaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/red-ball-4.jpg"]),
  "road-fury":          ("Road Fury",            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RoadFuryTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/road-fury.jpg"]),
  "rooftop-snipers":    ("Rooftop Snipers",      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/RooftopSnipersTeaser.jpg",      "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/rooftop-snipers.jpg"]),
  "run-3":              ("Run 3",                ["https://img.cdn.famobi.com/portal/html5games/images/tmp/Run3Teaser.jpg",                "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/run-3.jpg"]),
  "shell-shockers":     ("Shell Shockers",       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/ShellShockersTeaser.jpg",       "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/shell-shockers.jpg"]),
  "simon-says":         ("Simon Says",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SimonSaysTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/simon-says.jpg"]),
  "slither-io":         ("Slither.io",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SlitherIoTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/slither-io.jpg"]),
  "slope":              ("Slope",                ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SlopeTeaser.jpg",               "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/slope.webp"]),
  "smash-karts":        ("Smash Karts",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SmashKartsTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/smash-karts.jpg"]),
  "snail-bob":          ("Snail Bob",            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SnailBobTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/snail-bob.jpg"]),
  "snake":              ("Snake",                ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SnakeTeaser.jpg",               "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/snake.jpg"]),
  "soccer-random":      ("Soccer Random",        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SoccerRandomTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/soccer-random.jpg"]),
  "solitaire":          ("Solitaire",            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SolitaireTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/solitaire.jpg"]),
  "space-is-key":       ("Space is Key",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SpaceIsKeyTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/space-is-key.jpg"]),
  "space-waves":        ("Space Waves",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SpaceWavesTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/space-waves.jpg"]),
  "stickman-hook":      ("Stickman Hook",        ["https://img.cdn.famobi.com/portal/html5games/images/tmp/StickmanHookTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/stickman-hook.jpg"]),
  "stickman-soccer":    ("Stickman Soccer",      ["https://img.cdn.famobi.com/portal/html5games/images/tmp/StickmanSoccerTeaser.jpg",      "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/stickman-soccer.jpg"]),
  "subway-surfers":     ("Subway Surfers",       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SubwaySurfersTeaser.jpg",       "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/subway-surfers.jpg"]),
  "sudoku":             ("Sudoku",               ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SudokuTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/sudoku.jpg"]),
  "surviv-io":          ("Surviv.io",            ["https://img.cdn.famobi.com/portal/html5games/images/tmp/SurvivIoTeaser.jpg",            "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/surviv-io.jpg"]),
  "temple-run-2":       ("Temple Run 2",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TempleRun2Teaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/temple-run-2.jpg"]),
  "tennis-legends":     ("Tennis Legends",       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TennisLegendsTeaser.jpg",       "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/tennis-legends.jpg"]),
  "tetris":             ("Tetris",               ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TetrisTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/tetris.jpg"]),
  "tic-tac-toe":        ("Tic Tac Toe",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TicTacToeTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/tic-tac-toe.jpg"]),
  "traffic-jam-3d":     ("Traffic Jam 3D",       ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TrafficJam3DTeaser.jpg",        "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/traffic-jam-3d.jpg"]),
  "tunnel-rush":        ("Tunnel Rush",          ["https://img.cdn.famobi.com/portal/html5games/images/tmp/TunnelRushTeaser.jpg",          "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/tunnel-rush.jpg"]),
  "venge-io":           ("Venge.io",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/VengeIoTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/venge-io.jpg"]),
  "vex-7":              ("Vex 7",                ["https://img.cdn.famobi.com/portal/html5games/images/tmp/Vex7Teaser.jpg",                "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/vex-7.jpg"]),
  "wings-io":           ("Wings.io",             ["https://img.cdn.famobi.com/portal/html5games/images/tmp/WingsIoTeaser.jpg",             "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/wings-io.jpg"]),
  "wordle":             ("Wordle",               ["https://img.cdn.famobi.com/portal/html5games/images/tmp/WordleTeaser.jpg",              "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/wordle.jpg"]),
  "wormate-io":         ("Wormate.io",           ["https://img.cdn.famobi.com/portal/html5games/images/tmp/WormateIoTeaser.jpg",           "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/wormate-io.jpg"]),
  "zombs-royale":       ("Zombs Royale",         ["https://img.cdn.famobi.com/portal/html5games/images/tmp/ZombsRoyaleTeaser.jpg",         "https://raw.githubusercontent.com/sz-games/sz-games.github.io/main/cover/zombs-royale.jpg"]),
}


def try_download(url):
    """Attempt to download URL. Returns bytes if successful (>5KB), else None."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            if resp.status == 200:
                data = resp.read()
                if len(data) > 5000:   # reject HTML error pages
                    return data
    except Exception:
        pass
    return None


def save_icon(data, out_png):
    """Save image data as a 256x256 square PNG. Falls back to .jpg if no Pillow."""
    if not HAS_PILLOW:
        jpg = out_png.with_suffix('.jpg')
        jpg.write_bytes(data)
        return jpg
    img = Image.open(_io.BytesIO(data)).convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w + side) // 2, (h + side) // 2))
    img = img.resize((256, 256), Image.LANCZOS)
    img.save(out_png, "PNG", optimize=True)
    return out_png


def process_game(slug, name, urls, out_dir):
    out_png = out_dir / f"{slug}.png"
    out_svg = out_dir / f"{slug}.svg"

    for url in urls:
        data = try_download(url)
        if data:
            saved = save_icon(data, out_png)
            if out_svg.exists():
                out_svg.unlink()   # remove old SVG
            return True, url.split('/')[2]   # return domain for display
    return False, None


def main():
    script_dir = Path(__file__).parent
    icon_dirs  = [
        script_dir / "public" / "icons",
        script_dir / "public" / "icons" / "icons",
    ]

    total = len(GAMES)
    ok = fail = 0
    failed = []

    print(f"CycloneX Icon Downloader v2  ({total} games)\n{'='*52}")

    for d in icon_dirs:
        if not d.exists():
            print(f"⚠  Skipping (not found): {d}")
            continue

        print(f"\n📁  {d.relative_to(script_dir)}\n{'-'*40}")

        for i, (slug, (name, urls)) in enumerate(GAMES.items(), 1):
            sys.stdout.write(f"  [{i:2}/{total}] {name:<26}")
            sys.stdout.flush()

            success, src = process_game(slug, name, urls, d)
            if success:
                ok += 1
                print(f" ✓  {src}")
            else:
                fail += 1
                failed.append(name)
                print(" ✗  all sources failed")

            time.sleep(0.08)   # be polite

    print(f"\n{'='*52}")
    print(f"Done!  ✓ {ok} saved   ✗ {fail} failed")
    if failed:
        print("\nStill using SVG fallback for:")
        for n in failed:
            print(f"  • {n}")
    print("\nNow re-zip the project and redeploy!")


if __name__ == "__main__":
    main()
