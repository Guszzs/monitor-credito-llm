import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

resposta = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    messages=[
        {"role": "user", "content": "Explique o que é PSI (Population Stability Index) em uma frase, para alguém de risco de crédito."}
    ]
)

print(resposta.content[0].text)
