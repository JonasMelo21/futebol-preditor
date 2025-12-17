import requests
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
import time

# Carrega o ambiente
load_dotenv(find_dotenv())

API_KEY = os.getenv("FOOTBALL_API_KEY")
headers = {"x-apisports-key": API_KEY}
base_url = "https://v3.football.api-sports.io"

def get_combined_data():
    all_matches = []
    
    # Configuração das Ligas
    # 71 = Brasileirão Série A
    # 73 = Copa do Brasil
    leagues = {
        71: "Brasileirao Serie A",
        73: "Copa do Brasil"
    }
    
    # Anos para treino (quanto mais, melhor, mas cuidado com limite da API)
    # Vamos pegar de 2021 pra cá para garantir dados recentes e relevantes
    years = [2021, 2022, 2023, 2024, 2025]

    print(f"🚀 Iniciando coleta COMBINADA (Brasileirão + Copa do Brasil)...")

    for league_id, league_name in leagues.items():
        print(f"\n🏆 Entrando na Liga: {league_name} (ID: {league_id})")
        
        for year in years:
            print(f"   📅 Baixando temporada {year}...", end="")
            
            url = f"{base_url}/fixtures"
            # status="FT" (Full Time) pega jogos terminados
            # Se for 2025, vamos pegar também, caso tenha algum jogo adiantado ou estaduais que contem (mas aqui é BR e Copa)
            params = {"league": league_id, "season": year}
            
            try:
                resp = requests.get(url, headers=headers, params=params)
                data = resp.json()
                
                # Checa erros da API
                if "errors" in data and data["errors"]:
                    print(f" ❌ Erro API: {data['errors']}")
                    break

                if not data['response']:
                    print(f" ⚠️ Sem dados.")
                    continue

                fixtures = data['response']
                count = 0
                
                for f in fixtures:
                    # Só queremos jogos que JÁ ACONTECERAM (com placar)
                    # OU jogos futuros (status NS) para guardar na base, mas o foco é treino
                    status = f['fixture']['status']['short']
                    
                    # Filtra: Só salva se tiver terminado (FT, AET, PEN) ou se for o jogo futuro (NS)
                    if status in ['FT', 'AET', 'PEN', 'NS']:
                        
                        # Quem ganhou?
                        winner = "Draw"
                        if f['teams']['home']['winner']: winner = "Home"
                        elif f['teams']['away']['winner']: winner = "Away"
                        
                        match_data = {
                            "match_id": f['fixture']['id'],
                            "league_id": league_id,
                            "league_name": league_name,
                            "season": year,
                            "date": f['fixture']['date'],
                            "round": f['league']['round'],
                            "home_team": f['teams']['home']['name'],
                            "away_team": f['teams']['away']['name'],
                            "home_goals": f['goals']['home'],
                            "away_goals": f['goals']['away'],
                            "status": status,
                            "winner": winner,
                            "venue": f['fixture']['venue']['name']
                        }
                        all_matches.append(match_data)
                        count += 1
                
                print(f" ✅ {count} jogos processados.")
                
                # Pausa para não estourar o limite da API (seja gentil com o servidor)
                time.sleep(1.5)

            except Exception as e:
                print(f" ❌ Erro fatal em {year}: {e}")

    # Salvar o CSVzão
    if all_matches:
        # Garante a pasta data/processed
        os.makedirs('data/processed', exist_ok=True)
        
        df = pd.DataFrame(all_matches)
        
        # Ordena por data para ficar bonitinho
        df = df.sort_values(by='date', ascending=False)
        
        output_path = 'data/processed/base_completa_futebol.csv'
        df.to_csv(output_path, index=False)
        
        print(f"\n💾 SUCESSO TOTAL!")
        print(f"📦 Arquivo gerado: {output_path}")
        print(f"📊 Total de jogos coletados: {len(df)}")
        print("\n🔍 Amostra dos dados:")
        print(df.head(3))
    else:
        print("\n❌ Deu ruim. Nenhum jogo foi salvo.")

if __name__ == "__main__":
    get_combined_data()