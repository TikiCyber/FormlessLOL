import json
from datetime import datetime

def update_readme():
    """Update README with latest analysis results"""
    
    try:
        with open('reports/analysis_results.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No analysis results found")
        return
    
    readme_content = """# 🎮 FormlessLoL - League of Legends Analytics

Automated League of Legends performance analysis using GitHub Actions.

## 📊 Latest Analysis Results

"""
    
    for summoner_name, summoner_data in data.items():
        recs = summoner_data['recommendations']
        
        readme_content += f"""
### {summoner_name}
- **Win Rate:** {recs['avg_winrate']:.1%}
- **Games Analyzed:** {recs['total_games']}
- **Best Role:** {recs.get('best_role', 'N/A')}

"""
    
    readme_content += f"""
---
*Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC*

## 🚀 How it works

1. **Scheduled Analysis:** Runs daily via GitHub Actions
2. **Data Collection:** Fetches match history from Riot Games API
3. **Performance Analysis:** Calculates win rates, KDA, and role performance
4. **Recommendations:** Suggests optimal champions and playstyles
5. **Reporting:** Generates HTML reports and updates this README

## 📁 View Reports
- [Latest HTML Report](./reports/analysis_report.html)
- [Raw JSON Data](./reports/analysis_results.json)
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("📝 README updated!")

if __name__ == "__main__":
    update_readme()
