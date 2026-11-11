"""Local upload page and setup check for the agent team. Runs on this computer only."""
import argparse
import csv
import datetime as dt
import io
import json
import re
import shutil
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
MAX_BYTES = 25 * 1024 * 1024
BRAIN_DOCS = ["customers.md", "offer-and-proof.md", "voice.md", "competitors.md", "wins-and-flops.md", "research.md"]
DEMO_MARKERS = ["fictional", "Fenwick Row", "Summit Trail", "Rearview Mirror"]
DEMO_FILE_MARKERS = ("fictional: true", "Fictional competitor.", "Fictional demo.")

SLOTS = {
    "brain": {"label": "Brain docs", "used_by": "All 8 agents", "folder": "brain", "mode": "named", "ext": [".md"],
              "hint": "Use the exact names: " + ", ".join(BRAIN_DOCS)},
    "calls": {"label": "Sales call transcripts", "used_by": "Agent 1", "folder": "data/calls", "mode": "add",
              "ext": [".md", ".txt", ".vtt"], "hint": "One file per call. Start the name with the date, like 2026-11-05_acme.txt"},
    "emails": {"label": "Support emails", "used_by": "Agent 1", "folder": "data/support-emails", "mode": "replace",
               "file": "support_emails.csv", "ext": [".csv"],
               "columns": ["date", "from_name", "company", "label", "subject", "body"], "hint": "CSV with the columns listed"},
    "competitors": {"label": "Competitor pages", "used_by": "Agent 2", "folder": "data/competitors", "mode": "dated",
                    "ext": [".md", ".txt"], "hint": "One text file per competitor. Saved under today's date, so keep names the same each week"},
    "ai": {"label": "Claude category answers", "used_by": "Agent 2", "folder": "data/ai-visibility", "mode": "add",
           "ext": [".md", ".txt"], "hint": "Saved answers to your category prompt"},
    "ads": {"label": "Ad results", "used_by": "Agent 8", "folder": "data/ads", "mode": "replace", "file": "ads_daily.csv",
            "ext": [".csv"], "columns": ["date", "platform", "ad_id", "headline", "impressions", "clicks", "spend_usd", "signups"],
            "hint": "One row per ad per day. Rename the columns to match first"},
    "visitors": {"label": "Website visitor alerts", "used_by": "Agent 7", "folder": "data/visitors", "mode": "replace",
                 "file": "leadfeeder_alerts.csv", "ext": [".csv"],
                 "columns": ["alert_date", "company", "industry", "pricing_page_visits", "time_on_pricing_seconds"],
                 "hint": "CSV with the columns listed. Extra columns are fine"},
    "contacts": {"label": "Contacts", "used_by": "Agent 7", "folder": "data/visitors", "mode": "replace",
                 "file": "contacts.csv", "ext": [".csv"], "columns": ["company", "name", "title"],
                 "hint": "CSV with the columns listed"},
}


def decode(raw):
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


def safe_name(name):
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(name.replace("\\", "/")).name).strip("-.")
    return name


def validate_csv(slot, text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        return "The file has no data rows."
    missing = [c for c in slot["columns"] if c not in rows[0]]
    if missing:
        return "Missing columns: " + ", ".join(missing)
    if "spend_usd" in slot["columns"]:
        for i, row in enumerate(rows, 2):
            try:
                dt.date.fromisoformat(row["date"])
                float(row["spend_usd"])
                int(row["impressions"]), int(row["clicks"]), int(row["signups"])
            except (TypeError, ValueError):
                return f"Row {i} has a bad value. Dates must look like 2026-11-05, and the numbers must be plain numbers."
    return None


def unique_path(path):
    if not path.exists():
        return path
    n = 2
    while (candidate := path.with_name(f"{path.stem}-{n}{path.suffix}")).exists():
        n += 1
    return candidate


def clear_demo_files(root, key, folder):
    """Move demo files out of an add-only area, so agents never read them alongside real ones."""
    if not folder.exists():
        return
    for path in [p for p in folder.rglob("*") if p.is_file()]:
        if any(m in path.read_text(encoding="utf-8", errors="replace") for m in DEMO_FILE_MARKERS):
            keep = unique_path(root / "data" / "_replaced" / key / "demo" / path.relative_to(folder))
            keep.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(keep))


