"""
Junta as metricas de monitoramento com os relatorios do LLM numa unica
tabela plana, pronta para importar no Power BI.

Uso: python src/preparar_dados_powerbi.py
"""
import json
import pandas as pd

df_metricas = pd.read_csv("data/processed/metricas_mensais.csv")

with open("data/processed/relatorios_llm.json", "r", encoding="utf-8") as f:
    relatorios = json.load(f)

linhas = []
for _, row in df_metricas.iterrows():
    mes = str(int(row["mes"]))
    relatorio = relatorios.get(mes, {})

    linhas.append({
        "mes": int(row["mes"]),
        "psi": round(row["psi"], 4),
        "ks": round(row["ks"], 4),
        "auc": round(row["auc"], 4),
        "nivel_alerta": relatorio.get("nivel_alerta", "sem_relatorio"),
        "resumo_executivo": relatorio.get("resumo_executivo", ""),
        "causa_provavel": relatorio.get("causa_provavel", ""),
        "recomendacao": relatorio.get("recomendacao", ""),
    })

df_final = pd.DataFrame(linhas)

# Coluna auxiliar util para o Power BI: cor por nivel de alerta (para formatacao condicional)
mapa_cor = {"normal": "Verde", "atencao": "Amarelo", "critico": "Vermelho", "sem_relatorio": "Cinza"}
df_final["cor_alerta"] = df_final["nivel_alerta"].map(mapa_cor)

df_final.to_csv("data/processed/dashboard_powerbi.csv", index=False, encoding="utf-8-sig")
print(f"Arquivo pronto: data/processed/dashboard_powerbi.csv ({len(df_final)} linhas)")
print(df_final.head())
