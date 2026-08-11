import httpx
import os
import base64
from config import WHATSAPP_TOKEN, WHATSAPP_PHONE_NUMBER_ID

API_URL = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}"

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "minha_chave_secret_123")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "aniversario_ai")

# ==============================================================================
# META WHATSAPP CLOUD API
# ==============================================================================

async def baixar_midia_whatsapp(media_id: str) -> bytes:
    """
    Baixa os bytes de uma foto/mídia enviada pelo cliente via Meta WhatsApp Cloud API.
    """
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    async with httpx.AsyncClient() as client:
        res_info = await client.get(f"https://graph.facebook.com/v19.0/{media_id}", headers=headers)
        res_info.raise_for_status()
        media_url = res_info.json().get("url")

        res_bytes = await client.get(media_url, headers=headers)
        res_bytes.raise_for_status()
        return res_bytes.content

async def enviar_mensagem_texto(telefone_destino: str, texto: str) -> dict:
    """
    Envia uma mensagem de texto simples pelo WhatsApp Cloud API.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": telefone_destino,
        "type": "text",
        "text": {"preview_url": False, "body": texto}
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{API_URL}/messages", json=payload, headers=headers)
        return res.json()

async def enviar_imagem_whatsapp(telefone_destino: str, imagem_bytes: bytes, legenda: str = "") -> dict:
    """
    Faz upload da imagem para os servidores do WhatsApp e a envia para o telefone de destino.
    """
    headers_auth = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    files = {
        "file": ("arte_aniversario.jpg", imagem_bytes, "image/jpeg"),
        "type": (None, "image/jpeg"),
        "messaging_product": (None, "whatsapp")
    }
    
    async with httpx.AsyncClient() as client:
        upload_res = await client.post(
            f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/media",
            headers=headers_auth,
            files=files
        )
        upload_res.raise_for_status()
        media_id = upload_res.json().get("id")

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": telefone_destino,
            "type": "image",
            "image": {"id": media_id, "caption": legenda}
        }
        res = await client.post(f"{API_URL}/messages", json=payload, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"})
        return res.json()


# ==============================================================================
# EVOLUTION API (CONEXÃO VIA QR CODE)
# ==============================================================================

async def enviar_mensagem_texto_evolution(telefone_destino: str, texto: str) -> dict:
    """
    Envia uma mensagem de texto simples via Evolution API.
    """
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}
    payload = {
        "number": telefone_destino,
        "options": {
            "delay": 1200,
            "presence": "composing"
        },
        "textMessage": {
            "text": texto
        }
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}", json=payload, headers=headers)
        res_json = res.json()
        print(f"📤 [ENVIO TEXTO EVOLUTION RES]: {res_json}")
        return res_json

async def enviar_imagem_evolution(telefone_destino: str, imagem_bytes: bytes, legenda: str = "") -> dict:
    """
    Envia uma imagem em Base64 via Evolution API.
    """
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}
    base64_img = base64.b64encode(imagem_bytes).decode("utf-8")
    payload = {
        "number": telefone_destino,
        "mediaMessage": {
            "mediatype": "image",
            "caption": legenda,
            "media": base64_img
        }
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        res = await client.post(f"{EVOLUTION_API_URL}/message/sendMedia/{EVOLUTION_INSTANCE}", json=payload, headers=headers)
        res_json = res.json()
        print(f"📤 [ENVIO FOTO EVOLUTION RES]: {res_json}")
        return res_json


async def baixar_midia_evolution(key_dict: dict, message_dict: dict) -> bytes:
    """
    Baixa os bytes da foto enviada via Evolution API.
    """
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}
    payload = {
        "message": {
            "key": key_dict,
            "message": message_dict
        },
        "convertToMp4": False
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Tentar findMediaMessage
        try:
            res = await client.post(f"{EVOLUTION_API_URL}/chat/findMediaMessage/{EVOLUTION_INSTANCE}", json=payload, headers=headers)
            res_data = res.json()
            base64_media = res_data.get("base64")
            if base64_media:
                if "," in base64_media:
                    base64_media = base64_media.split(",")[1]
                return base64.b64decode(base64_media)
        except Exception as e:
            print(f"⚠️ findMediaMessage aviso: {e}")

        # 2. Tentar getBase64FromMediaMessage
        try:
            res2 = await client.post(f"{EVOLUTION_API_URL}/chat/getBase64FromMediaMessage/{EVOLUTION_INSTANCE}", json=payload, headers=headers)
            res_data2 = res2.json()
            base64_media = res_data2.get("base64")
            if base64_media:
                if "," in base64_media:
                    base64_media = base64_media.split(",")[1]
                return base64.b64decode(base64_media)
        except Exception as e:
            print(f"⚠️ getBase64FromMediaMessage aviso: {e}")

        # 3. Fallback thumbnail
        img_msg = message_dict.get("imageMessage", {})
        thumb = img_msg.get("jpegThumbnail")
        if thumb:
            if "," in thumb:
                thumb = thumb.split(",")[1]
            print("📸 Usando thumbnail da foto como fallback!")
            return base64.b64decode(thumb)

        raise ValueError("Não foi possível obter base64 da foto via Evolution API.")

