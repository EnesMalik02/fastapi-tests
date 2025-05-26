# main.py
from fastapi import FastAPI, HTTPException, Response, Request
from datetime import datetime
import qrcode
import io
import os

app = FastAPI()

# QR kod görsellerinin saklanacağı klasör
QR_DIR = "qr_codes"
os.makedirs(QR_DIR, exist_ok=True)

def generate_timestamp_qr(base_url: str, dt: datetime) -> bytes:
    """
    base_url/scan?timestamp=...&name=Enes URL'sini QR'a encode eder.
    """
    ts = dt.isoformat()
    url = f"{base_url}/scan?timestamp={ts}&name=Enes"

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

@app.get(
    "/qr",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}}
)
async def get_qr(request: Request):
    """
    GET /qr
    - Şu anki zamanı alır
    - request.base_url ile gerçek host+port bilgisi edinir
    - Bununla bir URL oluşturur: {base_url}/scan?timestamp=...&name=Enes
    - URL'i encode eden QR PNG'sini kaydeder ve döner
    """
    now = datetime.utcnow()
    base_url = str(request.base_url).rstrip("/")  # örn: "http://192.168.1.42:8000"
    img_bytes = generate_timestamp_qr(base_url, now)

    # İsterseniz PNG'i dosyaya kaydedin
    filename = now.strftime("%Y%m%d_%H%M%S") + ".png"
    path = os.path.join(QR_DIR, filename)
    with open(path, "wb") as f:
        f.write(img_bytes)

    return Response(content=img_bytes, media_type="image/png")

@app.get("/scan")
async def scan_via_qr(timestamp: str, name: str):
    """
    QR okutulduğunda tarayıcı şu URL'i açar:
      GET /scan?timestamp=...&name=Enes
    Bu handler:
    - timestamp'ı ISO formatta parse eder
    - iş mantığını çalıştırır (örneğin DB güncelleme)
    - JSON yanıt döner
    """
    try:
        dt = datetime.fromisoformat(timestamp)
    except ValueError:
        raise HTTPException(status_code=400, detail="Geçersiz timestamp formatı")

    return {
        "status":    "ok",
        "timestamp": timestamp,
        "name":      name
    }
