# Run from: C:\Users\w\CYX-browser\public\icons\
# Command:  python download-thumbnails.py

import urllib.request, os, time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept":     "image/webp,image/apng,image/*,*/*;q=0.8",
    "Referer":    "https://www.google.com/",
}

BASE = "https://img.cdn.famobi.com/portal/html5games/images/tmp/"

DOWNLOADS = {
    "1v1-lol":              BASE + "1v1LolTeaser.jpg",
    "2048":                 BASE + "2048Teaser.jpg",
    "agar-io":              BASE + "AgarIoTeaser.jpg",
    "asteroids":            BASE + "AsteroidsTeaser.jpg",
    "backgammon":           BASE + "BackgammonTeaser.jpg",
    "basketball-stars":     BASE + "BasketballStarsTeaser.jpg",
    "battleship":           BASE + "BattleshipTeaser.jpg",
    "bloons-td-5":          BASE + "BloonsTd5Teaser.jpg",
    "bloxorz":              BASE + "BloxorzTeaser.jpg",
    "bob-the-robber":       BASE + "BobTheRobberTeaser.jpg",
    "bonk-io":              BASE + "BonkIoTeaser.jpg",
    "boxing-random":        BASE + "BoxingRandomTeaser.jpg",
    "breakout":             BASE + "BreakoutTeaser.jpg",
    "buildnow-gg":          BASE + "BuildNowGGTeaser.jpg",
    "burnout-drift":        BASE + "BurnoutDriftTeaser.jpg",
    "checkers":             BASE + "CheckersTeaser.jpg",
    "chess":                BASE + "ChessTeaser.jpg",
    "cookie-clicker":       BASE + "CookieClickerTeaser.jpg",
    "crazy-cars":           BASE + "CrazyCarsTeaser.jpg",
    "crossy-road":          BASE + "CrossyRoadTeaser.jpg",
    "cubes-2048":           BASE + "Cubes2048Teaser.jpg",
    "cut-the-rope":         BASE + "CutTheRopeTeaser.jpg",
    "diep-io":              BASE + "DiepIoTeaser.jpg",
    "dino-run":             BASE + "DinoRunTeaser.jpg",
    "drift-boss":           BASE + "DriftBossTeaser.jpg",
    "drift-hunters":        BASE + "DriftHuntersTeaser.jpg",
    "ev-io":                BASE + "EvIoTeaser.jpg",
    "fireboy-watergirl":    BASE + "FireboyAndWatergirlTeaser.jpg",
    "fireboy-watergirl-2":  BASE + "FireboyAndWatergirl2Teaser.jpg",
    "flappy-bird":          BASE + "FlappyBirdTeaser.jpg",
    "football-legends":     BASE + "FootballLegendsTeaser.jpg",
    "friday-night-funkin":  BASE + "FridayNightFunkinTeaser.jpg",
    "geometry-dash-lite":   BASE + "GeometryDashTeaser.jpg",
    "getaway-shootout":     BASE + "GetawayShootoutTeaser.jpg",
    "gold-miner":           BASE + "GoldMinerTeaser.jpg",
    "golf-battle":          BASE + "GolfBattleTeaser.jpg",
    "happy-wheels":         BASE + "HappyWheelsTeaser.jpg",
    "highway-racer-3d":     BASE + "HighwayRacer3DTeaser.jpg",
    "hole-io":              BASE + "HoleIoTeaser.jpg",
    "jetpack-joyride":      BASE + "JetpackJoyrideTeaser.jpg",
    "kingdom-rush":         BASE + "KingdomRushTeaser.jpg",
    "krunker":              BASE + "KrunkerTeaser.jpg",
    "mahjong":              BASE + "MahjongTeaser.jpg",
    "memory-match":         BASE + "MemoryMatchTeaser.jpg",
    "minecraft-classic":    BASE + "MinecraftTeaser.jpg",
    "minesweeper":          BASE + "MinesweeperTeaser.jpg",
    "moomoo-io":            BASE + "MoomooIoTeaser.jpg",
    "moto-x3m":             BASE + "MotoX3mTeaser.jpg",
    "moto-x3m-pool-party":  BASE + "MotoX3mPoolPartyTeaser.jpg",
    "narrow-one":           BASE + "NarrowOneTeaser.jpg",
    "pandemic":             BASE + "PandemicTeaser.jpg",
    "paper-io-2":           BASE + "PaperIo2Teaser.jpg",
    "penalty-shooters":     BASE + "PenaltyShootersTeaser.jpg",
    "pong":                 BASE + "PongTeaser.jpg",
    "pong-2p":              BASE + "PongTeaser.jpg",
    "racing-limits":        BASE + "RacingLimitsTeaser.jpg",
    "red-ball-4":           BASE + "RedBall4Teaser.jpg",
    "road-fury":            BASE + "RoadFuryTeaser.jpg",
    "rooftop-snipers":      BASE + "RooftopSnipersTeaser.jpg",
    "run-3":                BASE + "Run3Teaser.jpg",
    "shell-shockers":       BASE + "ShellShockersTeaser.jpg",
    "simon-says":           BASE + "SimonSaysTeaser.jpg",
    "slither-io":           BASE + "SlitherIoTeaser.jpg",
    "slope":                BASE + "SlopeTeaser.jpg",
    "smash-karts":          BASE + "SmashKartsTeaser.jpg",
    "snail-bob":            BASE + "SnailBobTeaser.jpg",
    "snake":                BASE + "SnakeTeaser.jpg",
    "soccer-random":        BASE + "SoccerRandomTeaser.jpg",
    "solitaire":            BASE + "SolitaireTeaser.jpg",
    "space-is-key":         BASE + "SpaceIsKeyTeaser.jpg",
    "space-waves":          BASE + "SpaceWavesTeaser.jpg",
    "stickman-hook":        BASE + "StickmanHookTeaser.jpg",
    "stickman-soccer":      BASE + "StickmanSoccerTeaser.jpg",
    "subway-surfers":       BASE + "SubwaySurfersTeaser.jpg",
    "sudoku":               BASE + "SudokuTeaser.jpg",
    "surviv-io":            BASE + "SurvivIoTeaser.jpg",
    "temple-run-2":         BASE + "TempleRun2Teaser.jpg",
    "tennis-legends":       BASE + "TennisLegendsTeaser.jpg",
    "tetris":               BASE + "TetrisTeaser.jpg",
    "tic-tac-toe":          BASE + "TicTacToeTeaser.jpg",
    "traffic-jam-3d":       BASE + "TrafficJam3DTeaser.jpg",
    "tunnel-rush":          BASE + "TunnelRushTeaser.jpg",
    "venge-io":             BASE + "VengeIoTeaser.jpg",
    "vex-7":                BASE + "Vex7Teaser.jpg",
    "wings-io":             BASE + "WingsIoTeaser.jpg",
    "wordle":               BASE + "WordleTeaser.jpg",
    "wormate-io":           BASE + "WormateIoTeaser.jpg",
    "zombs-royale":         BASE + "ZombsRoyaleTeaser.jpg",
}

ok, skip, fail = 0, 0, 0
for slug, url in DOWNLOADS.items():
    fname = f"{slug}.jpg"
    if os.path.exists(fname):
        print(f"skip {fname}")
        skip += 1
        continue
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(fname, "wb") as f:
            f.write(data)
        print(f"OK   {fname} ({len(data):,} bytes)")
        ok += 1
        time.sleep(0.1)
    except Exception as e:
        print(f"FAIL {fname}: {e}")
        fail += 1

print(f"\nDone: {ok} downloaded, {skip} skipped, {fail} failed")
if fail == 0:
    print("\nAll good! Now run:")
    print("  cd C:\\Users\\w\\CYX-browser")
    print("  git add public/icons/")
    print('  git commit -m "Add all game thumbnails"')
    print("  git push origin main")
