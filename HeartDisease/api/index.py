import sys
from pathlib import Path

# Ensure project root is in python path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server import app as flask_app


class VercelPathFixMiddleware:
    """WSGI middleware ensuring proper path routing when Vercel rewrites to /api/index."""

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path in ("/api/index", "/api/index.py", "/api"):
            real_uri = (
                environ.get("HTTP_X_MATCHED_PATH")
                or environ.get("HTTP_X_FORWARDED_URI")
                or environ.get("REQUEST_URI")
            )
            if real_uri:
                environ["PATH_INFO"] = real_uri.split("?")[0]
        return self.wsgi_app(environ, start_response)


app = VercelPathFixMiddleware(flask_app)
