// Builds assets/icons.json from the simple-icons package (run in CI: npm i simple-icons@13)
const si = require("simple-icons");
const fs = require("fs");
const map = { React: "siReact", "Next.js": "siNextdotjs", TypeScript: "siTypescript", JavaScript: "siJavascript",
  Tailwind: "siTailwindcss", "Node.js": "siNodedotjs", Express: "siExpress", MongoDB: "siMongodb",
  PostgreSQL: "siPostgresql", Prisma: "siPrisma", Supabase: "siSupabase", Firebase: "siFirebase",
  "React Native": "siReact", Expo: "siExpo", Vercel: "siVercel", Figma: "siFigma", Python: "siPython",
  Git: "siGit", Vite: "siVite", MySQL: "siMysql", LinkedIn: "siLinkedin", GitHub: "siGithub" };
const out = {};
for (const [name, key] of Object.entries(map)) out[name] = { path: si[key].path, hex: si[key].hex };
fs.mkdirSync("assets", { recursive: true });
fs.writeFileSync("assets/icons.json", JSON.stringify(out));
console.log("icons:", Object.keys(out).length);
