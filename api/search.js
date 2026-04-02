// api/search.js
module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method === "POST") {
    try {
      const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
      const query = (body?.query || "").trim();
      if (!query) return res.status(400).json({ error: "Missing query" });

      const GROQ_KEY = process.env.GROQ_API_KEY;
      if (!GROQ_KEY) return res.status(500).json({ error: "No GROQ_API_KEY set in Vercel environment variables." });

      const groq = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + GROQ_KEY,
        },
        body: JSON.stringify({
          model: "llama3-8b-8192",
          max_tokens: 512,
          messages: [
            { role: "system", content: "You are Cyclone X AI. Give concise helpful answers. Use simple HTML like <b>, <br>, <ul><li> when useful. No markdown." },
            { role: "user", content: query },
          ],
        }),
      });

      if (!groq.ok) {
        const t = await groq.text();
        throw new Error("Groq " + groq.status + ": " + t.slice(0, 200));
      }
      const data = await groq.json();
      return res.json({ result: data.choices?.[0]?.message?.content || "No response." });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(405).json({ error: "Method not allowed" });
};
