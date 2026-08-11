from fastapi import FastAPI, Request, Response, BackgroundTasks, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response as RawResponse
import uvicorn
import os

from config import WEBHOOK_VERIFY_TOKEN, PORT, HOST
from prompts import MESSAGE_WELCOME, get_message_oferta_pacotes, get_message_pagamento_aprovado
from gemini_service import gerar_pacote_artes_async
from watermark_service import aplicar_marca_dagua_previa
from whatsapp_service import (
    baixar_midia_whatsapp, enviar_mensagem_texto, enviar_imagem_whatsapp,
    enviar_mensagem_texto_evolution, enviar_imagem_evolution, baixar_midia_evolution
)
from payment_service import gerar_cobranca_pix_mercadopago, consultar_status_pagamento

app = FastAPI(
    title="Auto-Aniversário AI — Meta & Evolution API",
    description="Sistema automatizado com pacotes promocionais diretos via PIX.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARTES_PENDENTES = {}

@app.get("/health")
def health_check():
    return {"status": "online", "sistema": "Auto-Aniversário AI", "versao": "2.0.0"}

# ==============================================================================
# FLUXO META CLOUD API
# ==============================================================================

@app.get("/webhook")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Token de verificação inválido.")

async def processar_fluxo_foto_e_pacotes(telefone_cliente: str, image_id: str):
    try:
        await enviar_mensagem_texto(telefone_cliente, MESSAGE_WELCOME)
        imagem_original_bytes = await baixar_midia_whatsapp(image_id)

        print(f"[GEMINI AI] Gerando variaçoes de foto para {telefone_cliente}...")
        pacote_artes_dict = await gerar_pacote_artes_async(imagem_original_bytes, qtd=3)

        arte_principal_hd = pacote_artes_dict["estilo_1"]
        previa_bytes = aplicar_marca_dagua_previa(arte_principal_hd)

        pix_999 = await gerar_cobranca_pix_mercadopago(valor=9.99, descricao="1 Foto HD", cliente_email=f"n1_{telefone_cliente}@cliente.com")
        pix_1499 = await gerar_cobranca_pix_mercadopago(valor=14.99, descricao="Combo 2 Fotos HD", cliente_email=f"n2_{telefone_cliente}@cliente.com")
        pix_1999 = await gerar_cobranca_pix_mercadopago(valor=19.99, descricao="Pacote VIP 3 Fotos HD", cliente_email=f"n3_{telefone_cliente}@cliente.com")

        ARTES_PENDENTES[pix_999["payment_id"]] = {"telefone": telefone_cliente, "artes": {"estilo_1": pacote_artes_dict["estilo_1"]}, "qtd": 1, "origem": "meta"}
        ARTES_PENDENTES[pix_1499["payment_id"]] = {"telefone": telefone_cliente, "artes": {"estilo_1": pacote_artes_dict["estilo_1"], "estilo_2": pacote_artes_dict["estilo_2"]}, "qtd": 2, "origem": "meta"}
        ARTES_PENDENTES[pix_1999["payment_id"]] = {"telefone": telefone_cliente, "artes": pacote_artes_dict, "qtd": 3, "origem": "meta"}

        print(f"[WHATSAPP META] Enviando previa protegida para {telefone_cliente}...")
        await enviar_imagem_whatsapp(telefone_cliente, previa_bytes, legenda="PREVIA DA SUA FOTO DE ANIVERSARIO")

        msg_oferta = get_message_oferta_pacotes(
            pix_copia_cola_999=pix_999["pix_copia_cola"],
            pix_copia_cola_1499=pix_1499["pix_copia_cola"],
            pix_copia_cola_1999=pix_1999["pix_copia_cola"]
        )
        await enviar_mensagem_texto(telefone_cliente, msg_oferta)

    except Exception as e:
        print(f"[ERRO FLUXO META] {e}")

@app.post("/webhook")
async def receber_webhook(request: Request, background_tasks: BackgroundTasks):
    payload_body = await request.json()
    print(f"[WEBHOOK META RECEBIDO]: {payload_body}")
    try:
        entry = payload_body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if messages:
            msg = messages[0]
            telefone = msg.get("from")
            type_msg = msg.get("type")

            if type_msg == "image":
                image_id = msg.get("image", {}).get("id")
                background_tasks.add_task(processar_fluxo_foto_e_pacotes, telefone, image_id)
            elif type_msg == "text":
                background_tasks.add_task(
                    enviar_mensagem_texto, 
                    telefone, 
                    "*Ola! Sou o assistente do Auto-Aniversario AI!*\n\nEnvie uma **foto de perfil ou rosto** para que nossa Inteligencia Artificial gere suas artes festivas de aniversario!"
                )
    except Exception as e:
        print(f"Evento Meta ignorado: {e}")

    return {"status": "recebido"}


# ==============================================================================
# FLUXO EVOLUTION API (QR CODE)
# ==============================================================================

async def processar_fluxo_foto_evolution(telefone_cliente: str, key_dict: dict, message_dict: dict):
    try:
        await enviar_mensagem_texto_evolution(telefone_cliente, MESSAGE_WELCOME)
        imagem_original_bytes = await baixar_midia_evolution(key_dict, message_dict)

        print(f"[GEMINI AI - EVOLUTION] Gerando variaçoes para {telefone_cliente}...")
        pacote_artes_dict = await gerar_pacote_artes_async(imagem_original_bytes, qtd=3)

        arte_principal_hd = pacote_artes_dict["estilo_1"]
        previa_bytes = aplicar_marca_dagua_previa(arte_principal_hd)

        pix_999 = await gerar_cobranca_pix_mercadopago(valor=9.99, descricao="1 Foto HD", cliente_email=f"n1_{telefone_cliente}@cliente.com")
        pix_1499 = await gerar_cobranca_pix_mercadopago(valor=14.99, descricao="Combo 2 Fotos HD", cliente_email=f"n2_{telefone_cliente}@cliente.com")
        pix_1999 = await gerar_cobranca_pix_mercadopago(valor=19.99, descricao="Pacote VIP 3 Fotos HD", cliente_email=f"n3_{telefone_cliente}@cliente.com")

        ARTES_PENDENTES[pix_999["payment_id"]] = {"telefone": telefone_cliente, "artes": {"estilo_1": pacote_artes_dict["estilo_1"]}, "qtd": 1, "origem": "evolution"}
        ARTES_PENDENTES[pix_1499["payment_id"]] = {"telefone": telefone_cliente, "artes": {"estilo_1": pacote_artes_dict["estilo_1"], "estilo_2": pacote_artes_dict["estilo_2"]}, "qtd": 2, "origem": "evolution"}
        ARTES_PENDENTES[pix_1999["payment_id"]] = {"telefone": telefone_cliente, "artes": pacote_artes_dict, "qtd": 3, "origem": "evolution"}

        print(f"[WHATSAPP EVOLUTION] Enviando previa para {telefone_cliente}...")
        await enviar_imagem_evolution(telefone_cliente, previa_bytes, legenda="PREVIA DA SUA FOTO DE ANIVERSARIO")

        msg_oferta = get_message_oferta_pacotes(
            pix_copia_cola_999=pix_999["pix_copia_cola"],
            pix_copia_cola_1499=pix_1499["pix_copia_cola"],
            pix_copia_cola_1999=pix_1999["pix_copia_cola"]
        )
        await enviar_mensagem_texto_evolution(telefone_cliente, msg_oferta)

    except Exception as e:
        print(f"[ERRO FLUXO EVOLUTION] {e}")

async def processar_chat_texto_evolution(telefone_cliente: str, texto_recebido: str):
    from gemini_service import responder_chat_cliente_async
    resposta_ia = await responder_chat_cliente_async(texto_recebido)
    await enviar_mensagem_texto_evolution(telefone_cliente, resposta_ia)

@app.post("/webhook/evolution")
async def webhook_evolution(request: Request, background_tasks: BackgroundTasks):
    payload_body = await request.json()
    print(f"[EVOLUTION RECEBIDO]: {payload_body}")

    try:
        event = payload_body.get("event")
        data = payload_body.get("data", {})

        if event in ["messages.upsert", "MESSAGES_UPSERT"]:
            key = data.get("key", {})
            from_me = key.get("fromMe", False)
            if from_me:
                return {"status": "mensagem_propria_ignorada"}

            remote_jid = key.get("senderPn") or key.get("remoteJid", "")
            telefone_cliente = remote_jid.split("@")[0]

            message = data.get("message", {})
            message_type = data.get("messageType") or list(message.keys())[0] if message else ""

            if message_type == "imageMessage" or "imageMessage" in message:
                background_tasks.add_task(processar_fluxo_foto_evolution, telefone_cliente, key, message)
            elif message_type in ["conversation", "extendedTextMessage"] or "conversation" in message or "extendedTextMessage" in message:
                texto_msg = message.get("conversation") or message.get("extendedTextMessage", {}).get("text", "")
                background_tasks.add_task(processar_chat_texto_evolution, telefone_cliente, texto_msg)
    except Exception as e:
        print(f"Evento Evolution ignorado: {e}")

    return {"status": "ok"}


# ==============================================================================
# PAGAMENTOS PIX
# ==============================================================================

async def entregar_artes_hd(telefone: str, artes_dict: dict, qtd: int, origem: str = "meta"):
    msg_confirmacao = get_message_pagamento_aprovado(qtd)
    if origem == "evolution":
        await enviar_mensagem_texto_evolution(telefone, msg_confirmacao)
        idx = 1
        for estilo, img_hd_bytes in artes_dict.items():
            legenda = f"Sua Foto HD #{idx} (Sem Marca d'Agua)"
            await enviar_imagem_evolution(telefone, img_hd_bytes, legenda=legenda)
            idx += 1
    else:
        await enviar_mensagem_texto(telefone, msg_confirmacao)
        idx = 1
        for estilo, img_hd_bytes in artes_dict.items():
            legenda = f"Sua Foto HD #{idx} (Sem Marca d'Agua)"
            await enviar_imagem_whatsapp(telefone, img_hd_bytes, legenda=legenda)
            idx += 1

@app.post("/webhook/payment")
async def webhook_pagamento_pix(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    payment_id = str(data.get("data", {}).get("id") or data.get("id", ""))
    
    if payment_id in ARTES_PENDENTES:
        status = await consultar_status_pagamento(payment_id)
        if status == "approved":
            item = ARTES_PENDENTES.pop(payment_id)
            telefone = item["telefone"]
            artes_dict = item["artes"]
            qtd = item["qtd"]
            origem = item.get("origem", "meta")

            print(f"[PAGAMENTO PIX APROVADO] Entregando pacote de {qtd} foto(s) HD para {telefone}!")
            background_tasks.add_task(entregar_artes_hd, telefone, artes_dict, qtd, origem)

    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
