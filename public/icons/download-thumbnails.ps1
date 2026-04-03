# Run this from PowerShell in C:\Users\w\CYX-browser\public\icons\
# Command: cd C:\Users\w\CYX-browser\public\icons; .\download-thumbnails.ps1

$F  = "https://img.cdn.famobi.com/portal/html5games/images/tmp/"
$CG = "https://images.crazygames.com/"

$games = @{
    "1v1-lol"             = @($F+"1v1LolTeaser.jpg",           $CG+"1v1-lol_16x9/auto/auto/1v1-lol_16x9-cover.jpg")
    "2048"                = @($F+"2048Teaser.jpg",              $CG+"2048_16x9/auto/auto/2048_16x9-cover.jpg")
    "agar-io"             = @($F+"AgarIoTeaser.jpg",            $CG+"agario_16x9/auto/auto/agario_16x9-cover.jpg")
    "asteroids"           = @($F+"AsteroidsTeaser.jpg",         $CG+"asteroids_16x9/auto/auto/asteroids_16x9-cover.jpg")
    "backgammon"          = @($F+"BackgammonTeaser.jpg",        $CG+"backgammon_16x9/auto/auto/backgammon_16x9-cover.jpg")
    "basketball-stars"    = @($F+"BasketballStarsTeaser.jpg",   $CG+"basketball-stars_16x9/auto/auto/basketball-stars_16x9-cover.jpg")
    "battleship"          = @($F+"BattleshipTeaser.jpg",        $CG+"battleship_16x9/auto/auto/battleship_16x9-cover.jpg")
    "bloons-td-5"         = @($F+"BloonsTd5Teaser.jpg",         $CG+"bloons-tower-defense-5_16x9/auto/auto/bloons-tower-defense-5_16x9-cover.jpg")
    "bloxorz"             = @($F+"BloxorzTeaser.jpg",           $CG+"bloxorz_16x9/auto/auto/bloxorz_16x9-cover.jpg")
    "bob-the-robber"      = @($F+"BobTheRobberTeaser.jpg",      $CG+"bob-the-robber_16x9/auto/auto/bob-the-robber_16x9-cover.jpg")
    "bonk-io"             = @($F+"BonkIoTeaser.jpg",            $CG+"bonk-io_16x9/auto/auto/bonk-io_16x9-cover.jpg")
    "boxing-random"       = @($F+"BoxingRandomTeaser.jpg",      $CG+"boxing-random_16x9/auto/auto/boxing-random_16x9-cover.jpg")
    "breakout"            = @($F+"BreakoutTeaser.jpg",          $CG+"breakout_16x9/auto/auto/breakout_16x9-cover.jpg")
    "buildnow-gg"         = @($F+"BuildNowGGTeaser.jpg",        $CG+"buildnow-gg_16x9/auto/auto/buildnow-gg_16x9-cover.jpg")
    "burnout-drift"       = @($F+"BurnoutDriftTeaser.jpg",      $CG+"burnout-drift_16x9/auto/auto/burnout-drift_16x9-cover.jpg")
    "checkers"            = @($F+"CheckersTeaser.jpg",          $CG+"checkers_16x9/auto/auto/checkers_16x9-cover.jpg")
    "chess"               = @($F+"ChessTeaser.jpg",             $CG+"chess_16x9/auto/auto/chess_16x9-cover.jpg")
    "cookie-clicker"      = @($F+"CookieClickerTeaser.jpg",     $CG+"cookie-clicker_16x9/auto/auto/cookie-clicker_16x9-cover.jpg")
    "crazy-cars"          = @($F+"CrazyCarsTeaser.jpg",         $CG+"crazy-cars_16x9/auto/auto/crazy-cars_16x9-cover.jpg")
    "crossy-road"         = @($F+"CrossyRoadTeaser.jpg",        $CG+"crossy-road-online_16x9/auto/auto/crossy-road-online_16x9-cover.jpg")
    "cubes-2048"          = @($F+"Cubes2048Teaser.jpg",         $CG+"cubes-2048_16x9/auto/auto/cubes-2048_16x9-cover.jpg")
    "cut-the-rope"        = @($F+"CutTheRopeTeaser.jpg",        $CG+"cut-the-rope_16x9/auto/auto/cut-the-rope_16x9-cover.jpg")
    "diep-io"             = @($F+"DiepIoTeaser.jpg",            $CG+"diepio_16x9/auto/auto/diepio_16x9-cover.jpg")
    "dino-run"            = @($F+"DinoRunTeaser.jpg",           $CG+"dino-run_16x9/auto/auto/dino-run_16x9-cover.jpg")
    "drift-boss"          = @($F+"DriftBossTeaser.jpg",         $CG+"drift-boss_16x9/auto/auto/drift-boss_16x9-cover.jpg")
    "drift-hunters"       = @($F+"DriftHuntersTeaser.jpg",      $CG+"drift-hunters_16x9/auto/auto/drift-hunters_16x9-cover.jpg")
    "ev-io"               = @($F+"EvIoTeaser.jpg",              $CG+"ev-io_16x9/auto/auto/ev-io_16x9-cover.jpg")
    "fireboy-watergirl"   = @($F+"FireboyAndWatergirlTeaser.jpg",   $CG+"fireboy-and-watergirl-1-forest-temple_16x9/auto/auto/fireboy-and-watergirl-1-forest-temple_16x9-cover.jpg")
    "fireboy-watergirl-2" = @($F+"FireboyAndWatergirl2Teaser.jpg",  $CG+"fireboy-and-watergirl-2-light-temple_16x9/auto/auto/fireboy-and-watergirl-2-light-temple_16x9-cover.jpg")
    "flappy-bird"         = @($F+"FlappyBirdTeaser.jpg",        $CG+"flappy-bird_16x9/auto/auto/flappy-bird_16x9-cover.jpg")
    "football-legends"    = @($F+"FootballLegendsTeaser.jpg",   $CG+"football-legends-2021_16x9/auto/auto/football-legends-2021_16x9-cover.jpg")
    "friday-night-funkin" = @($F+"FridayNightFunkinTeaser.jpg", $CG+"friday-night-funkin_16x9/auto/auto/friday-night-funkin_16x9-cover.jpg")
    "geometry-dash-lite"  = @($F+"GeometryDashTeaser.jpg",      $CG+"geometry-dash_16x9/auto/auto/geometry-dash_16x9-cover.jpg")
    "getaway-shootout"    = @($F+"GetawayShootoutTeaser.jpg",   $CG+"getaway-shootout_16x9/auto/auto/getaway-shootout_16x9-cover.jpg")
    "gold-miner"          = @($F+"GoldMinerTeaser.jpg",         $CG+"gold-miner_16x9/auto/auto/gold-miner_16x9-cover.jpg")
    "golf-battle"         = @($F+"GolfBattleTeaser.jpg",        $CG+"golf-battle_16x9/auto/auto/golf-battle_16x9-cover.jpg")
    "happy-wheels"        = @($F+"HappyWheelsTeaser.jpg",       $CG+"happy-wheels_16x9/auto/auto/happy-wheels_16x9-cover.jpg")
    "highway-racer-3d"    = @($F+"HighwayRacer3DTeaser.jpg",    $CG+"highway-racer-3d_16x9/auto/auto/highway-racer-3d_16x9-cover.jpg")
    "hole-io"             = @($F+"HoleIoTeaser.jpg",            $CG+"hole-io_16x9/auto/auto/hole-io_16x9-cover.jpg")
    "jetpack-joyride"     = @($F+"JetpackJoyrideTeaser.jpg",    $CG+"jetpack-joyride_16x9/auto/auto/jetpack-joyride_16x9-cover.jpg")
    "kingdom-rush"        = @($F+"KingdomRushTeaser.jpg",       $CG+"kingdom-rush_16x9/auto/auto/kingdom-rush_16x9-cover.jpg")
    "krunker"             = @($F+"KrunkerTeaser.jpg",           $CG+"krunker-io_16x9/auto/auto/krunker-io_16x9-cover.jpg")
    "mahjong"             = @($F+"MahjongTeaser.jpg",           $CG+"mahjong_16x9/auto/auto/mahjong_16x9-cover.jpg")
    "memory-match"        = @($F+"MemoryMatchTeaser.jpg",       $CG+"memory-match_16x9/auto/auto/memory-match_16x9-cover.jpg")
    "minecraft-classic"   = @($F+"MinecraftTeaser.jpg",         $CG+"minecraft-classic_16x9/auto/auto/minecraft-classic_16x9-cover.jpg")
    "minesweeper"         = @($F+"MinesweeperTeaser.jpg",       $CG+"minesweeper_16x9/auto/auto/minesweeper_16x9-cover.jpg")
    "moomoo-io"           = @($F+"MoomooIoTeaser.jpg",          $CG+"moomoo-io_16x9/auto/auto/moomoo-io_16x9-cover.jpg")
    "moto-x3m"            = @($F+"MotoX3mTeaser.jpg",           $CG+"moto-x3m_16x9/auto/auto/moto-x3m_16x9-cover.jpg")
    "moto-x3m-pool-party" = @($F+"MotoX3mPoolPartyTeaser.jpg",  $CG+"moto-x3m-pool-party_16x9/auto/auto/moto-x3m-pool-party_16x9-cover.jpg")
    "narrow-one"          = @($F+"NarrowOneTeaser.jpg",         $CG+"narrow-one_16x9/auto/auto/narrow-one_16x9-cover.jpg")
    "pandemic"            = @($F+"PandemicTeaser.jpg",          $CG+"pandemic_16x9/auto/auto/pandemic_16x9-cover.jpg")
    "paper-io-2"          = @($F+"PaperIo2Teaser.jpg",          $CG+"paperio-2_16x9/auto/auto/paperio-2_16x9-cover.jpg")
    "penalty-shooters"    = @($F+"PenaltyShootersTeaser.jpg",   $CG+"penalty-shooters-2_16x9/auto/auto/penalty-shooters-2_16x9-cover.jpg")
    "pong"                = @($F+"PongTeaser.jpg",              $CG+"pong_16x9/auto/auto/pong_16x9-cover.jpg")
    "pong-2p"             = @($F+"PongTeaser.jpg",              $CG+"pong_16x9/auto/auto/pong_16x9-cover.jpg")
    "racing-limits"       = @($F+"RacingLimitsTeaser.jpg",      $CG+"racing-limits_16x9/auto/auto/racing-limits_16x9-cover.jpg")
    "red-ball-4"          = @($F+"RedBall4Teaser.jpg",          $CG+"red-ball-4_16x9/auto/auto/red-ball-4_16x9-cover.jpg")
    "road-fury"           = @($F+"RoadFuryTeaser.jpg",          $CG+"road-fury_16x9/auto/auto/road-fury_16x9-cover.jpg")
    "rooftop-snipers"     = @($F+"RooftopSnipersTeaser.jpg",    $CG+"rooftop-snipers_16x9/auto/auto/rooftop-snipers_16x9-cover.jpg")
    "run-3"               = @($F+"Run3Teaser.jpg",              $CG+"run-3_16x9/auto/auto/run-3_16x9-cover.jpg")
    "shell-shockers"      = @($F+"ShellShockersTeaser.jpg",     $CG+"shell-shockers_16x9/auto/auto/shell-shockers_16x9-cover.jpg")
    "simon-says"          = @($F+"SimonSaysTeaser.jpg",         $CG+"simon-says_16x9/auto/auto/simon-says_16x9-cover.jpg")
    "slither-io"          = @($F+"SlitherIoTeaser.jpg",         $CG+"slither-io_16x9/auto/auto/slither-io_16x9-cover.jpg")
    "slope"               = @($F+"SlopeTeaser.jpg",             $CG+"slope_16x9/auto/auto/slope_16x9-cover.jpg")
    "smash-karts"         = @($F+"SmashKartsTeaser.jpg",        $CG+"smash-karts_16x9/auto/auto/smash-karts_16x9-cover.jpg")
    "snail-bob"           = @($F+"SnailBobTeaser.jpg",          $CG+"snail-bob_16x9/auto/auto/snail-bob_16x9-cover.jpg")
    "snake"               = @($F+"SnakeTeaser.jpg",             $CG+"snake_16x9/auto/auto/snake_16x9-cover.jpg")
    "soccer-random"       = @($F+"SoccerRandomTeaser.jpg",      $CG+"soccer-random_16x9/auto/auto/soccer-random_16x9-cover.jpg")
    "solitaire"           = @($F+"SolitaireTeaser.jpg",         $CG+"solitaire_16x9/auto/auto/solitaire_16x9-cover.jpg")
    "space-is-key"        = @($F+"SpaceIsKeyTeaser.jpg",        $CG+"space-is-key_16x9/auto/auto/space-is-key_16x9-cover.jpg")
    "space-waves"         = @($F+"SpaceWavesTeaser.jpg",        $CG+"space-waves_16x9/auto/auto/space-waves_16x9-cover.jpg")
    "stickman-hook"       = @($F+"StickmanHookTeaser.jpg",      $CG+"stickman-hook_16x9/auto/auto/stickman-hook_16x9-cover.jpg")
    "stickman-soccer"     = @($F+"StickmanSoccerTeaser.jpg",    $CG+"stickman-soccer_16x9/auto/auto/stickman-soccer_16x9-cover.jpg")
    "subway-surfers"      = @($F+"SubwaySurfersTeaser.jpg",     $CG+"subway-surfers_16x9/auto/auto/subway-surfers_16x9-cover.jpg")
    "sudoku"              = @($F+"SudokuTeaser.jpg",            $CG+"sudoku_16x9/auto/auto/sudoku_16x9-cover.jpg")
    "surviv-io"           = @($F+"SurvivIoTeaser.jpg",          $CG+"surviv-io_16x9/auto/auto/surviv-io_16x9-cover.jpg")
    "temple-run-2"        = @($F+"TempleRun2Teaser.jpg",        $CG+"temple-run-2_16x9/auto/auto/temple-run-2_16x9-cover.jpg")
    "tennis-legends"      = @($F+"TennisLegendsTeaser.jpg",     $CG+"tennis-legends-2021_16x9/auto/auto/tennis-legends-2021_16x9-cover.jpg")
    "tetris"              = @($F+"TetrisTeaser.jpg",            $CG+"tetris_16x9/auto/auto/tetris_16x9-cover.jpg")
    "tic-tac-toe"         = @($F+"TicTacToeTeaser.jpg",         $CG+"tic-tac-toe_16x9/auto/auto/tic-tac-toe_16x9-cover.jpg")
    "traffic-jam-3d"      = @($F+"TrafficJam3DTeaser.jpg",      $CG+"traffic-jam-3d_16x9/auto/auto/traffic-jam-3d_16x9-cover.jpg")
    "tunnel-rush"         = @($F+"TunnelRushTeaser.jpg",        $CG+"tunnel-rush_16x9/auto/auto/tunnel-rush_16x9-cover.jpg")
    "venge-io"            = @($F+"VengeIoTeaser.jpg",           $CG+"venge-io_16x9/auto/auto/venge-io_16x9-cover.jpg")
    "vex-7"               = @($F+"Vex7Teaser.jpg",              $CG+"vex-7_16x9/auto/auto/vex-7_16x9-cover.jpg")
    "wings-io"            = @($F+"WingsIoTeaser.jpg",           $CG+"wings-io_16x9/auto/auto/wings-io_16x9-cover.jpg")
    "wordle"              = @($F+"WordleTeaser.jpg",            $CG+"wordle-unlimited_16x9/auto/auto/wordle-unlimited_16x9-cover.jpg")
    "wormate-io"          = @($F+"WormateIoTeaser.jpg",         $CG+"wormate-io_16x9/auto/auto/wormate-io_16x9-cover.jpg")
    "zombs-royale"        = @($F+"ZombsRoyaleTeaser.jpg",       $CG+"zombsroyale-io_16x9/auto/auto/zombsroyale-io_16x9-cover.jpg")
}

