"""
Módulo de armazenagem dos Prompts, Mensagens e Pacotes de Preço do Auto-Aniversário AI.
"""

# Prompts de Estilos de IA Realistas para o Gemini
PROMPTS_ESTILOS = {
    "estilo_1": """
[IDENTIDADE FACIAL MAXIMA - IDENTICA]: Mantenha com precisao cirurgica o rosto, olhos, formato e tom de pele da pessoa na foto enviada.
Crie um retrato cinematografico fotorrealista em alta definicao 8k da pessoa da foto transformada no guerreiro Goku Super Saiyajin de Dragon Ball Z.
- Cabelo loiro espetado reluzente de Super Saiyajin com aura de energia dourada brilhante e raios eletricos ao redor do corpo.
- Vestimenta: quimono classico de artes marciais laranja e azul com faixa escura na cintura.
- Fundo festivo comemorativo de aniversario com baloes metalicos dourados, luzes cintilantes e um bolo de aniversario epico com velas acesas.
- Texto em destaque 3D brilhante: "Feliz Aniversario Guerreiro!".
- Iluminacao de estudio profissional, renderizacao 8k fotorrealista e cinematografica.
""",
    "estilo_2": """
[IDENTIDADE FACIAL MAXIMA - IDENTICA]: Mantenha o rosto e expressao realista da pessoa na foto fornecida.
Crie uma fotografia de estudio de luxo fotorrealista 8k de comemoracao de aniversario.
- Fundo elegante de festa sofisticada com baloes metalicos rose gold e prateados flutuantes, confetes e iluminacao suave bokeh.
- Bolo de aniversario gourmet de 3 andares com velas acesas a frente.
- Texto estilizado dourado cintilante: "Feliz Aniversario!".
- Iluminacao de estudio fotografico profissional com ultra nitidez e textura realista de pele.
""",
    "estilo_3": """
[IDENTIDADE FACIAL MAXIMA - IDENTICA]: Mantenha os tracos faciais reais e formato do rosto da pessoa na foto enviada.
Crie uma imagem realista moderna e epica de festa de aniversario com iluminacao Neon.
- Fundo com letreiro de neon brilhante em destaque escrito "Happy Birthday" com baloes festivos metalicos.
- Efeitos de luzes brilhantes e confetes reluzentes no ar.
- Estilo fotografico vibrante, moderno e detalhado em 8K.
"""
}


# Tabela de Preços e Pacotes
PACOTES_PRECO = {
    "1": {"nome": "1 Foto HD", "qtd_artes": 1, "valor": 9.99},
    "2": {"nome": "Combo 2 Fotos HD", "qtd_artes": 2, "valor": 14.99},
    "3": {"nome": "Pacote VIP 3 Fotos HD", "qtd_artes": 3, "valor": 19.99}
}

# Mensagem inicial enviada ao receber a foto
MESSAGE_WELCOME = """
*Parabens pelo seu Aniversario!*

Recebemos a sua foto! Nossa Inteligencia Artificial ja esta gerando as suas previas de aniversario em alta qualidade.

Aguarde so alguns instantes...
"""

# Mensagem de Escolha de Pacote com Codigos PIX
def get_message_oferta_pacotes(pix_copia_cola_999: str, pix_copia_cola_1499: str, pix_copia_cola_1999: str) -> str:
    return f"""
*Sua Arte de Aniversario Ficou Pronta!*

Acabamos de enviar uma **previa com marca d'agua** da sua imagem acima!

Escolha qual pacote voce quer receber em **Altissima Definicao (HD)** sem marca d'agua:

---
*Opcao 1 (R$ 9,99): 1 Foto HD*
Copie o PIX: `{pix_copia_cola_999}`

---
*Opcao 2 (R$ 14,99): Combo 2 Fotos HD*
Copie o PIX: `{pix_copia_cola_1499}`

---
*Opcao 3 (R$ 19,99 - VIP): Pacote VIP 3 Fotos HD*
Copie o PIX: `{pix_copia_cola_1999}`

---
Assim que realizar o PIX do pacote escolhido no seu aplicativo do banco, suas fotos HD sem marca d'agua serao enviadas automaticamente aqui!
"""

# Mensagem enviada automaticamente quando o pagamento PIX e APROVADO
def get_message_pagamento_aprovado(qtd_artes: int) -> str:
    return f"""
*PAGAMENTO CONFIRMADO COM SUCESSO!*

Muito obrigado! Estamos enviando abaixo a(s) sua(s) **{qtd_artes} Foto(s) em Altissima Definicao (HD)** totalmente limpas e sem marca d'agua! 

Aproveite o seu dia e compartilhe com seus amigos e familiares!
"""
