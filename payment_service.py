import httpx
import os
import uuid
from config import MERCADOPAGO_ACCESS_TOKEN, PIX_VALOR_PADRAO

"""
Módulo de Integração com PIX (Mercado Pago / Gateway de Pagamento)
Gera cobranças dinâmicas PIX e recebe webhooks de confirmação de pagamento.
"""

async def gerar_cobranca_pix_mercadopago(valor: float = None, descricao: str = "Arte de Aniversario HD", cliente_email: str = "cliente@aniversario.com") -> dict:
    """
    Gera um pagamento PIX no Mercado Pago com código Copia e Cola e QR Code.
    Retorna o payment_id, pix_copia_e_cola e qr_code_base64.
    """
    valor_cobranca = valor or PIX_VALOR_PADRAO

    if not MERCADOPAGO_ACCESS_TOKEN or MERCADOPAGO_ACCESS_TOKEN == "seu_access_token_mercadopago":
        # Simulação para desenvolvimento / teste quando a API KEY não estiver preenchida
        fake_id = str(uuid.uuid4())[:8]
        return {
            "payment_id": f"SIM_PIX_{fake_id}",
            "status": "pending",
            "valor": valor_cobranca,
            "pix_copia_cola": f"00020126580014br.gov.bcb.pix0136simulacao-pix-{fake_id}5204000053039865404{valor_cobranca:.2f}5802BR5915AUTO_ANIVERSARIO6009SAO_PAULO62070503***63041234",
            "qr_code_base64": None,
            "simulado": True
        }

    headers = {
        "Authorization": f"Bearer {MERCADOPAGO_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": str(uuid.uuid4())
    }

    payload = {
        "transaction_amount": float(valor_cobranca),
        "description": descricao,
        "payment_method_id": "pix",
        "payer": {
            "email": cliente_email
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.mercadopago.com/v1/payments", json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()

        pix_data = data.get("point_of_interaction", {}).get("transaction_data", {})
        return {
            "payment_id": str(data.get("id")),
            "status": data.get("status"),
            "valor": valor_cobranca,
            "pix_copia_cola": pix_data.get("qr_code"),
            "qr_code_base64": pix_data.get("qr_code_base64"),
            "simulado": False
        }

async def consultar_status_pagamento(payment_id: str) -> str:
    """
    Consulta o status de um pagamento pelo ID no Mercado Pago.
    Status possíveis: 'approved', 'pending', 'rejected', 'cancelled'.
    """
    if payment_id.startswith("SIM_PIX_"):
        return "approved" # Para testes simulados

    headers = {"Authorization": f"Bearer {MERCADOPAGO_ACCESS_TOKEN}"}
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.mercadopago.com/v1/payments/{payment_id}", headers=headers)
        res.raise_for_status()
        return res.json().get("status")
