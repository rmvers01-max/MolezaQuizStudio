import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class AIService:

    def gerar_quiz(self, tema, quantidade):

        prompt = f"""
Crie {quantidade} perguntas de múltipla escolha.

Tema:
{tema}

Retorne SOMENTE um JSON.

Formato:

[
 {
   "pergunta":"...",
   "alternativas":[
      "A",
      "B",
      "C",
      "D"
   ],
   "resposta":1
 }
]

Nada além do JSON.
"""

        resposta = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        texto = resposta.choices[0].message.content

        return json.loads(texto)
