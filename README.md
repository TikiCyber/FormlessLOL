# FormlessLOL - League of Legends Analytics

Automated League of Legends performance analysis using GitHub Actions.

## Setup

Riot recently overhauled their API system so please generate your key here: https://developer.riotgames.com/

1. Log in with your Riot account
2. Generate a new development API key
3. Add it to your GitHub repo secrets as `RIOT_API_KEY`

## Latest Analysis Results

---
Last updated: 2025-10-09 04:28:01 UTC

## How it works

Runs daily via GitHub Actions to fetch match history from Riot Games API, calculate win rates and KDA stats, then generate reports.

## View Reports
- [Latest HTML Report](./reports/analysis_report.html)
- [Raw JSON Data](./reports/analysis_results.json)
