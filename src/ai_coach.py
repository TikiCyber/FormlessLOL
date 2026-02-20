import os
import json
import anthropic

# using claude to generate coaching insights based on match data
# plugs into the existing analysis pipeline after lol_analyzer.py runs

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def build_prompt(summoner_name, match_data, recommendations):
    """turn the match data into something useful for the AI"""

    total_games = len(match_data)
    wins = sum(1 for m in match_data if m.get("win"))
    losses = total_games - wins
    winrate = round((wins / total_games) * 100, 1) if total_games > 0 else 0

    # figure out if they're on a streak
    streak = 0
    streak_type = None
    for match in match_data:
        result = match.get("win")
        if streak_type is None:
            streak_type = result
            streak = 1
        elif result == streak_type:
            streak += 1
        else:
            break

    streak_str = f"{streak} game {'win' if streak_type else 'loss'} streak" if streak >= 2 else "no current streak"

    # recent 5 games for trend
    recent = match_data[:5]
    recent_wins = sum(1 for m in recent if m.get("win"))
    recent_summary = f"{recent_wins}/5 wins in last 5 games"

    # average stats
    avg_kills = round(sum(m.get("kills", 0) for m in match_data) / total_games, 1)
    avg_deaths = round(sum(m.get("deaths", 0) for m in match_data) / total_games, 1)
    avg_assists = round(sum(m.get("assists", 0) for m in match_data) / total_games, 1)
    avg_cs = round(sum(m.get("cs", 0) for m in match_data) / total_games, 1)

    best_role = recommendations.get("best_role", "unknown")

    prompt = f"""You are a League of Legends coach reviewing a player's recent performance. Give honest, specific feedback — not generic advice.

Player: {summoner_name}
Last {total_games} ranked games: {wins}W {losses}L ({winrate}% winrate)
Recent form: {recent_summary}
Current streak: {streak_str}
Average stats: {avg_kills}/{avg_deaths}/{avg_assists} KDA, {avg_cs} CS per game
Best performing role: {best_role}

Give me 3 things:

1. TREND - What does their win rate pattern tell you? Are they improving, declining, or inconsistent? Be specific.

2. PLAYSTYLE - Based on their KDA and CS numbers, what kind of player are they? (passive, aggressive, farming-focused, etc). What's one thing they should change?

3. MENTAL GAME - Based on their streaks and consistency, how is their mental holding up? Any tilt risk? One practical tip.

Keep it under 200 words total. Talk directly to the player. No bullet points, just three short paragraphs labeled TREND, PLAYSTYLE, and MENTAL GAME."""

    return prompt


def get_ai_coaching(summoner_name, match_data, recommendations):
    """call claude and get back coaching text"""

    if not match_data:
        return None

    prompt = build_prompt(summoner_name, match_data, recommendations)

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except Exception as e:
        print(f"AI coaching failed for {summoner_name}: {e}")
        return None


def run_ai_coaching(results_path="reports/analysis_results.json"):
    """load existing results, add AI insights, save back"""

    with open(results_path, "r") as f:
        data = json.load(f)

    for summoner_name, summoner_data in data.items():
        print(f"Getting AI coaching for {summoner_name}...")

        match_data = summoner_data.get("match_data", [])
        recommendations = summoner_data.get("recommendations", {})

        coaching = get_ai_coaching(summoner_name, match_data, recommendations)

        if coaching:
            summoner_data["ai_coaching"] = coaching
            print(f"  done")
        else:
            print(f"  skipped (no data or API error)")

    # save back with AI insights added
    with open(results_path, "w") as f:
        json.dump(data, f, indent=2)

    print("AI coaching complete")


if __name__ == "__main__":
    run_ai_coaching()
