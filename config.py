import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "meu_token_de_verificacao_secreto_123")

# Configurações de Pagamento PIX (Mercado Pago / Gateway)
MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")
PIX_VALOR_PADRAO = float(os.getenv("PIX_VALOR_PADRAO", "9.90")) # Valor da arte em Reais (R$)

PORT = int(os.getenv("PORT", "8005"))
HOST = os.getenv("HOST", "0.0.0.0")

# Validação básica
if not GEMINI_API_KEY or GEMINI_API_KEY == "sua_chave_gemini_api_aqui":
    print("⚠️  [AVISO] GEMINI_API_KEY não configurada no arquivo .env!")
