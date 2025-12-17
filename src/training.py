import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Caminhos
DATA_PATH = 'data/processed/base_completa_futebol.csv'
MODEL_DIR = 'backend/models'
MODEL_PATH = f'{MODEL_DIR}/futebol_model_v1.pkl'
ENCODER_PATH = f'{MODEL_DIR}/team_encoder.pkl'

def train_model():
    print("🧠 Iniciando treinamento do modelo...")
    
    # 1. Carregar Dados
    if not os.path.exists(DATA_PATH):
        print("❌ Erro: Arquivo de dados não encontrado. Rode o ingestion.py primeiro.")
        return

    df = pd.read_csv(DATA_PATH)
    print(f"📦 Dados carregados: {len(df)} jogos.")

    # 2. Pré-processamento (Engenharia de Features Simples)
    # Vamos converter quem ganhou (Home, Away, Draw) em números: 0, 1, 2
    # Mas o LabelEncoder faz isso automático se passarmos a string.
    
    # Precisamos transformar os nomes dos times em números únicos
    # Ex: Flamengo = 10, Vasco = 25...
    le = LabelEncoder()
    
    # Juntamos todos os times (casa e fora) pra aprender todos os nomes possíveis
    all_teams = pd.concat([df['home_team'], df['away_team']]).unique()
    le.fit(all_teams)
    
    # Transforma as colunas de texto em números
    df['home_code'] = le.transform(df['home_team'])
    df['away_code'] = le.transform(df['away_team'])
    
    # Target (O que queremos prever): 'winner' (Home, Away, Draw)
    # Vamos converter para números também
    target_le = LabelEncoder()
    df['target'] = target_le.fit_transform(df['winner'])
    
    # Features (As dicas que damos pro modelo)
    # Por enquanto: Quem é o mandante, quem é o visitante, e o ID da liga (Série A ou Copa)
    features = ['home_code', 'away_code', 'league_id']
    
    X = df[features]
    y = df['target']

    # 3. Divisão Treino (aprender) e Teste (prova final)
    # 80% pra estudar, 20% pra prova
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Treinamento (Random Forest)
    # Um modelo robusto que cria várias "árvores de decisão"
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # 5. Avaliação
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\n📊 Acurácia do Modelo: {acc:.2%}")
    print("------------------------------------------------")
    print("Nota: Futebol é difícil. 40-50% em 3 classes (Vitória, Empate, Derrota) já é melhor que chute aleatório (33%).")
    
    # 6. Salvar o Modelo e os Decodificadores
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH) # Salvamos o dicionário de nomes dos times
    joblib.dump(target_le, f'{MODEL_DIR}/target_encoder.pkl')
    
    print(f"\n💾 Modelo salvo em: {MODEL_PATH}")
    print(f"💾 Dicionário de times salvo em: {ENCODER_PATH}")

if __name__ == "__main__":
    train_model()