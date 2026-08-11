"""
Script de teste direto da API do Gemini com os 3 estilos de fotografia realistas (Sem 3D).
Uso: python test_gemini.py caminho/para/foto.jpg
"""

import sys
import os
import io

def test_gemini_estilos_realistas():
    if len(sys.argv) < 2:
        print("Por favor, informe a foto de teste. Exemplo:")
        print("   python test_gemini.py foto_teste.jpg")
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Arquivo nao encontrado: {file_path}")
        return

    print(f"Lendo foto de entrada: {file_path}...")
    with open(file_path, "rb") as f:
        img_bytes = f.read()

    print("1. Enviando foto para a API do Gemini (Gerando os 3 estilos realistas)...")
    from gemini_service import gerar_pacote_artes_async
    from watermark_service import aplicar_marca_dagua_previa
    import asyncio
    
    try:
        # Gerar os 3 estilos realistas
        artes_dict = asyncio.run(gerar_pacote_artes_async(img_bytes, qtd=3))
        
        for estilo, arte_hd_bytes in artes_dict.items():
            filename = f"resultado_{estilo}_HD.jpg"
            with open(filename, "wb") as f:
                f.write(arte_hd_bytes)
            print(f"[HD] Estilo '{estilo}' salvo em: {os.path.abspath(filename)}")

        # Teste de Prévia com Marca d'Água na foto principal
        previa_bytes = aplicar_marca_dagua_previa(artes_dict["estilo_1"])
        file_previa = "resultado_PREVIA_MARCADAGUA.jpg"
        with open(file_previa, "wb") as f:
            f.write(previa_bytes)
        print(f"[PREVIA] Marca d'agua salva em: {os.path.abspath(file_previa)}")

    except Exception as e:
        print(f"Erro durante os testes: {e}")

if __name__ == "__main__":
    test_gemini_estilos_realistas()
