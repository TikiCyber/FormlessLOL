# FormlessLoL

A League of Legends analytics tool that pulls your match history through the Riot API, runs performance analysis, and uses AI to give you actual coaching feedback — not just your win rate.

Built this because I wanted something that could tell me *why* I was losing, not just that I was.

## What it does

Pulls your last 20 ranked games and breaks down:
- Win rate trends over time
- KDA and CS averages by champion and role
- Best performing role
- AI-generated coaching based on your actual stats — covers your playstyle, win rate patterns, and whether your mental is holding up

The analysis runs automatically every day through GitHub Actions and updates the report without you touching anything.

## Latest Results

### TikiCyber
- **Win Rate:** 50.0%
- **Games:** 20
- **Best Role:** TOP

*Last updated: 2026-02-20 05:05:39 UTC*

[View full report](./reports/analysis_report.html) | [Raw data](./reports/analysis_results.json)

## How it works

1. GitHub Actions triggers the pipeline daily
2. Pulls match history from the Riot Games API
3. Runs stats analysis with pandas
4. Feeds the results to Claude (Anthropic API) to generate personalized coaching
5. Builds an HTML report and commits everything back to the repo

## Setup

You'll need two API keys stored as GitHub secrets:

```
RIOT_API_KEY
ANTHROPIC_API_KEY
```

Get your Riot key at [developer.riotgames.com](https://developer.riotgames.com) and your Anthropic key at [console.anthropic.com](https://console.anthropic.com).

Then add your account to `config/summoners.json`:

```json
{
  "summoners": [
    {
      "riot_id": "YourName",
      "tagline": "NA1",
      "region": "na1"
    }
  ]
}
```

Push the change and the pipeline runs automatically.

## Stack

Python, Riot Games API, Anthropic API, GitHub Actions, pandas
