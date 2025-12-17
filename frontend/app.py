import streamlit as st
import pandas as pd
import joblib
import os

# --- CONFIGURAÇÃO DE CAMINHOS (Baseado na sua árvore) ---
# O arquivo roda em /frontend, então voltamos um nível (..) para achar models e data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'modelo_futebol.pkl')
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'processed', 'base_dados_site.csv')

# --- CARREGAMENTO ---
@st.cache_data
def carregar_arquivos():
    if not os.path.exists(MODEL_PATH):
        return None, None, f"Erro: Modelo não encontrado em {MODEL_PATH}"
    
    if not os.path.exists(DATA_PATH):
        return None, None, f"Erro: Dados não encontrados em {DATA_PATH}"

    try:
        modelo = joblib.load(MODEL_PATH)
        df = pd.read_csv(DATA_PATH)
        # Garante que data é data
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return modelo, df, None
    except Exception as e:
        return None, None, str(e)

# --- INTERFACE ---
st.set_page_config(page_title="Guru do Futebol ⚽", layout="centered")

st.title("⚽ Preditor de Resultados (IA)")
st.markdown("Selecione os times e a Inteligência Artificial analisará a forma recente (gols, chutes, posse) para prever o vencedor.")

modelo, df, erro = carregar_arquivos()

if erro:
    st.error(erro)
    st.stop()

# Filtra lista de times únicos
todos_times = sorted(pd.concat([df['home_team'], df['away_team']]).unique())

# Layout de seleção
col1, col2 = st.columns(2)
with col1:
    time_casa = st.selectbox("Mandante (Casa)", todos_times, index=0)
with col2:
    time_visitante = st.selectbox("Visitante (Fora)", todos_times, index=1)

# Botão de Previsão
if st.button("Calcular Probabilidade 🎲", type="primary"):
    if time_casa == time_visitante:
        st.warning("Selecione times diferentes!")
    else:
        # --- A MÁGICA ---
        # 1. Buscar a "forma" mais recente do mandante
        # Filtramos onde ele jogou (casa ou fora) e pegamos o último registro
        stats_casa = df[(df['home_team'] == time_casa) | (df['away_team'] == time_casa)].sort_values('date').iloc[-1]
        
        # 2. Buscar a "forma" mais recente do visitante
        stats_visitante = df[(df['home_team'] == time_visitante) | (df['away_team'] == time_visitante)].sort_values('date').iloc[-1]

        # 3. Extrair as médias corretas
        # Se na última linha ele era Mandante, pegamos 'home_media...'. Se era Visitante, 'away_media...'
        def pegar_medias(row, time_alvo):
            prefixo = 'home' if row['home_team'] == time_alvo else 'away'
            return {
                'goals': row[f'{prefixo}_media_goals'],
                'shots': row[f'{prefixo}_media_shots_on_goal'],
                'possession': row[f'{prefixo}_media_possession'],
                'corners': row[f'{prefixo}_media_corners']
            }

        m_casa = pegar_medias(stats_casa, time_casa)
        m_visi = pegar_medias(stats_visitante, time_visitante)

        # 4. Montar o DataFrame para a IA (Tem que ter as mesmas 8 colunas do treino)
        input_ia = pd.DataFrame([{
            'home_media_goals': m_casa['goals'],
            'home_media_shots_on_goal': m_casa['shots'],
            'home_media_possession': m_casa['possession'],
            'home_media_corners': m_casa['corners'],
            'away_media_goals': m_visi['goals'],
            'away_media_shots_on_goal': m_visi['shots'],
            'away_media_possession': m_visi['possession'],
            'away_media_corners': m_visi['corners']
        }])

        # 5. Previsão Robusta
        probs = modelo.predict_proba(input_ia)[0]
        classes = modelo.classes_ # Descobre quais resultados a IA conhece (ex: só [0, 2] ou [0, 1, 2])

        # Inicializa tudo com 0.0 para não dar erro
        prob_away = 0.0 # Código 0
        prob_draw = 0.0 # Código 1
        prob_home = 0.0 # Código 2

        # Mapeia dinamicamente (seguro contra modelos "viciados")
        for classe, probabilidade in zip(classes, probs):
            if classe == 0: prob_away = probabilidade
            elif classe == 1: prob_draw = probabilidade
            elif classe == 2: prob_home = probabilidade

        # --- EXIBIÇÃO ---
        st.divider()
        c1, c2, c3 = st.columns(3)
        
        # Agora as variáveis existem garantidamente
        c1.metric(f"Vitória {time_casa}", f"{prob_home*100:.1f}%")
        c2.metric("Empate", f"{prob_draw*100:.1f}%")
        c3.metric(f"Vitória {time_visitante}", f"{prob_away*100:.1f}%")

        # Gráfico de barras simples
        chart_data = pd.DataFrame({
            "Resultado": [time_casa, "Empate", time_visitante],
            "Probabilidade": [prob_home, prob_draw, prob_away]
        })
        st.bar_chart(chart_data, x="Resultado", y="Probabilidade")
        
        # Detalhes técnicos (Debug visual)
        with st.expander("Ver estatísticas consideradas pela IA"):
            st.write(f"**{time_casa} (Médias Recentes):** {m_casa['goals']:.1f} Gols, {m_casa['shots']:.1f} Chutes, {m_casa['possession']:.0f}% Posse")
            st.write(f"**{time_visitante} (Médias Recentes):** {m_visi['goals']:.1f} Gols, {m_visi['shots']:.1f} Chutes, {m_visi['possession']:.0f}% Posse")