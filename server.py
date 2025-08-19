#!/usr/bin/env python3
# minimal file share server (Python 3.9+)
import os, json, mimetypes, re
from pathlib import Path
from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify

BASE = Path(__file__).resolve().parent
PUBLIC = BASE / "public"
UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)

app = Flask(__name__)

SAFE_CHARS = re.compile(r"[^A-Za-z0-9._ ()-]")

def safe_name(name: str) -> str:
    # strip path bits and sanitize
    name = os.path.basename(name)
    return SAFE_CHARS.sub("", name)

def split_name_ext(filename: str):
    i = filename.rfind(".")
    return (filename, "") if i <= 0 else (filename[:i], filename[i:])

def human_size(n: int) -> str:
    if n < 1024: return f"{n} B"
    for unit in ["KB", "MB", "GB", "TB"]:
        n /= 1024.0
        if n < 1024.0:
            return f"{n:.1f} {unit}"
    return f"{n:.1f} PB"

# --------- Static pages ----------
@app.get("/")
def root():
    return send_from_directory(PUBLIC, "index.html")

@app.get("/downloads.html")
def downloads_page():
    return send_from_directory(PUBLIC, "downloads.html")

@app.get("/public/<path:path>")
def static_files(path):
    return send_from_directory(PUBLIC, path)

# --------- APIs ----------
@app.post("/api/upload")
def api_upload():
    files = request.files.getlist("files")
    saved = 0
    for f in files:
        if not f or not f.filename:
            continue
        original = safe_name(f.filename)
        if not original:
            continue
        name, ext = split_name_ext(original)
        candidate = original
        i = 1
        while (UPLOADS / candidate).exists():
            candidate = f"{name} ({i}){ext}"
            i += 1
        f.save(UPLOADS / candidate)
        saved += 1
    return jsonify(ok=True, saved=saved)

@app.get("/api/files")
def api_files():
    entries = []
    for p in sorted(UPLOADS.iterdir(), key=lambda q: q.stat().st_mtime, reverse=True):
        if p.is_file():
            st = p.stat()
            entries.append({
                "name": p.name,
                "size": st.st_size,
                "size_h": human_size(st.st_size),
                "mtime": int(st.st_mtime),
                "mtime_h": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
            })
    return jsonify(ok=True, files=entries)

@app.get("/d/<path:name>")
def download(name):
    safe = safe_name(name)
    path = UPLOADS / safe
    if not path.exists() or not path.is_file():
        return ("Not found", 404)
    ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return send_from_directory(UPLOADS, safe, as_attachment=True, mimetype=ctype)

if __name__ == "__main__":
    # pip install flask
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    print(f"Serving on http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
