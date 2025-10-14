# FormlessLoL

Tracking my League matches because porofessor and blitz don't really give me what I want

## Why im making this

Started this to help me climb to GM all these apps compare you with koreans and pro's which don't really help you improve. Wanted to refference recent games instead of looking at my winrate for 200+ games to track my real time progress.

## How it works

Uses GitHub Actions to pull my match history from Riot's API every day. It calculates my win rates, KDA, and breaks down performance by role. Then it just dumps everything into a report so I can see where I'm actually improving (or not).

The workflow runs at like 6am so the data is usually fresh by the time I check it.

## What it shows

- Win rates by champion
- KDA trends
- Role performance breakdown  
- Which champs I should probably stop playing
- Match history with actual stats

## Setup

You'll need:
- Riot API key (get it from their developer portal)
- Your summoner name and region
- GitHub account for Actions

Add your API key and summoner info to GitHub secrets:
- `RIOT_API_KEY`
- `SUMMONER_NAME`  
- `REGION`

The action runs automatically but you can trigger it manually from the Actions tab.

## Files

- `reports/analysis_report.html` - Latest stats in readable format
- `reports/analysis_results.json` - Raw data if you want to do your own analysis
- `.github/workflows/analyze.yml` - The automation script

## Stuff I learned

- GitHub Actions are actually pretty useful
- I play way too much when I should be studying (I swear I can still work recruiter)
- My Talon is actually pretty clean (2.5 kp)
- Sometimes seeing the numbers makes you realize you need to dodge certain matchups

## Known issues

- Sometimes the API rate limits if I manually trigger it too much
- Report formatting could be better on mobile
- Doesn't track normal games, only ranked
- Lowkey could add sums and port some stuff over from OPGG really

---

Just a personal project to settle arguments and actually improve at the game. Code's pretty rough but it works.
