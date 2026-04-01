// api/search.js — GET /api/search?q= (game search) | POST /api/search {query} (AI answer)
export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();

  /* ── POST: AI Answer via Groq ─────────────────────────────── */
  if (req.method === "POST") {
    try {
      const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
      const query = (body?.query || "").trim();
      if (!query) return res.status(400).json({ error: "Missing query" });

      const GROQ_KEY = process.env.GROQ_API_KEY;
      if (!GROQ_KEY) {
        return res.json({
          result: `<b>AI Search:</b> Almost ready!<br><br>To enable AI answers, add your free Groq key to Vercel:<br>
            <ol><li>Go to <a href="https://console.groq.com" target="_blank" style="color:#a78bfa">console.groq.com</a> → get a free API key</li>
            <li>Vercel Dashboard → Your Project → Settings → Environment Variables</li>
            <li>Add: <code>GROQ_API_KEY</code> = your key</li>
            <li>Redeploy</li></ol>`
        });
      }

      const groq = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${GROQ_KEY}`,
        },
        body: JSON.stringify({
          model: "llama3-8b-8192",
          max_tokens: 512,
          messages: [
            {
              role: "system",
              content: "You are Cyclone X, a helpful AI assistant built into a browser. Give concise, accurate answers. Use simple HTML: <b>, <br>, <ul><li> when helpful. No markdown, no code fences.",
            },
            { role: "user", content: query },
          ],
        }),
      });

      if (!groq.ok) {
        const errText = await groq.text();
        console.error("Groq error:", groq.status, errText);
        throw new Error(`Groq API returned ${groq.status}`);
      }

      const data = await groq.json();
      const result = data.choices?.[0]?.message?.content || "No response returned.";
      return res.json({ result });
    } catch (err) {
      console.error("AI search error:", err);
      return res.status(500).json({ error: err.message || "AI search failed" });
    }
  }

  /* ── GET: Game Search ─────────────────────────────────────── */
  const { q = "", cat = "all", limit = "20" } = req.query;
  const lim = Math.min(parseInt(limit, 10) || 20, 85);
  const base = process.env.VERCEL_URL
    ? "https://" + process.env.VERCEL_URL
    : "http://localhost:3000";
  const resp = await fetch(`${base}/api/games?q=${encodeURIComponent(q)}&cat=${cat}`);
  const data = await resp.json();
  const results = data.games.slice(0, lim);
  return res.json({ query: q, cat, count: results.length, results });
}
