# Run this from: C:\Users\w\CYX-browser\public\icons\
# Command: cd C:\Users\w\CYX-browser\public\icons && python download-thumbnails.py
# It downloads all game thumbnails as JPG files directly to the icons folder.

import urllib.request, os, time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.crazygames.com/'
}

downloads = {
    "1v1-lol":           "https://images.crazygames.com/1v1-lol_16x9/auto/auto/1v1-lol_16x9-cover.jpg",
    "agar-io":           "https://images.crazygames.com/agario_16x9/auto/auto/agario_16x9-cover.jpg",
    "asteroids":         "https://images.crazygames.com/asteroids_16x9/auto/auto/asteroids_16x9-cover.jpg",
    "backgammon":        "https://images.crazygames.com/backgammon_16x9/auto/auto/backgammon_16x9-cover.jpg",
    "basketball-stars":  "https://images.crazygames.com/basketball-stars_16x9/auto/auto/basketball-stars_16x9-cover.jpg",
    "battleship":        "https://images.crazygames.com/battleship_16x9/auto/auto/battleship_16x9-cover.jpg",
    "bloons-td-5":       "https://images.crazygames.com/bloons-tower-defense-5_16x9/auto/auto/bloons-tower-defense-5_16x9-cover.jpg",
    "bloxorz":           "https://images.crazygames.com/bloxorz_16x9/auto/auto/bloxorz_16x9-cover.jpg",
    "bob-the-robber":    "https://images.crazygames.com/bob-the-robber_16x9/auto/auto/bob-the-robber_16x9-cover.jpg",
    "bonk-io":           "https://images.crazygames.com/bonk-io_16x9/auto/auto/bonk-io_16x9-cover.jpg",
    "boxing-random":     "https://images.crazygames.com/boxing-random_16x9/auto/auto/boxing-random_16x9-cover.jpg",
    "breakout":          "https://images.crazygames.com/breakout_16x9/auto/auto/breakout_16x9-cover.jpg",
    "buildnow-gg":       "https://images.crazygames.com/buildnow-gg_16x9/auto/auto/buildnow-gg_16x9-cover.jpg",
    "burnout-drift":     "https://images.crazygames.com/burnout-drift_16x9/auto/auto/burnout-drift_16x9-cover.jpg",
    "checkers":          "https://images.crazygames.com/checkers_16x9/auto/auto/checkers_16x9-cover.jpg",
    "chess":             "https://images.crazygames.com/chess_16x9/auto/auto/chess_16x9-cover.jpg",
    "cookie-clicker":    "https://images.crazygames.com/cookie-clicker_16x9/auto/auto/cookie-clicker_16x9-cover.jpg",
    "crazy-cars":        "https://images.crazygames.com/crazy-cars_16x9/auto/auto/crazy-cars_16x9-cover.jpg",
    "crossy-road":       "https://images.crazygames.com/crossy-road-online_16x9/auto/auto/crossy-road-online_16x9-cover.jpg",
    "cubes-2048":        "https://images.crazygames.com/cubes-2048_16x9/auto/auto/cubes-2048_16x9-cover.jpg",
    "diep-io":           "https://images.crazygames.com/diepio_16x9/auto/auto/diepio_16x9-cover.jpg",
    "dino-run":          "https://images.crazygames.com/dino-run_16x9/auto/auto/dino-run_16x9-cover.jpg",
    "drift-boss":        "https://images.crazygames.com/drift-boss_16x9/auto/auto/drift-boss_16x9-cover.jpg",
    "drift-hunters":     "https://images.crazygames.com/drift-hunters_16x9/auto/auto/drift-hunters_16x9-cover.jpg",
    "ev-io":             "https://images.crazygames.com/ev-io_16x9/auto/auto/ev-io_16x9-cover.jpg",
    "fireboy-watergirl":   "https://images.crazygames.com/fireboy-and-watergirl-1-forest-temple_16x9/auto/auto/fireboy-and-watergirl-1-forest-temple_16x9-cover.jpg",
    "fireboy-watergirl-2": "https://images.crazygames.com/fireboy-and-watergirl-2-light-temple_16x9/auto/auto/fireboy-and-watergirl-2-light-temple_16x9-cover.jpg",
    "flappy-bird":       "https://images.crazygames.com/flappy-bird_16x9/auto/auto/flappy-bird_16x9-cover.jpg",
    "football-legends":  "https://images.crazygames.com/football-legends-2021_16x9/auto/auto/football-legends-2021_16x9-cover.jpg",
    "friday-night-funkin": "https://images.crazygames.com/friday-night-funkin_16x9/auto/auto/friday-night-funkin_16x9-cover.jpg",
    "geometry-dash-lite": "https://images.crazygames.com/geometry-dash_16x9/auto/auto/geometry-dash_16x9-cover.jpg",
    "getaway-shootout":  "https://images.crazygames.com/getaway-shootout_16x9/auto/auto/getaway-shootout_16x9-cover.jpg",
    "gold-miner":        "https://images.crazygames.com/gold-miner_16x9/auto/auto/gold-miner_16x9-cover.jpg",
    "golf-battle":       "https://images.crazygames.com/golf-battle_16x9/auto/auto/golf-battle_16x9-cover.jpg",
    "happy-wheels":      "https://images.crazygames.com/happy-wheels_16x9/auto/auto/happy-wheels_16x9-cover.jpg",
    "highway-racer-3d":  "https://images.crazygames.com/highway-racer-3d_16x9/auto/auto/highway-racer-3d_16x9-cover.jpg",
    "hole-io":           "https://images.crazygames.com/hole-io_16x9/auto/auto/hole-io_16x9-cover.jpg",
    "kingdom-rush":      "https://images.crazygames.com/kingdom-rush_16x9/auto/auto/kingdom-rush_16x9-cover.jpg",
    "krunker":           "https://images.crazygames.com/krunker-io_16x9/auto/auto/krunker-io_16x9-cover.jpg",
    "memory-match":      "https://images.crazygames.com/memory-match_16x9/auto/auto/memory-match_16x9-cover.jpg",
    "minesweeper":       "https://images.crazygames.com/minesweeper_16x9/auto/auto/minesweeper_16x9-cover.jpg",
    "moomoo-io":         "https://images.crazygames.com/moomoo-io_16x9/auto/auto/moomoo-io_16x9-cover.jpg",
    "narrow-one":        "https://images.crazygames.com/narrow-one_16x9/auto/auto/narrow-one_16x9-cover.jpg",
    "pandemic":          "https://images.crazygames.com/pandemic_16x9/auto/auto/pandemic_16x9-cover.jpg",
    "paper-io-2":        "https://images.crazygames.com/paperio-2_16x9/auto/auto/paperio-2_16x9-cover.jpg",
    "penalty-shooters":  "https://images.crazygames.com/penalty-shooters-2_16x9/auto/auto/penalty-shooters-2_16x9-cover.jpg",
    "pong":              "https://images.crazygames.com/pong_16x9/auto/auto/pong_16x9-cover.jpg",
    "pong-2p":           "https://images.crazygames.com/pong_16x9/auto/auto/pong_16x9-cover.jpg",
    "racing-limits":     "https://images.crazygames.com/racing-limits_16x9/auto/auto/racing-limits_16x9-cover.jpg",
    "red-ball-4":        "https://images.crazygames.com/red-ball-4_16x9/auto/auto/red-ball-4_16x9-cover.jpg",
    "road-fury":         "https://images.crazygames.com/road-fury_16x9/auto/auto/road-fury_16x9-cover.jpg",
    "rooftop-snipers":   "https://images.crazygames.com/rooftop-snipers_16x9/auto/auto/rooftop-snipers_16x9-cover.jpg",
    "run-3":             "https://images.crazygames.com/run-3_16x9/auto/auto/run-3_16x9-cover.jpg",
    "shell-shockers":    "https://images.crazygames.com/shell-shockers_16x9/auto/auto/shell-shockers_16x9-cover.jpg",
    "simon-says":        "https://images.crazygames.com/simon-says_16x9/auto/auto/simon-says_16x9-cover.jpg",
    "slither-io":        "https://images.crazygames.com/slither-io_16x9/auto/auto/slither-io_16x9-cover.jpg",
    "snail-bob":         "https://images.crazygames.com/snail-bob_16x9/auto/auto/snail-bob_16x9-cover.jpg",
    "snake":             "https://images.crazygames.com/snake_16x9/auto/auto/snake_16x9-cover.jpg",
    "soccer-random":     "https://images.crazygames.com/soccer-random_16x9/auto/auto/soccer-random_16x9-cover.jpg",
    "space-is-key":      "https://images.crazygames.com/space-is-key_16x9/auto/auto/space-is-key_16x9-cover.jpg",
    "space-waves":       "https://images.crazygames.com/space-waves_16x9/auto/auto/space-waves_16x9-cover.jpg",
    "stickman-hook":     "https://images.crazygames.com/stickman-hook_16x9/auto/auto/stickman-hook_16x9-cover.jpg",
    "stickman-soccer":   "https://images.crazygames.com/stickman-soccer_16x9/auto/auto/stickman-soccer_16x9-cover.jpg",
    "subway-surfers":    "https://images.crazygames.com/subway-surfers_16x9/auto/auto/subway-surfers_16x9-cover.jpg",
    "surviv-io":         "https://images.crazygames.com/surviv-io_16x9/auto/auto/surviv-io_16x9-cover.jpg",
    "temple-run-2":      "https://images.crazygames.com/temple-run-2_16x9/auto/auto/temple-run-2_16x9-cover.jpg",
    "tennis-legends":    "https://images.crazygames.com/tennis-legends-2021_16x9/auto/auto/tennis-legends-2021_16x9-cover.jpg",
    "tetris":            "https://images.crazygames.com/tetris_16x9/auto/auto/tetris_16x9-cover.jpg",
    "tic-tac-toe":       "https://images.crazygames.com/tic-tac-toe_16x9/auto/auto/tic-tac-toe_16x9-cover.jpg",
    "traffic-jam-3d":    "https://images.crazygames.com/traffic-jam-3d_16x9/auto/auto/traffic-jam-3d_16x9-cover.jpg",
    "tunnel-rush":       "https://images.crazygames.com/tunnel-rush_16x9/auto/auto/tunnel-rush_16x9-cover.jpg",
    "venge-io":          "https://images.crazygames.com/venge-io_16x9/auto/auto/venge-io_16x9-cover.jpg",
    "vex-7":             "https://images.crazygames.com/vex-7_16x9/auto/auto/vex-7_16x9-cover.jpg",
    "wings-io":          "https://images.crazygames.com/wings-io_16x9/auto/auto/wings-io_16x9-cover.jpg",
    "wordle":            "https://images.crazygames.com/wordle-unlimited_16x9/auto/auto/wordle-unlimited_16x9-cover.jpg",
    "wormate-io":        "https://images.crazygames.com/wormate-io_16x9/auto/auto/wormate-io_16x9-cover.jpg",
    "zombs-royale":      "https://images.crazygames.com/zombsroyale-io_16x9/auto/auto/zombsroyale-io_16x9-cover.jpg",
}

ok, skip, fail = 0, 0, 0
for slug, url in downloads.items():
    fname = f'{slug}.jpg'
    if os.path.exists(fname):
        print(f'skip {fname}')
        skip += 1
        continue
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(fname, 'wb') as f:
            f.write(data)
        print(f'OK   {fname} ({len(data):,} bytes)')
        ok += 1
        time.sleep(0.2)  # be polite
    except Exception as e:
        print(f'FAIL {fname}: {e}')
        fail += 1

print(f'\nDone: {ok} downloaded, {skip} skipped, {fail} failed')
if fail == 0:
    print('\nAll good! Now run:')
    print('  cd C:\\Users\\w\\CYX-browser')
    print('  git add public/icons/')
    print('  git commit -m "Add all game thumbnail JPGs"')
    print('  git push origin main')
