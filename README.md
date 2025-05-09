# Plano do Projeto: Detecção de Volatilidade em Criptomoedas

**Aluno:** Guilherme Gomes Daivd
**Curso:** Pós Tech - Machine Learning Engineering
**Disciplina:** Tech Challenge - Fase 03

## 1. Objetivo Principal do Projeto

Desenvolver um modelo de Machine Learning para detectar e/ou prever a volatilidade de criptomoedas, utilizando dados de preço e volume. O projeto culminará numa API de coleta de dados, um modelo treinado e uma aplicação simples ou dashboard para visualização dos resultados.

## 2. Fonte de Dados Primária

* **API:** Binance API (Pública)
* **Endpoint Principal:** `GET /api/v3/klines`
    * **Descrição:** Fornece dados de velas/candlesticks (OHLCV).
    * **Dados a Serem Coletados:**
        * Timestamp de Abertura/Fechamento
        * Preço de Abertura (Open)
        * Preço Máximo (High)
        * Preço Mínimo (Low)
        * Preço de Fechamento (Close)
        * Volume da Moeda Base
        * Volume da Moeda de Cotação
        * Número de Trades
    * **Acesso:** O endpoint de klines é público e não requer chave de API para acesso inicial, facilitando o desenvolvimento e testes.
    * **Parâmetros Chave:** `symbol` (ex: BTCUSDT), `interval` (ex: 1h, 4h, 1d), `limit` (máx. 1000 velas por chamada), `startTime`, `endTime`.

## 3. Estratégia de Coleta de Dados

1.  **Coleta de Dados Históricos:**
    * Utilizar scripts Python (com a biblioteca `requests`) para buscar dados históricos em lotes do endpoint `/api/v3/klines`.
    * Serão feitas chamadas iterativas, ajustando `startTime` e `endTime` para cobrir o período desejado (ex: últimos 1-3 anos) para as criptomoedas selecionadas.
2.  **Coleta de Dados "Em Tempo Real" (para o dashboard/aplicação):**
    * Implementar polling periódico (ex: a cada 1, 5 ou 15 minutos) no mesmo endpoint para buscar as velas mais recentes.
    * Alternativamente, para uma reatividade maior no futuro, pode-se explorar os WebSockets da Binance (`<symbol>@kline_<interval>`).

## 4. Foco do Modelo de Machine Learning

* **Entrada:** Séries temporais de dados OHLCV e features derivadas (ex: médias móveis, indicadores técnicos, métricas de volatilidade calculadas como Desvio Padrão dos Retornos, ATR, Largura das Bandas de Bollinger).
* **Saída (Objetivo da Detecção):**
    * **Classificação:** Categorizar a volatilidade futura (ex: Baixa, Média, Alta).
    * **Regressão:** Prever o valor de uma métrica de volatilidade (ex: ATR do próximo período).
    * **Detecção de Anomalias:** Identificar picos ou mudanças abruptas na volatilidade.
* **Modelos Potenciais:** Random Forests, XGBoost, LSTM (para abordagens de séries temporais mais complexas), modelos de GARCH (como benchmark).

## 5. Arquitetura e Tecnologias Propostas

* **Linguagem Principal:** Python
* **Coleta de Dados:** Scripts Python, biblioteca `requests`.
* **API de Coleta Própria:** FastAPI ou Flask.
* **Armazenamento de Dados:**
    * **Dados Brutos (AWS):** Amazon S3.
    * **Dados Processados/Features:** PostgreSQL em container Docker.
    * **ETL (AWS):** AWS Glue ou AWS Lambda (para interagir entre S3 e o banco de dados, se necessário, ou para processamentos agendados).
* **Treinamento e Deploy do Modelo (AWS):** Amazon SageMaker.
* **Aplicação/Dashboard (AWS):** Streamlit ou Dash, hospedado em AWS Elastic Beanstalk ou AWS App Runner.
* **Versionamento:** Git e GitHub.

## 6. Entregáveis Conforme o Desafio

1.  API que coleta dados (da Binance) e armazena (no S3 e PostgreSQL).
2.  Modelo de ML treinado com a base de dados coletada.
3.  Código no GitHub com documentação.
4.  Vídeo explicativo (storytelling do projeto).
5.  Modelo produtivo (alimentando aplicação simples ou dashboard).