def save_upload(root, key, name, raw, today=None):
    slot = SLOTS.get(key)
    if not slot:
        return 400, "Unknown upload type."
    if not raw:
        return 400, "The file is empty."
    if len(raw) > MAX_BYTES:
        return 413, "The file is over 25 MB."
    name = safe_name(name)
    if not name or Path(name).suffix.lower() not in slot["ext"]:
        return 400, "Accepted file types: " + ", ".join(slot["ext"])
    text = decode(raw)
    if "columns" in slot:
        problem = validate_csv(slot, text)
        if problem:
            return 400, problem
    mode, folder = slot["mode"], root / slot["folder"]
    if mode == "named" and name not in BRAIN_DOCS:
        return 400, "Use one of the six Brain doc names: " + ", ".join(BRAIN_DOCS)
    if mode in ("add", "dated"):
        clear_demo_files(root, key, folder)
    if mode == "dated":
        folder = folder / (today or dt.date.today().isoformat())
    folder.mkdir(parents=True, exist_ok=True)
    if mode in ("replace", "named"):
        target = folder / slot.get("file", name)
        if target.exists():
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            keep = unique_path(root / "data" / "_replaced" / key / f"{stamp}_{target.name}")
            keep.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, keep)
    else:
        target = unique_path(folder / name)
    target.write_text(text, encoding="utf-8")
    return 200, f"Saved as {target.relative_to(root).as_posix()}"


def status(root):
    result = []
    for key, slot in SLOTS.items():
        folder = root / slot["folder"]
        if "file" in slot:
            files = [folder / slot["file"]] if (folder / slot["file"]).exists() else []
        elif folder.exists():
            files = [p for p in folder.rglob("*") if p.is_file()]
        else:
            files = []
        if key == "brain":
            missing = [d for d in BRAIN_DOCS if not (folder / d).exists()]
        else:
            missing = []
        text = " ".join(p.read_text(encoding="utf-8", errors="replace") for p in files)
        rows = None
        if "columns" in slot and files:
            rows = len(list(csv.DictReader(io.StringIO(text))))
        latest = max((p.stat().st_mtime for p in files), default=None)
        if not files or missing:
            state = "missing"
        elif any(m.lower() in text.lower() for m in DEMO_MARKERS):
            state = "demo"
        else:
            state = "yours"
        result.append({
            "key": key, "label": slot["label"], "used_by": slot["used_by"], "hint": slot["hint"],
            "columns": slot.get("columns", []), "ext": slot["ext"], "state": state, "files": len(files), "rows": rows,
            "missing": missing, "updated": dt.datetime.fromtimestamp(latest).strftime("%Y-%m-%d %H:%M") if latest else None,
        })
    agents = sorted(p.name for p in (root / "agents").glob("*.md")) if (root / "agents").exists() else []
    return {"slots": result, "agents": len(agents)}


def make_handler(root):
    class Handler(BaseHTTPRequestHandler):
        def send(self, code, body, kind="application/json"):
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", f"{kind}; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def host_ok(self):
            return self.headers.get("Host", "").split(":")[0] in ("127.0.0.1", "localhost")

        def do_GET(self):
            if not self.host_ok():
                return self.send(403, json.dumps({"message": "Forbidden"}))
            path = urlparse(self.path).path
            if path == "/":
                return self.send(200, (HERE / "upload.html").read_text(encoding="utf-8"), "text/html")
            if path == "/status":
                return self.send(200, json.dumps(status(root)))
            return self.send(404, json.dumps({"message": "Not found"}))

        def do_POST(self):
            # The custom header blocks uploads triggered by other websites.
            if not self.host_ok() or self.headers.get("X-Agent-Upload") != "1":
                return self.send(403, json.dumps({"message": "Forbidden"}))
            url = urlparse(self.path)
            if url.path != "/upload":
                return self.send(404, json.dumps({"message": "Not found"}))
            size = int(self.headers.get("Content-Length") or 0)
            if size > MAX_BYTES:
                self.close_connection = True
                return self.send(413, json.dumps({"message": "The file is over 25 MB."}))
            query = parse_qs(url.query)
            code, message = save_upload(root, query.get("type", [""])[0], query.get("name", [""])[0], self.rfile.read(size))
            return self.send(code, json.dumps({"message": message}))

        def log_message(self, *args):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=HERE.parent)
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--check", action="store_true", help="print the setup status and exit")
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.check:
        report = status(root)
        for slot in report["slots"]:
            extra = f", missing: {', '.join(slot['missing'])}" if slot["missing"] else ""
            print(f"{slot['state']:8} {slot['label']} ({slot['files']} files{extra})")
        print(f"agents   {report['agents']} of 8 instruction files")
        return
    url = f"http://127.0.0.1:{args.port}/"
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(root))
    print(f"Upload page: {url}  Press Ctrl+C to stop.")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
