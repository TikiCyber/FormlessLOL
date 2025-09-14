import json
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

def generate_html_report():
    """Generate an HTML report from analysis results"""
    
    with open('reports/analysis_results.json', 'r') as f:
        data = json.load(f)
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FormlessLoL Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #0f1419; color: #cdbe91; }
            .header { text-align: center; margin-bottom: 40px; }
            .summoner-section { margin-bottom: 40px; padding: 20px; border: 1px solid #463714; border-radius: 8px; background: #1e1e1e; }
            .metric { display: inline-block; margin: 10px; padding: 15px; background: #2d2d2d; border-radius: 5px; }
            .champion-list { display: flex; flex-wrap: wrap; gap: 10px; }
            .champion { padding: 10px; background: #3c3c3c; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎮 FormlessLoL Analysis Report</h1>
            <p>Generated on {}</p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    for summoner_name, summoner_data in data.items():
        recs = summoner_data['recommendations']
        
        html_content += f"""
        <div class="summoner-section">
            <h2>📊 {summoner_name}</h2>
            
            <div class="metric">
                <strong>Win Rate:</strong> {recs['avg_winrate']:.1%}
            </div>
            <div class="metric">
                <strong>Games Analyzed:</strong> {recs['total_games']}
            </div>
            <div class="metric">
                <strong>Best Role:</strong> {recs['best_role']}
            </div>
            
            <h3>🏆 Champion Performance</h3>
            <div class="champion-list">
        """
        
        # Add champion recommendations here
        html_content += """
            </div>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open('reports/analysis_report.html', 'w') as f:
        f.write(html_content)
    
    print("📊 HTML report generated!")

if __name__ == "__main__":
    generate_html_report()
