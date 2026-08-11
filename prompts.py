"""
Módulo de armazenagem dos Prompts, Mensagens e Pacotes de Preço do Auto-Aniversário AI.
"""

# Prompts de Estilos de IA Realistas para o Gemini
PROMPTS_ESTILOS = {
    "estilo_1": """
[IDENTIDADE FACIAL MÁXIMA - IDÊNTICA]: Mantenha com precisão cirúrgica o rosto, olhos, formato e tom de pele da pessoa na foto enviada.
Crie um retrato cinematográfico fotorrealista em alta definição 8k da pessoa da foto transformada no guerreiro Goku Super Saiyajin de Dragon Ball Z.
- Cabelo loiro espetado reluzente de Super Saiyajin com aura de energia dourada brilhante e raios elétricos ao redor do corpo.
- Vestimeta: quimono clássico de artes marciais laranja e azul com faixa escura na cintura.
- Fundo festivo comemorativo de aniversário com balões metálicos dourados, luzes cintilantes e um bolo de aniversário épico com velas acesas.
- Texto em destaque 3D brilhante: "Feliz Aniversário Guerreiro!".
- Iluminação de estúdio profissional, renderização 8k fotorrealista e cinematográfica.
""",
    "estilo_2": """
[IDENTIDADE FACIAL MÁXIMA - IDÊNTICA]: Mantenha o rosto e expressão realista da pessoa na foto fornecida.
Crie uma fotografia de estúdio de luxo fotorrealista 8k de comemoração de aniversário.
- Fundo elegante de festa sofisticada com balões metálicos rose gold e prateados flutuantes, confetes e iluminação suave bokeh.
- Bolo de aniversário gourmet de 3 andares com velas acesas à frente.
- Texto estilizado dourado cintilante: "Feliz Aniversário!".
- Iluminação de estúdio fotográfico profissional com ultra nitidez e textura realista de pele.
""",
    "estilo_3": """
[IDENTIDADE FACIAL MÁXIMA - IDÊNTICA]: Mantenha os traços faciais reais e formato do rosto da pessoa na foto enviada.
Crie uma imagem realista moderna e épica de festa de aniversário com iluminação Neon.
- Fundo com letreiro de néon brilhante em destaque escrito "Happy Birthday" com balões festivos metálicos.
- Efeitos de luzes brilhantes e confetes reluzentes no ar.
- Estilo fotográfico vibrante, moderno e detalhado em 8K.
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
🎉 *Parabéns pelo seu Aniversário!* 🎂

Recebemos a sua foto! Nossa Inteligência Artificial já está gerando as suas prévias de aniversário em alta qualidade.

Aguarde só alguns instantes... 🚀
"""

# Mensagem de Escolha de Pacote com Códigos PIX
def get_message_oferta_pacotes(pix_copia_cola_999: str, pix_copia_cola_1499: str, pix_copia_cola_1999: str) -> str:
    return f"""
✨ *Sua Arte de Aniversário Ficou Pronta!* 🎈

Acabamos de enviar uma **prévia com marca d'água** da sua imagem acima!

Escolha qual pacote você quer receber em **Altíssima Definição (HD)** sem marca d'água:

---
⭐ *Opção 1 (R$ 9,99): 1 Foto HD*
Copie o PIX: `{pix_copia_cola_999}`

---
🔥 *Opção 2 (R$ 14,99): Combo 2 Fotos HD*
Copie o PIX: `{pix_copia_cola_1499}`

---
👑 *Opção 3 (R$ 19,99 - VIP): Pacote VIP 3 Fotos HD*
Copie o PIX: `{pix_copia_cola_1999}`

---
 Assim que realizar o PIX do pacote escolhido no seu aplicativo do banco, suas fotos HD sem marca d'água serão enviadas automaticamente aqui! 🚀
"""

# Mensagem enviada automaticamente quando o pagamento PIX é APROVADO
def get_message_pagamento_aprovado(qtd_artes: int) -> str:
    return f"""
✅ *PAGAMENTO CONFIRMADO COM SUCESSO!* 🎉

Muito obrigado! Estamos enviando abaixo a(s) sua(s) **{qtd_artes} Foto(s) em Altíssima Definição (HD)** totalmente limpas e sem marca d'água! 

Aproveite o seu dia e compartilhe com seus amigos e familiares! 🎂🎈
"""
