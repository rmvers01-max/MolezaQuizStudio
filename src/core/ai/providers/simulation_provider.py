import re
import unicodedata

from .base_provider import BaseAIProvider


class SimulationProvider(BaseAIProvider):
    """
    Provedor offline para desenvolvimento e testes.

    Ele não utiliza internet nem créditos. O retorno imita o JSON esperado
    pela Central de IA para que o restante do fluxo possa ser testado.
    """

    def gerar_texto(
        self,
        prompt: str,
        temperatura: float = 0.7,
    ) -> str:
        tema = self._extrair_valor(
            prompt,
            "Tema",
            "Quiz divertido"
        )
        publico = self._extrair_valor(
            prompt,
            "Público",
            "Família"
        )
        formato = self._extrair_valor(
            prompt,
            "Formato",
            "Vídeo longo"
        )
        quantidade = self._extrair_quantidade(
            prompt
        )

        titulo_tema = self._normalizar_titulo(
            tema
        )

        quiz_preferencia = self._eh_quiz_preferencia(
            tema
        )

        perguntas = [
            self._criar_pergunta(
                indice=indice,
                tema=tema,
                quiz_preferencia=quiz_preferencia
            )
            for indice in range(
                1,
                quantidade + 1
            )
        ]

        hashtags = self._criar_hashtags(
            tema
        )

        tags = self._criar_tags(
            tema=tema,
            publico=publico,
            formato=formato
        )

        dados = {
            "titulo": (
                f"{titulo_tema} | "
                f"{quantidade} DESAFIOS DIVERTIDOS!"
            ),
            "titulo_alternativo": (
                f"VOCÊ CONSEGUE COMPLETAR ESTE QUIZ? "
                f"{titulo_tema}"
            ),
            "descricao": (
                f"Prepare-se para um quiz divertido sobre {tema}. "
                f"São {quantidade} perguntas para brincar com toda "
                f"a família. Comente quantas você acertou e compartilhe "
                f"o vídeo com seus amigos."
            ),
            "hashtags": hashtags,
            "tags": tags,
            "texto_thumbnail": self._criar_texto_thumbnail(
                tema
            ),
            "prompt_thumbnail": (
                "Thumbnail infantil e familiar em 1280x720, "
                "fundo vibrante com contraste forte, composição limpa, "
                f"tema principal: {tema}, mascote preguiça Moleza Quiz "
                "em destaque com expressão alegre, objetos grandes "
                "relacionados ao tema, iluminação colorida, contorno "
                "branco nos elementos, sombras suaves, texto curto e "
                "muito legível, espaço seguro nas bordas, visual de alto CTR."
            ),
            "introducao": (
                f"Olá, pessoal! Hoje temos um desafio especial sobre "
                f"{tema}. Prepare-se, escolha suas respostas e conte "
                f"no final quantas você acertou!"
            ),
            "chamada_inscricao": (
                "Antes de continuar, deixe o seu like, inscreva-se "
                "no Moleza Quiz e ative o sininho para não perder "
                "os próximos desafios!"
            ),
            "perguntas": perguntas,
            "observacoes_estrategicas": [
                (
                    "Este conteúdo foi criado pelo Modo Simulação "
                    "e serve para testar o fluxo do programa."
                ),
                (
                    "Revise as perguntas e respostas antes de publicar."
                ),
                (
                    "Use imagens grandes e pouco texto na thumbnail."
                ),
            ],
        }

        import json

        return json.dumps(
            dados,
            ensure_ascii=False,
            indent=2
        )

    def _extrair_valor(
        self,
        prompt: str,
        nome: str,
        padrao: str
    ) -> str:
        padrao_regex = rf"-\s*{re.escape(nome)}:\s*(.+)"
        correspondencia = re.search(
            padrao_regex,
            prompt,
            flags=re.IGNORECASE
        )

        if not correspondencia:
            return padrao

        valor = correspondencia.group(1).strip()

        return valor or padrao

    def _extrair_quantidade(
        self,
        prompt: str
    ) -> int:
        correspondencia = re.search(
            r"Quantidade de perguntas:\s*(\d+)",
            prompt,
            flags=re.IGNORECASE
        )

        if not correspondencia:
            return 10

        return max(
            1,
            min(
                int(correspondencia.group(1)),
                100
            )
        )

    def _criar_pergunta(
        self,
        indice: int,
        tema: str,
        quiz_preferencia: bool
    ) -> dict:
        modelos = [
            (
                f"Qual opção combina mais com o tema {tema}?",
                [
                    f"Opção divertida {indice}A",
                    f"Opção divertida {indice}B",
                ]
            ),
            (
                f"O que você escolheria no desafio {indice} sobre {tema}?",
                [
                    f"Escolha {indice}A",
                    f"Escolha {indice}B",
                ]
            ),
            (
                f"Qual alternativa você prefere na rodada {indice}?",
                [
                    f"Alternativa {indice}A",
                    f"Alternativa {indice}B",
                ]
            ),
        ]

        pergunta, opcoes = modelos[
            (indice - 1) % len(modelos)
        ]

        resposta = (
            ""
            if quiz_preferencia
            else opcoes[0]
        )

        return {
            "numero": indice,
            "pergunta": pergunta,
            "opcoes": opcoes,
            "resposta": resposta,
            "narracao": (
                f"Pergunta número {indice}. {pergunta} "
                f"Você prefere {opcoes[0]} ou {opcoes[1]}?"
            ),
        }

    def _eh_quiz_preferencia(
        self,
        tema: str
    ) -> bool:
        texto = unicodedata.normalize(
            "NFKD",
            tema.lower()
        )

        texto = "".join(
            caractere
            for caractere in texto
            if not unicodedata.combining(
                caractere
            )
        )

        expressoes = (
            "o que voce prefere",
            "qual voce prefere",
            "voce escolheria",
            "voce prefere",
            "escolha um",
            "faca sua escolha",
        )

        return any(
            expressao in texto
            for expressao in expressoes
        )

    def _criar_hashtags(
        self,
        tema: str
    ) -> list[str]:
        palavras = self._palavras_relevantes(
            tema
        )

        hashtags = [
            "#MolezaQuiz",
            "#Quiz",
            "#QuizInfantil",
            "#DiversãoEmFamília",
        ]

        for palavra in palavras[:3]:
            hashtags.append(
                f"#{palavra}"
            )

        return list(
            dict.fromkeys(
                hashtags
            )
        )

    def _criar_tags(
        self,
        tema: str,
        publico: str,
        formato: str
    ) -> list[str]:
        tags = [
            "moleza quiz",
            "quiz",
            "quiz infantil",
            "quiz para família",
            "desafio divertido",
            tema.lower(),
            publico.lower(),
            formato.lower(),
        ]

        return list(
            dict.fromkeys(
                tag.strip()
                for tag in tags
                if tag.strip()
            )
        )

    def _criar_texto_thumbnail(
        self,
        tema: str
    ) -> str:
        palavras = self._palavras_relevantes(
            tema
        )

        if not palavras:
            return "VOCÊ CONSEGUE?"

        texto = " ".join(
            palavras[:4]
        ).upper()

        return texto[:35]

    def _normalizar_titulo(
        self,
        texto: str
    ) -> str:
        return texto.strip().upper()

    def _palavras_relevantes(
        self,
        texto: str
    ) -> list[str]:
        texto_normalizado = unicodedata.normalize(
            "NFKD",
            texto
        )

        texto_sem_acentos = "".join(
            caractere
            for caractere in texto_normalizado
            if not unicodedata.combining(
                caractere
            )
        )

        palavras = re.findall(
            r"[A-Za-z0-9]+",
            texto_sem_acentos
        )

        ignoradas = {
            "o",
            "a",
            "os",
            "as",
            "de",
            "da",
            "do",
            "das",
            "dos",
            "e",
            "ou",
            "que",
            "voce",
            "um",
            "uma",
        }

        return [
            palavra
            for palavra in palavras
            if palavra.lower() not in ignoradas
        ]
