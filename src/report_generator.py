import json
import pandas as pd
from datetime import datetime

def generate_html_report():
    with open('reports/analysis_results.json', 'r') as f:
        data = json.load(f)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>FormlessLoL Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #0f1419; color: #cdbe91; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .summoner-section {{ margin-bottom: 40px; padding: 20px; border: 1px solid #463714; border-radius: 8px; background: #1e1e1e; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #2d2d2d; border-radius: 5px; }}
        .champion-list {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .champion {{ padding: 10px; background: #3c3c3c; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>FormlessLoL Analysis Report</h1>
        <p>Generated on {timestamp}</p>
    </div>
"""
    
    for summoner_name, summoner_data in data.items():
        recs = summoner_data['recommendations']
        avg_wr = recs['avg_winrate'] * 100
        
        html_content += f"""
    <div class="summoner-section">
        <h2>{summoner_name}</h2>
        
        <div class="metric">
            <strong>Win Rate:</strong> {avg_wr:.1f}%
        </div>
        <div class="metric">
            <strong>Games Analyzed:</strong> {recs['total_games']}
        </div>
        <div class="metric">
            <strong>Best Role:</strong> {recs['best_role']}
        </div>
        
        <h3>Champion Performance</h3>
        <div class="champion-list">
"""
        
        html_content += """
        </div>
"""

        # add AI coaching section if it exists
        coaching = summoner_data.get("ai_coaching")
        if coaching:
            # split the three sections into separate blocks
            sections = {"TREND": "", "PLAYSTYLE": "", "MENTAL GAME": ""}
            current = None
            for line in coaching.split("\n"):
                for key in sections:
                    if line.startswith(key):
                        current = key
                        line = line[len(key):].lstrip(": ")
                if current:
                    sections[current] += line + " "

            html_content += """
        <div style="margin-top: 24px;">
            <h3 style="color: #c89b3c; border-bottom: 1px solid #463714; padding-bottom: 8px;">AI Coach</h3>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
"""
            labels = {"TREND": "📈 Trend", "PLAYSTYLE": "🎮 Playstyle", "MENTAL GAME": "🧠 Mental Game"}
            for key, text in sections.items():
                if text.strip():
                    html_content += f"""
                <div style="flex: 1; min-width: 200px; background: #2d2d2d; border-left: 3px solid #c89b3c; padding: 14px; border-radius: 4px;">
                    <strong style="color: #c89b3c;">{labels[key]}</strong>
                    <p style="margin: 8px 0 0; font-size: 14px; line-height: 1.6; color: #cdbe91;">{text.strip()}</p>
                </div>
"""
            html_content += """
            </div>
        </div>
"""

        html_content += """
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    with open('reports/analysis_report.html', 'w') as f:
        f.write(html_content)
    
    print("HTML report generated")

if __name__ == "__main__":
    generate_html_report()
