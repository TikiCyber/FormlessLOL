import os
import json
import requests
import time
from datetime import datetime
import pandas as pd

class LoLAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('RIOT_API_KEY')
        self.base_url = "https://{}.api.riotgames.com"
        self.headers = {"X-Riot-Token": self.api_key}
        
    def get_summoner_by_riot_id(self, riot_id, tagline, region):
        """Get summoner info by Riot ID"""
        url = f"{self.base_url.format('americas')}/riot/account/v1/accounts/by-riot-id/{riot_id}/{tagline}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            account_data = response.json()
            # Get summoner data
            summoner_url = f"{self.base_url.format(region)}/lol/summoner/v4/summoners/by-puuid/{account_data['puuid']}"
            summoner_response = requests.get(summoner_url, headers=self.headers)
            return summoner_response.json() if summoner_response.status_code == 200 else None
        return None
        
    def get_match_history(self, puuid, region, count=20):
        """Get recent match history"""
        url = f"{self.base_url.format('americas')}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {'count': count, 'type': 'ranked'}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else []
        
    def analyze_matches(self, match_ids, puuid):
        """Analyze match details for performance metrics"""
        match_data = []
        
        for match_id in match_ids:
            url = f"{self.base_url.format('americas')}/lol/match/v5/matches/{match_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                match_info = response.json()
                player_data = None
                
                # Find player's data in the match
                for participant in match_info['info']['participants']:
                    if participant['puuid'] == puuid:
                        player_data = participant
                        break
                        
                if player_data:
                    match_data.append({
                        'match_id': match_id,
                        'champion': player_data['championName'],
                        'role': player_data['teamPosition'],
                        'win': player_data['win'],
                        'kills': player_data['kills'],
                        'deaths': player_data['deaths'],
                        'assists': player_data['assists'],
                        'cs': player_data['totalMinionsKilled'],
                        'damage': player_data['totalDamageDealtToChampions'],
                        'game_duration': match_info['info']['gameDuration']
                    })
            
            time.sleep(1)  # Rate limiting
            
        return pd.DataFrame(match_data)
        
    def generate_recommendations(self, df):
        """Generate champion and playstyle recommendations"""
        if df.empty:
            return {}
            
        # Win rate by champion
        champion_stats = df.groupby('champion').agg({
            'win': ['count', 'sum', 'mean'],
            'kills': 'mean',
            'deaths': 'mean',
            'assists': 'mean'
        }).round(2)
        
        # Recommendations
        recommendations = {
            'top_champions': champion_stats.head(5).to_dict(),
            'avg_winrate': df['win'].mean(),
            'best_role': df.groupby('role')['win'].mean().idxmax(),
            'total_games': len(df),
            'timestamp': datetime.now().isoformat()
        }
        
        return recommendations

def main():
    analyzer = LoLAnalyzer()
    
    # Load configuration
    with open('config/summoners.json', 'r') as f:
        config = json.load(f)
    
    results = {}
    
    for summoner_config in config['summoners']:
        print(f"Analyzing {summoner_config['riot_id']}...")
        
        # Get summoner info
        summoner = analyzer.get_summoner_by_riot_id(
            summoner_config['riot_id'],
            summoner_config['tagline'],
            summoner_config['region']
        )
        
        if summoner:
            # Get match history
            match_ids = analyzer.get_match_history(
                summoner['puuid'], 
                summoner_config['region'],
                config['analysis_settings']['match_count']
            )
            
            # Analyze matches
            df = analyzer.analyze_matches(match_ids, summoner['puuid'])
            
            # Generate recommendations
            recommendations = analyzer.generate_recommendations(df)
            
            results[summoner_config['riot_id']] = {
                'summoner_info': summoner,
                'recommendations': recommendations,
                'match_data': df.to_dict('records')
            }
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✅ Analysis complete!")

if __name__ == "__main__":
    main()
