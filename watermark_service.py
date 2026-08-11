import io
from PIL import Image, ImageDraw, ImageFont

def aplicar_marca_dagua_previa(imagem_bytes: bytes, texto: str = "PRÉVIA - LIBERE VIA PIX") -> bytes:
    """
    Aplica uma marca d'água semi-transparente sobre a imagem gerada pela IA
    para servir de prévia antes da confirmação do pagamento.
    """
    img = Image.open(io.BytesIO(imagem_bytes)).convert("RGBA")
    
    # Criar uma camada transparente para o texto da marca d'água
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    width, height = img.size
    font_size = int(height / 15)
    
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Desenhar faixa diagonal com marca d'água repetida
    step_y = int(height / 4)
    for y in range(step_y // 2, height, step_y):
        draw.text((width * 0.1, y), texto, fill=(255, 255, 255, 140), font=font)
        draw.text((width * 0.1 + 2, y + 2), texto, fill=(0, 0, 0, 140), font=font)

    # Combinar a imagem original com a marca d'água
    watermarked = Image.alpha_composite(img, overlay).convert("RGB")
    
    output = io.BytesIO()
    watermarked.save(output, format="JPEG", quality=85)
    return output.getvalue()
