import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'modelo_futebol.pkl')
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'processed', 'base_dados_site.csv')
PIX_PATH = os.path.join(BASE_DIR, 'pix.jpeg')

# --- DICIONÁRIO DE LOGOS (Série A e B principais) ---
# URLs públicas (Wikimedia/PNGs). Adicione mais conforme necessário.
LOGOS = {
    "América-MG": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Am%C3%A9rica_Mineiro_logo.png",
    "Athletico Paranaense": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Logo_Club_Athletico_Paranaense_2019.png",
    "Atletico Goianiense": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Atletico_Goianiense_logo.png",
    "Atletico Mineiro": "https://upload.wikimedia.org/wikipedia/commons/2/27/Clube_Atl%C3%A9tico_Mineiro_logo.png",
    "Bahia": "https://upload.wikimedia.org/wikipedia/pt/2/2c/Esporte_Clube_Bahia_logo.png",
    "Botafogo": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Botafogo_de_Futebol_e_Regatas_logo.svg",
    "Ceara": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cear%C3%A1_Sporting_Club_logo.svg/1200px-Cear%C3%A1_Sporting_Club_logo.svg.png",
    "Corinthians": "https://upload.wikimedia.org/wikipedia/pt/b/b4/Corinthians_simbolo.png",
    "Coritiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Coritiba_FBC_%282006%29.png/1200px-Coritiba_FBC_%282006%29.png",
    "Cruzeiro": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Logo_Cruzeiro_1996.png",
    "Cuiaba": "https://upload.wikimedia.org/wikipedia/pt/2/20/Cuiab%C3%A1_EC.png",
    "Flamengo": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Flamengo_braz_logo.svg",
    "Fluminense": "https://upload.wikimedia.org/wikipedia/pt/a/a3/FFC_logo.svg",
    "Fortaleza": "https://upload.wikimedia.org/wikipedia/commons/4/42/Fortaleza_Esporte_Clube_logo.svg",
    "Goias": "https://upload.wikimedia.org/wikipedia/commons/5/59/Goias_Esporte_Clube_logo.svg",
    "Gremio": "https://upload.wikimedia.org/wikipedia/commons/5/50/Gr%C3%AAmio_FBPA_logo.svg",
    "Internacional": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Escudo_do_Sport_Club_Internacional.svg",
    "Juventude": "https://upload.wikimedia.org/wikipedia/pt/9/91/Juventude_logo.png",
    "Palmeiras": "https://upload.wikimedia.org/wikipedia/commons/1/10/Palmeiras_logo.svg",
    "Red Bull Bragantino": "https://upload.wikimedia.org/wikipedia/pt/9/92/Red_Bull_Bragantino.png",
    "Santos": "https://upload.wikimedia.org/wikipedia/commons/1/15/Santos_Logo.png",
    "Sao Paulo": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg",
    "Sport Recife": "https://upload.wikimedia.org/wikipedia/pt/1/17/Sport_Club_do_Recife.png",
    "Vasco DA Gama": "https://upload.wikimedia.org/wikipedia/pt/a/ac/CRVascodaGama.png",
    "Vitoria": "https://upload.wikimedia.org/wikipedia/pt/0/07/Esporte_Clube_Vit%C3%B3ria_logo.png"
}
URL_GENERICA = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Fut-IA: Previsões Matemáticas",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    # Se quiser colocar uma foto sua ou logo aqui em cima, pode manter
    st.image("https://cdn-icons-png.flaticon.com/512/8637/8637099.png", width=100)
    
    st.title("Sobre o Projeto")
    st.write("""
    Este é um projeto de **Ciência de Dados** desenvolvido para fins didáticos.
    Utilizamos algoritmos de Machine Learning (Random Forest) para encontrar padrões em jogos de futebol.
    """)

    # Texto novo aqui 👇
    st.write("**Quer ver o código ou bater um papo? Meus contatos estão logo abaixo:**")
    
    st.divider()
    
    st.write("👨‍💻 **Desenvolvedor:** Jonas Melo")
    st.write("🎓 Estudante de Ciência da Computação")

    
    # --- REDES SOCIAIS (NOVO) ---
    c_git, c_in = st.columns(2)
    with c_git:
        st.link_button("GitHub 💻", "https://github.com/JonasMelo21")
    with c_in:
        st.link_button("LinkedIn 👔", "https://www.linkedin.com/in/jonas-honorato-melo/")
    
    
    
    st.divider()
    st.markdown("### ☕ Apoie o Estudante!")
    st.write("Se o projeto te ajudou ou você achou legal, pague um cafézinho simbólico (R$ 3,50) pra manter o servidor rodando!")
    
    # Exibe o QR Code se o arquivo existir
    if os.path.exists(PIX_PATH):
        st.image(PIX_PATH, caption="Escaneie para doar", width=200)
    else:
        st.warning("QR Code não carregado (Arquivo pix.jpeg faltando)")
    
    # Campo para copiar a chave (MUITO IMPORTANTE PARA QUEM USA CELULAR)
    st.write("**Ou copie a chave Pix:**")
    st.code("00020101021126660014br.gov.bcb.pix0114+55619950373620226Muito obrigado pela doacao52040000530398654043.505802BR5917JONAS H L DE MELO6008BRASILIA62070503***63045E5B", language="text") # <--- TROQUE PELA SUA CHAVE AQUI
# --- CARREGAMENTO ---
@st.cache_data
def carregar_dados():
    try:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(DATA_PATH):
            return None, None, "Arquivos de modelo não encontrados."
        
        modelo = joblib.load(MODEL_PATH)
        df = pd.read_csv(DATA_PATH)
        if 'date' in df.columns: df['date'] = pd.to_datetime(df['date'])
        return modelo, df, None
    except Exception as e:
        return None, None, str(e)