$ok = 0; $skip = 0; $fail = 0
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    "Referer"    = "https://www.google.com/"
    "Accept"     = "image/webp,image/apng,image/*,*/*;q=0.8"
}

foreach ($entry in $games.GetEnumerator()) {
    $slug = $entry.Key
    $urls = $entry.Value
    $fname = "$slug.jpg"

    if (Test-Path $fname) {
        Write-Host "skip $fname"
        $skip++
        continue
    }

    $saved = $false
    foreach ($url in $urls) {
        try {
            Invoke-WebRequest -Uri $url -Headers $headers -OutFile $fname -TimeoutSec 15 -ErrorAction Stop
            $size = (Get-Item $fname).Length
            if ($size -gt 1000) {
                Write-Host "OK   $fname ($size bytes)"
                $ok++
                $saved = $true
                break
            } else {
                Remove-Item $fname -Force
            }
        } catch {
            if (Test-Path $fname) { Remove-Item $fname -Force }
        }
    }

    if (-not $saved) {
        Write-Host "FAIL $fname"
        $fail++
    }
    Start-Sleep -Milliseconds 50
}

Write-Host ""
Write-Host "Done: $ok downloaded, $skip skipped, $fail failed"
if ($fail -eq 0) {
    Write-Host ""
    Write-Host "All good! Now run:"
    Write-Host "  cd C:\Users\w\CYX-browser"
    Write-Host "  git add public/icons/"
    Write-Host "  git commit -m `"Add all game thumbnails`""
    Write-Host "  git push origin main"
}
