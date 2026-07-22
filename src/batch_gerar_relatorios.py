"""
Gera relatorios do LLM para todos os meses de uma vez e salva em disco.
Rodar uma vez (ou sempre que os dados mudarem) para nao gastar API a toa
toda vez que o dashboard for aberto.

Uso: python src/batch_gerar_relatorios.py
"""
import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

TOOL_SCHEMA = {
    "name": "gerar_relatorio_risco",
    "description": "Gera um relatorio estruturado de monitoramento de modelo de credito",
    "input_schema": {
        "type": "object",
        "properties": {
            "nivel_alerta": {
                "type": "string",
                "enum": ["normal", "atencao", "critico"],
            },
            "resumo_executivo": {"type": "string"},
            "causa_provavel": {"type": "string"},
            "recomendacao": {"type": "string"},
        },
        "required": ["nivel_alerta", "resumo_executivo", "causa_provavel", "recomendacao"],
    },
}

SYSTEM_PROMPT = """Você é um analista sênior de risco de crédito, especialista em
monitoramento de modelos de score. Você escreve relatórios objetivos e técnicos,
seguindo boas práticas de mercado:

- PSI abaixo de 0.10 é estável; entre 0.10 e 0.25 merece atenção; acima de 0.25 é crítico
- Queda de AUC/KS indica perda de poder discriminante do modelo (problema mais sério que PSI alto sozinho)
- PSI alto com AUC/KS estáveis sugere mudança de população, não necessariamente falha do modelo
- Seja direto e evite jargão desnecessário no resumo executivo (ele é para um gestor, não um cientista de dados)
"""

def gerar_relatorio_mes(mes, df_metricas, historico_meses=3):
    linha_atual = df_metricas[df_metricas["mes"] == mes].iloc[0]
    historico = df_metricas[df_metricas["mes"] < mes].tail(historico_meses)

    contexto = f"""
Métricas do mês {mes}:
- PSI: {linha_atual['psi']:.3f}
- KS: {linha_atual['ks']:.3f}
- AUC: {linha_atual['auc']:.3f}

Histórico dos {historico_meses} meses anteriores:
{historico[['mes', 'psi', 'ks', 'auc']].to_string(index=False)}
"""

    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Gere o relatorio de monitoramento com base nestes dados:\n{contexto}"}],
        tools=[TOOL_SCHEMA],
        tool_choice={"type": "tool", "name": "gerar_relatorio_risco"},
    )
    return resposta.content[0].input


def main():
    df_metricas = pd.read_csv("data/processed/metricas_mensais.csv")
    relatorios = {}

    for mes in df_metricas["mes"]:
        print(f"Gerando relatorio do mes {mes}...")
        relatorios[str(mes)] = gerar_relatorio_mes(mes, df_metricas)
        time.sleep(0.5)  # evita rate limit

    with open("data/processed/relatorios_llm.json", "w", encoding="utf-8") as f:
        json.dump(relatorios, f, ensure_ascii=False, indent=2)

    print(f"\n{len(relatorios)} relatorios salvos em data/processed/relatorios_llm.json")


if __name__ == "__main__":
    main()
