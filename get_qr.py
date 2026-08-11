import httpx
import time
import qrcode
import base64
import os

API_URL = "http://localhost:8080"
API_KEY = "minha_chave_secret_123"
INSTANCE = "aniversario_ai"

headers = {"apikey": API_KEY, "Content-Type": "application/json"}

# 1. Tentar criar a instância se não existir
try:
    httpx.post(f"{API_URL}/instance/create", json={"instanceName": INSTANCE, "qrcode": True, "integration": "WHATSAPP-BAILEYS"}, headers=headers)
except Exception:
    pass

# 2. Obter a conexão / QR Code
res = httpx.get(f"{API_URL}/instance/connect/{INSTANCE}", headers=headers).json()
print("Conectando...", res)

qr_code_str = res.get("code") or res.get("pairingCode")
base64_str = res.get("base64")

if not qr_code_str and not base64_str:
    # Reiniciar instância para força nova geração de QR Code
    httpx.get(f"{API_URL}/instance/restart/{INSTANCE}", headers=headers)
    time.sleep(3)
    res = httpx.get(f"{API_URL}/instance/connect/{INSTANCE}", headers=headers).json()
    qr_code_str = res.get("code") or res.get("pairingCode")
    base64_str = res.get("base64")

if base64_str:
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    with open("qrcode.png", "wb") as f:
        f.write(base64.b64decode(base64_str))
    print("✅ QR Code salvo em qrcode.png!")

    # Gerar HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>WhatsApp QR Code</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{ font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: #0b141a; color: white; }}
            img {{ border: 10px solid white; border-radius: 12px; max-width: 320px; }}
        </style>
    </head>
    <body>
        <h1>Escaneie com seu WhatsApp</h1>
        <img src="data:image/png;base64,{base64_str}" />
    </body>
    </html>
    """
    with open("qrcode.html", "w") as f:
        f.write(html_content)
    print("🌐 QR Code HTML salvo em qrcode.html!")

if qr_code_str:
    qr = qrcode.QRCode()
    qr.add_data(qr_code_str)
    qr.print_ascii(invert=True)
