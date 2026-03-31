// API/search.js — GET /api/search?q=slope
// Lightweight game search for external integrations.

export default async function handler(req, res) {
  const { q = "", cat = "all", limit = "20" } = req.query;
  const lim = Math.min(parseInt(limit, 10) || 20, 85);

  const resp = await fetch(`${process.env.VERCEL_URL
    ? "https://" + process.env.VERCEL_URL
    : "http://localhost:3000"}/api/games?q=${encodeURIComponent(q)}&cat=${cat}`);
  const data = await resp.json();
  const results = data.games.slice(0, lim);

  res.setHeader("Access-Control-Allow-Origin", "*");
  res.json({ query: q, cat, count: results.length, results });
}