modelo, df, erro = carregar_dados()

# --- CABEÇALHO E DISCLAIMER ---
st.title("⚽ Fut-IA: Inteligência Artificial no Futebol")
st.markdown("##### Prevendo resultados com base em desempenho recente e estatísticas avançadas.")

st.warning("""
    ⚠️ **AVISO LEGAL:** Este site é um projeto estritamente **EDUCACIONAL** e **ACADÊMICO**. 
    Os resultados apresentados são probabilidades matemáticas baseadas em dados passados e **não garantem resultados futuros**. 
    O autor não incentiva apostas esportivas e não se responsabiliza por perdas financeiras. Jogue com responsabilidade.
""")

if erro:
    st.error(f"Erro ao carregar sistema: {erro}")
    st.stop()

# --- ÁREA DE SELEÇÃO ---
st.divider()
col_team1, col_x, col_team2 = st.columns([1, 0.2, 1])

# Filtro de times
todos_times = sorted(pd.concat([df['home_team'], df['away_team']]).unique())

with col_team1:
    st.subheader("Mandante 🏠")
    time_casa = st.selectbox("Selecione o time da casa", todos_times, index=todos_times.index("Vasco DA Gama") if "Vasco DA Gama" in todos_times else 0)
    st.image(LOGOS.get(time_casa, URL_GENERICA), width=120)

with col_x:
    st.markdown("<h1 style='text-align: center; vertical-align: middle; padding-top: 100px;'>X</h1>", unsafe_allow_html=True)

with col_team2:
    st.subheader("Visitante ✈️")
    time_visitante = st.selectbox("Selecione o time visitante", todos_times, index=todos_times.index("Corinthians") if "Corinthians" in todos_times else 1)
    st.image(LOGOS.get(time_visitante, URL_GENERICA), width=120)

# --- BOTÃO DE AÇÃO ---
st.markdown("---")
if st.button("🧠 PROCESSAR DADOS E PREVER VENCEDOR", type="primary", use_container_width=True):
    if time_casa == time_visitante:
        st.error("Por favor, selecione times diferentes.")
    else:
        # Lógica de buscar dados (mesma do anterior)
        try:
            stats_casa = df[(df['home_team'] == time_casa) | (df['away_team'] == time_casa)].sort_values('date').iloc[-1]
            stats_visitante = df[(df['home_team'] == time_visitante) | (df['away_team'] == time_visitante)].sort_values('date').iloc[-1]

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

            # Previsão
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

            probs = modelo.predict_proba(input_ia)[0]
            classes = modelo.classes_
            
            prob_dict = {0: 0.0, 1: 0.0, 2: 0.0} # Away, Draw, Home
            for c, p in zip(classes, probs):
                prob_dict[c] = p

            # --- RESULTADOS VISUAIS ---
            st.success("Análise Concluída com Sucesso!")
            
            # 1. Placar de Probabilidades
            c1, c2, c3 = st.columns(3)
            c1.metric(f"Vitória {time_casa}", f"{prob_dict[2]*100:.1f}%", delta="Mandante")
            c2.metric("Empate", f"{prob_dict[1]*100:.1f}%", delta_color="off")
            c3.metric(f"Vitória {time_visitante}", f"{prob_dict[0]*100:.1f}%", delta="Visitante")

            # 2. Gráfico de Radar (Comparativo Técnico)
            st.subheader("📊 Comparativo de 'Forma' (Médias Recentes)")
            
            # Normalizar dados para o gráfico ficar bonito (escala 0 a 1 ou aproximada)
            # Como posse é %, e gols é unitário, o radar chart puro pode ficar distorcido.
            # Vamos usar valores brutos mas num gráfico interativo que mostra o tooltip.
            
            categories = ['Gols Marcados', 'Chutes no Gol', 'Posse de Bola (%)', 'Escanteios']
            
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=[m_casa['goals'], m_casa['shots'], m_casa['possession']/10, m_casa['corners']], # Posse dividida por 10 pra caber na escala
                theta=categories,
                fill='toself',
                name=time_casa,
                line_color='blue'
            ))

            fig.add_trace(go.Scatterpolar(
                r=[m_visi['goals'], m_visi['shots'], m_visi['possession']/10, m_visi['corners']],
                theta=categories,
                fill='toself',
                name=time_visitante,
                line_color='red'
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=True,
                title="Raio-X dos Times (Nota: Posse de bola escala /10)"
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao gerar análise: {e}")

# --- RODAPÉ TÉCNICO ---
with st.expander("🤓 Como a mágica funciona? (Área Técnica)"):
    st.markdown("""
    ### O Algoritmo: Random Forest 🌳
    Este projeto utiliza um modelo de **Machine Learning** chamado *Random Forest* (Floresta Aleatória). 
    
    Imagine que você pergunte a 100 especialistas em futebol quem vai ganhar o jogo. 
    Cada especialista olha para um detalhe diferente: um olha só para chutes no gol, outro olha só para escanteios, outro para posse de bola.
    No final, eles votam. A decisão da "floresta" é a média desses votos.
    
    **Tecnologias Usadas:**
    * **Python:** Linguagem de programação.
    * **Pandas:** Manipulação de dados.
    * **Scikit-Learn:** Criação da inteligência artificial.
    * **Streamlit:** Criação deste site.
    
    ### Links para Estudo:
    * [Entendendo Random Forest (Artigo)](https://medium.com/machina-sapiens/o-algoritmo-da-floresta-aleat%C3%B3ria-3545f6babdf8)
    * [Documentação do Scikit-Learn](https://scikit-learn.org/stable/modules/ensemble.html#forest)
    """)