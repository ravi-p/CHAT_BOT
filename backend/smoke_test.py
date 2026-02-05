import requests
import time
import os

base = "http://127.0.0.1:8000"

# wait for server to be ready
for i in range(30):
    try:
        r = requests.get(base + "/docs", timeout=1)
        if r.status_code < 500:
            break
    except Exception:
        time.sleep(0.5)
else:
    print("Server did not become ready")
    raise SystemExit(1)

# create a small test file
fn = os.path.join(os.path.dirname(__file__), "test_upload.txt")
with open(fn, "w", encoding="utf-8") as f:
    f.write("This short document explains that apples are fruits and oranges are citrus fruits.\nIt mentions nutrition and examples.")

# upload
with open(fn, "rb") as fh:
    files = {"file": ("test_upload.txt", fh, "text/plain")}
    r = requests.post(base + "/upload", files=files, timeout=30)
    print("UPLOAD ->", r.status_code, r.text)

# chat
r2 = requests.post(base + "/chat", data={"query": "What is this document about?"}, timeout=30)
print("CHAT ->", r2.status_code, r2.text)
