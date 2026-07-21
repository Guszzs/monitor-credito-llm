# 🏦 Monitor Inteligente de Modelo de Crédito

Sistema que calcula métricas de monitoramento de um modelo de score de crédito
(PSI, KS, AUC ao longo do tempo) e usa um LLM para gerar relatórios executivos
automáticos em português, interpretando os números e sinalizando riscos.

## 🎯 Problema que o projeto resolve

Times de risco de crédito precisam monitorar constantemente se um modelo de score
continua confiável em produção: a população de clientes mudou? O modelo está
perdendo poder preditivo? Normalmente isso vira um relatório técnico manual e demorado.
Este projeto automatiza o cálculo das métricas **e** a redação do relatório.

## 📊 Metodologia

1. Treinamento de um modelo de score de crédito simples (regressão logística)
2. Simulação de "safras" temporais (meses de produção) a partir de um dataset público
3. Cálculo de métricas de monitoramento por safra:
   - **PSI** (Population Stability Index) — mudança na distribuição da população
   - **KS** (Kolmogorov-Smirnov) e **AUC** — poder discriminante do modelo ao longo do tempo
4. Geração automática de relatório executivo via LLM (Claude), usando as métricas
   calculadas (não os dados brutos) como entrada
5. Dashboard simples reunindo tudo

## 📁 Estrutura do projeto

```
monitor-credito-llm/
├── data/
│   ├── raw/           # Dados brutos originais
│   └── processed/      # Dados limpos e safras simuladas
├── notebooks/          # Jupyter notebooks de exploração e análise
├── src/                # Scripts Python reutilizáveis
├── reports/
│   └── figures/         # Gráficos e relatórios gerados
├── requirements.txt
└── README.md
```

## 🛠️ Como rodar

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # depois preencha com sua API key da Anthropic
```

## 📈 Fontes de dados

- Dataset público de crédito (a definir: Give Me Some Credit / German Credit)

## 📌 Status

🚧 Em desenvolvimento — Fase 1: configuração inicial e primeira chamada de API

## 👤 Autor

Gustavo Cruz | [LinkedIn](https://linkedin.com/in/gustavo-goncalves-cruz) | [GitHub](https://github.com/Guszzs)
