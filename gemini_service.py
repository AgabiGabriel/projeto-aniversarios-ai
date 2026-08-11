import os
import io
import time
import asyncio
from PIL import Image
from google import genai
from config import GEMINI_API_KEY
from prompts import PROMPTS_ESTILOS

def processar_foto_aniversario(imagem_input_bytes: bytes, estilo_chave: str = "estilo_1") -> bytes:
    """
    Recebe os bytes da foto enviada pelo cliente e o estilo realista desejado,
    chama a API do Gemini e retorna os bytes da imagem gerada.
    """
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key or api_key == "sua_chave_gemini_api_aqui":
        raise ValueError("GEMINI_API_KEY não está configurada no arquivo .env!")

    prompt = PROMPTS_ESTILOS.get(estilo_chave, PROMPTS_ESTILOS["estilo_1"])
    image_pil = Image.open(io.BytesIO(imagem_input_bytes))

    try:
        client = genai.Client(api_key=api_key)

        models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']
        for mod in models_to_try:
            for tentativa in range(2):
                try:
                    print(f"[GEMINI TENTATIVA {tentativa+1}] Modelo {mod} - Estilo: {estilo_chave}...")
                    response = client.models.generate_content(
                        model=mod,
                        contents=[image_pil, prompt]
                    )
                    if hasattr(response, 'images') and response.images:
                        img_out = response.images[0]
                        output_buffer = io.BytesIO()
                        img_out.save(output_buffer, format="JPEG")
                        print(f"[GEMINI SUCESSO] Imagem gerada com modelo {mod}!")
                        return output_buffer.getvalue()
                    elif hasattr(response, 'text') and response.text:
                        print(f"[GEMINI AVISO] ({mod}) retornou texto: {response.text[:120]}")
                        break
                except Exception as e_mod:
                    print(f"[GEMINI ALERTA] Modelo {mod} tentativa {tentativa+1} falhou: {e_mod}")
                    time.sleep(1.5)
    except Exception as e_gen:
        print(f"[GEMINI ERRO CRITICO]: {e_gen}")

    print("Retornando imagem original como fallback.")
    output_buffer = io.BytesIO()
    image_pil.save(output_buffer, format="JPEG")
    return output_buffer.getvalue()


async def processar_foto_aniversario_async(imagem_input_bytes: bytes, estilo_chave: str = "estilo_1") -> bytes:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, processar_foto_aniversario, imagem_input_bytes, estilo_chave
    )

async def gerar_pacote_artes_async(imagem_input_bytes: bytes, qtd: int = 1) -> dict:
    """
    Gera 1, 2 ou 3 variações de fotos para o pacote escolhido.
    Estilos: 'estilo_1', 'estilo_2', 'estilo_3'.
    """
    estilos = ["estilo_1", "estilo_2", "estilo_3"][:qtd]
    resultados = {}
    
    tasks = [processar_foto_aniversario_async(imagem_input_bytes, estilo) for estilo in estilos]
    artes = await asyncio.gather(*tasks)
    
    for estilo, arte_bytes in zip(estilos, artes):
        resultados[estilo] = arte_bytes
        
    return resultados

async def responder_chat_cliente_async(mensagem_cliente: str) -> str:
    """
    Usa o Gemini 2.5 Flash para responder dúvidas dos clientes no WhatsApp sobre o serviço de Fotos de Aniversário AI.
    """
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key:
        return "Ola! Sou o assistente do Auto-Aniversario AI! Envie uma foto de rosto para comecarmos!"

    prompt_sistema = f"""
    Você é o assistente virtual simpático e atencioso do "Auto-Aniversário AI".
    Seu objetivo é orientar o cliente e incentivá-lo a enviar uma FOTO DE PERFIL / ROSTO para que nossa Inteligência Artificial gere fotos incríveis de aniversário.
    Valores dos pacotes:
    - 1 Foto HD: R$ 9,99
    - Combo 2 Fotos HD: R$ 14,99
    - Pacote VIP 3 Fotos HD: R$ 19,99
    Responda em português brasileiro de forma direta e sem utilizar emojis.
    
    Mensagem do cliente: "{mensagem_cliente}"
    """

    def _chamar_gemini_texto():
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            res = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt_sistema]
            )
            return res.text.strip() if hasattr(res, 'text') and res.text else None
        except Exception as e:
            print(f"[CHAT GEMINI ERRO]: {e}")
            return None

    loop = asyncio.get_running_loop()
    resposta = await loop.run_in_executor(None, _chamar_gemini_texto)
    return resposta or "Ola! Envie uma foto de rosto aqui no WhatsApp para que a nossa Inteligencia Artificial crie suas artes de aniversario em alta definicao!"
