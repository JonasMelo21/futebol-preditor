# ⚽ Fut-IA: Preditor de Resultados da Copa do Brasil com ML

![Python](https://img.shields.io/badge/python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

> Uma aplicação web que utiliza Inteligência Artificial para prever probabilidades de resultados em jogos de futebol baseando-se no desempenho recente dos times.

---

## 🚀 **Demo Online**
O projeto está em produção! Acesse e faça suas simulações:

### 👉 [Clique aqui para acessar o Fut-IA](https://futebol-preditor-mrispqpjk2gjhmgxng3ttf.streamlit.app/)

---

## 🧠 **O Projeto**

Este projeto foi desenvolvido com fins didáticos para aplicar conceitos de **Engenharia de Dados** e **Machine Learning** em um cenário real (e imprevisível): o futebol brasileiro.

O objetivo não é apenas "chutar" um vencedor, mas calcular a probabilidade matemática de cada resultado (Vitória do Mandante, Empate, Vitória do Visitante) com base em métricas objetivas.

### **Como funciona a Inteligência?**
O modelo não olha para a "camisa" ou tradição do time. Ele analisa a **forma recente** (últimos 5 jogos), considerando:
* Média de Gols Marcados ⚽
* Média de Posse de Bola 📊
* Média de Chutes no Gol 🎯
* Média de Escanteios 🚩

---

## 🛠️ **Arquitetura e Tecnologias**

O fluxo de dados segue a seguinte pipeline:

1.  **Ingestão:** Coleta de dados históricos via API de Futebol (API-Football/RapidAPI).
2.  **Processamento (ETL):** Limpeza e transformação dos dados com **Pandas**. Criação de *features* de médias móveis (Window Functions).
3.  **Modelagem:** Treinamento de um algoritmo **Random Forest Classifier** (Scikit-Learn) para identificar padrões de vitória.
4.  **Frontend:** Interface interativa desenvolvida em **Streamlit**, com gráficos **Plotly** para comparação visual.
5.  **Deploy:** Hospedagem no Streamlit Community Cloud com CI/CD via GitHub.

---

## 📂 **Estrutura do Repositório**

```bash
futebol-preditor/
├── data/                  # Armazenamento de dados processados (CSV)
├── frontend/              # Código do site (Streamlit)
│   ├── app.py             # Aplicação principal
│   └── pix.png            # QR Code para doação
├── models/                # Modelos treinados (.pkl)
├── notebooks/             # Jupyter Notebooks para análise e treino
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação
