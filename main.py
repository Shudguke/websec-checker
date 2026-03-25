from fastapi import FastAPI
import requests

app = FastAPI()

from fastapi.responses import FileResponse

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.get("/scan")
def scan(url: str):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        risk = "LOW"

        if "Content-Security-Policy" not in headers:
            risk = "HIGH"
        elif "Strict-Transport-Security" not in headers:
            risk = "MEDIUM"

        result = {
            "status_code": response.status_code,
            "https": response.url.startswith("https://"),
            "risk": risk,
            "security": {
                "CSP": "Content-Security-Policy" in headers,
                "X-Frame-Options": "X-Frame-Options" in headers,
                "HSTS": "Strict-Transport-Security" in headers,
                "X-Content-Type-Options": "X-Content-Type-Options" in headers,
                "Referrer-Policy": "Referrer-Policy" in headers
            }
        }

        return result

    except:
        return {"error": "Failed to scan"}