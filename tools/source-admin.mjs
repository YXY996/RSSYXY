import http from "node:http";
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";

const execFileAsync = promisify(execFile);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalogPath = path.join(root, "config", "sources.json");
const pagePath = path.join(root, "tools", "source-admin.html");
const csrf = crypto.randomBytes(24).toString("hex");
const port = 8765;
const safeId = /^[a-z0-9][a-z0-9._-]{1,63}$/;

function send(res, status, value, contentType = "application/json; charset=utf-8") {
  const body = typeof value === "string" ? value : JSON.stringify(value);
  res.writeHead(status, { "content-type": contentType, "cache-control": "no-store", "x-content-type-options": "nosniff" });
  res.end(body);
}

function trusted(req) {
  const host = req.headers.host || "";
  const origin = req.headers.origin || "";
  return /^(127\.0\.0\.1|localhost):8765$/.test(host) && (!origin || /^(http:\/\/127\.0\.0\.1:8765|http:\/\/localhost:8765)$/.test(origin));
}

async function bodyJson(req) {
  let raw = "";
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 262144) throw new Error("请求内容过大");
  }
  return JSON.parse(raw || "{}");
}

function validate(catalog) {
  for (const section of ["platforms", "rss"]) {
    if (!Array.isArray(catalog?.[section])) throw new Error(`${section} 必须是列表`);
    const seen = new Set();
    for (const item of catalog[section]) {
      if (!safeId.test(item.id || "") || seen.has(item.id)) throw new Error(`ID 无效或重复：${item.id || "(空)"}`);
      seen.add(item.id);
      if (!String(item.name || "").trim()) throw new Error(`${item.id} 缺少名称`);
      if (section === "rss") {
        const parsed = new URL(item.url || "about:blank");
        if (parsed.protocol !== "https:") throw new Error(`${item.id} 的 RSS 地址必须使用 HTTPS`);
      }
    }
  }
}

async function saveCatalog(catalog) {
  validate(catalog);
  const temp = `${catalogPath}.tmp`;
  await fs.writeFile(temp, `${JSON.stringify(catalog, null, 2)}\n`, "utf8");
  await fs.rename(temp, catalogPath);
}

async function syncGitHub() {
  await execFileAsync("git", ["add", "config/sources.json"], { cwd: root, windowsHide: true });
  try {
    await execFileAsync("git", ["diff", "--cached", "--quiet"], { cwd: root, windowsHide: true });
    return "没有需要同步的消息源改动";
  } catch (error) {
    if (error.code !== 1) throw error;
  }
  await execFileAsync("git", ["commit", "-m", "chore-update-news-sources"], { cwd: root, windowsHide: true });
  const { stdout, stderr } = await execFileAsync("git", ["push", "origin", "main"], { cwd: root, windowsHide: true });
  return (stdout || stderr || "已同步到 GitHub").trim();
}

const server = http.createServer(async (req, res) => {
  try {
    if (!trusted(req)) return send(res, 403, { error: "只允许从本机后台访问" });
    if (req.method === "GET" && req.url === "/") {
      const page = (await fs.readFile(pagePath, "utf8")).replaceAll("__CSRF_TOKEN__", csrf);
      return send(res, 200, page, "text/html; charset=utf-8");
    }
    if (req.method === "GET" && req.url === "/api/sources") {
      return send(res, 200, JSON.parse(await fs.readFile(catalogPath, "utf8")));
    }
    if (req.method === "POST" && req.headers["x-source-admin-token"] !== csrf) return send(res, 403, { error: "页面会话已失效，请刷新" });
    if (req.method === "POST" && req.url === "/api/sources") {
      await saveCatalog(await bodyJson(req));
      return send(res, 200, { message: "已保存到本机，尚未同步 GitHub" });
    }
    if (req.method === "POST" && req.url === "/api/sync") {
      const catalog = await bodyJson(req);
      await saveCatalog(catalog);
      return send(res, 200, { message: await syncGitHub() });
    }
    return send(res, 404, { error: "未找到页面" });
  } catch (error) {
    return send(res, 400, { error: error.message || String(error) });
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`消息源后台已启动：http://127.0.0.1:${port}/`);
  import("node:child_process").then(({ spawn }) => spawn("cmd", ["/c", "start", "", `http://127.0.0.1:${port}/`], { detached: true, windowsHide: true }));
});
