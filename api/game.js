// API/game.js — GET /api/game/:id
// Returns a single game by numeric ID.

import gamesHandler from "./games.js";

// Re-use the same GAMES array (import trick for Vercel)
module.exports = function handler(req, res) {
  const id = parseInt(req.query.id, 10);
  if (!id || isNaN(id)) {
    return res.status(400).json({ error: "Missing or invalid id" });
  }

  // Pull the games list inline (copy) to avoid circular imports on Vercel
  // In production, extract GAMES to a shared games-data.js module
  const { games } = require("./_games-data");
  const game = games.find(g => g.id === id);
  if (!game) return res.status(404).json({ error: "Game not found" });

  res.setHeader("Access-Control-Allow-Origin", "*");
  res.json(game);
}
