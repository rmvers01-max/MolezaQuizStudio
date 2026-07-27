import json

from .models import AIContentRequest


class MolezaPromptBuilder:
    """Monta prompts especializados para o canal Moleza Quiz."""

    def criar_prompt(self, pedido: AIContentRequest) -> str:
        pedido.validar()

        esquema = {
            "titulo": "string",
            "titulo_alternativo": "string",
            "descricao": "string",
            "hashtags": ["string"],
            "tags": ["string"],
            "texto_thumbnail": "string",
            "prompt_thumbnail": "string",
            "introducao": "string",
            "chamada_inscricao": "string",
            "perguntas": [
                {
                    "numero": 1,
                    "pergunta": "string",
                    "opcoes": ["string", "string"],
                    "resposta": "string",
                    "narracao": "string",
                }
            ],
            "observacoes_estrategicas": ["string"],
        }

        return f"""
Você é o estrategista de conteúdo do canal brasileiro "{pedido.nome_canal}".

Crie um pacote completo para um vídeo de quiz em português do Brasil.

DADOS DO PEDIDO
- Tema: {pedido.tema}
- Público: {pedido.publico}
- Formato: {pedido.formato}
- Quantidade de perguntas: {pedido.quantidade_perguntas}
- Estilo visual e editorial: {pedido.estilo}
- Observações adicionais: {pedido.observacoes or "Nenhuma"}

REGRAS EDITORIAIS
1. O conteúdo deve ser apropriado para toda a família.
2. Use linguagem simples, divertida, natural e energética.
3. Evite promessas enganosas, informações inventadas e clickbait falso.
4. O título deve ser atraente, claro e adequado ao YouTube.
5. A descrição deve conter palavras-chave naturalmente, sem repetição artificial.
6. Hashtags devem começar com #.
7. Tags devem ser entregues sem #.
8. O texto da thumbnail deve ser curto e legível, preferencialmente com até 5 palavras.
9. O prompt da thumbnail deve descrever composição, fundo, mascote, objetos,
   iluminação, cores, texto e espaço visual para alta legibilidade.
10. Gere exatamente {pedido.quantidade_perguntas} perguntas.
11. Cada pergunta deve ser coerente com o formato solicitado.
12. Em quizzes de opinião ou preferência, como "O que você prefere?",
    "Você escolheria?", "Qual você prefere?" ou formatos equivalentes,
    não existe resposta correta. Nesses casos, entregue o campo
    "resposta" como uma string vazia: "".
13. Somente quizzes objetivos, com resposta verificável, devem trazer
    uma resposta correta no campo "resposta".
14. Não inclua markdown, comentários ou texto fora do JSON.

FORMATO OBRIGATÓRIO
Retorne somente um objeto JSON válido seguindo esta estrutura:

{json.dumps(esquema, ensure_ascii=False, indent=2)}
""".strip()
