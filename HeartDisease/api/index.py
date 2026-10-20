import sys
from pathlib import Path

# Ensure project root is in python path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from urllib.parse import parse_qs, urlencode

from server import app as flask_app


class VercelPathFixMiddleware:
    """WSGI middleware ensuring proper path routing when Vercel rewrites to /api/index."""

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = environ.get("QUERY_STRING", "")
        if "__route" in qs:
            params = parse_qs(qs, keep_blank_values=True)
            route_parts = params.pop("__route", [""])
            subroute = route_parts[0].lstrip("/")

            # Reconstruct the target API path
            if subroute:
                environ["PATH_INFO"] = f"/api/{subroute}"
            else:
                environ["PATH_INFO"] = "/api/health"

            # Rebuild clean query string without __route
            environ["QUERY_STRING"] = urlencode(params, doseq=True)
        else:
            path = environ.get("PATH_INFO", "")
            if path in ("/api/index", "/api/index.py", "/api"):
                for header in ("HTTP_X_FORWARDED_URI", "HTTP_X_ORIGINAL_URL", "REQUEST_URI"):
                    val = environ.get(header)
                    if val:
                        cleaned = val.split("?")[0]
                        if cleaned not in ("/api/index", "/api/index.py", "/api"):
                            environ["PATH_INFO"] = cleaned
                            break

        return self.wsgi_app(environ, start_response)


app = VercelPathFixMiddleware(flask_app)

