import requests
import os
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

API_KEY = os.getenv("FOOTBALL_API_KEY")
headers = {"x-apisports-key": API_KEY}
base_url = "https://v3.football.api-sports.io"

def check_league_coverage():
    print("🕵️ Investigando a cobertura da Liga 73 (Copa do Brasil)...")
    
    # Vamos pegar os detalhes da liga pelo ID
    url = f"{base_url}/leagues"
    params = {"id": "73"} # ID que descobrimos antes
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if not data['response']:
            print("❌ A API não retornou nada para o ID 73. O ID pode estar errado.")
            return

        league_data = data['response'][0]
        league_name = league_data['league']['name']
        country = league_data['country']['name']
        seasons = league_data['seasons']
        
        print(f"✅ Liga Encontrada: {league_name} ({country})")
        print("\n📅 TEMPORADAS DISPONÍVEIS NA SUA CONTA:")
        
        for season in seasons:
            year = season['year']
            start = season['start']
            end = season['end']
            is_current = season['current']
            # Verifica se tem cobertura de jogos (fixtures)
            has_fixtures = season['coverage']['fixtures']['events']
            
            status_icon = "🟢" if is_current else "⚪"
            fixtures_icon = "⚽ Sim" if has_fixtures else "❌ Não"
            
            print(f"{status_icon} Ano: {year} | Início: {start} -> Fim: {end} | Jogos: {fixtures_icon}")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    check_league_coverage()