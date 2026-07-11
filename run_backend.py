import os
import socket
from pathlib import Path
import uvicorn

WORKSPACE_ROOT = Path(__file__).resolve().parent
BACKEND_URL_FILE = WORKSPACE_ROOT / ".backend_url"


def find_free_port(start_port: int = 8000, end_port: int = 8100) -> int:
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No free local port found in the requested range.")


if __name__ == "__main__":
    port = int(os.getenv("PORT", find_free_port()))
    backend_url = f"http://127.0.0.1:{port}"
    os.environ["BACKEND_URL"] = backend_url
    BACKEND_URL_FILE.write_text(backend_url, encoding="utf-8")
    print(f"Starting backend on {backend_url}")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False, log_level="info")
