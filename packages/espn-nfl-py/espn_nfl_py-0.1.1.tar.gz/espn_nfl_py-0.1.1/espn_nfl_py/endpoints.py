ENDPOINTS = {
    "ODDS": {
        "PROVIDERS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/providers",
        "BET_PROVIDER": lambda BET_PROVIDER_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/providers/{BET_PROVIDER_ID}",
        "PROBABILITIES": lambda EVENT_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/probabilities?limit=200",
        "ODDS": lambda EVENT_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/odds",
        "PREDICTOR": lambda EVENT_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/predictor",
        "ATS": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/2/teams/{TEAM_ID}/ats",
        "FUTURES": lambda YEAR: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/futures",
        "H2H": lambda EVENT_ID, BET_PROVIDER_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/odds/{BET_PROVIDER_ID}/head-to-heads",
        "ODDS_RECORDS": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/0/teams/{TEAM_ID}/odds-records",
        "GAME_ODDS": lambda EVENT_ID, BET_PROVIDER_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/odds/{BET_PROVIDER_ID}/history/0/movement?limit=100",
        "QBR": lambda YEAR, WEEK_NUM: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/2/weeks/{WEEK_NUM}/qbr/10000",
        "PAST_PERFORMANCES": lambda TEAM_ID, BET_PROVIDER_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams/{TEAM_ID}/odds/{BET_PROVIDER_ID}/past-performances?limit=200"
    },
    "TEAMS": {
        "ATHLETES": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/teams/{TEAM_ID}/athletes?limit=200",
        "EVENTS": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/teams/{TEAM_ID}/events",
        "TEAMS": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
        "TEAM": lambda TEAM_ID: f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}",
        "SEASON_TEAMS": lambda YEAR: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/teams",
        "SEASON_TEAM": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/teams/{TEAM_ID}",
        "TEAM_LEADERS": "https://site.web.api.espn.com/apis/site/v3/sports/football/nfl/teamleaders",
        "SEASON_LEADERS": lambda YEAR, SEASONTYPE: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/leaders",
        "RECORD": lambda YEAR, SEASONTYPE, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/teams/{TEAM_ID}/record",
        "DEPTHCHARTS": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/teams/{TEAM_ID}/depthcharts",
        "ROSTER": lambda TEAM_ID: f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/roster",
        "DETAILED_ROSTER": lambda TEAM_ID: f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}?enable=roster,projection,stats",
        "SCHEDULE": lambda TEAM_ID, YEAR: f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{TEAM_ID}/schedule?season={YEAR}",
        "INJURIES": lambda TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams/{TEAM_ID}/injuries",
        "STATISTICS": lambda YEAR, SEASONTYPE, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/teams/{TEAM_ID}/statistics",
        "PROJECTION": lambda YEAR, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/teams/{TEAM_ID}/projection", # Not valid before 2023
        "SEASON_STANDING": lambda YEAR, SEASONTYPE, CONFERENCE_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/groups/{CONFERENCE_ID}/standings"
    },
    "GAMES": {
        "EVENTS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events",
        "EVENT": lambda EVENT_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}",
        "SUMMARY": lambda EVENT_ID: f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={EVENT_ID}",
        "PLAY_BY_PLAY": lambda EVENT_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/plays?limit=300",
        "LINESCORES": lambda EVENT_ID, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/competitors/{TEAM_ID}/linescores",
        "SCORING": lambda EVENT_ID, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/competitors/{TEAM_ID}/statistics",
        "ROSTER": lambda EVENT_ID, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/competitors/{TEAM_ID}/roster",
        "TALENT_PICKS": lambda YEAR, SEASONTYPE, WEEK_NUM: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/weeks/{WEEK_NUM}/talentpicks?limit=100",
        "WEEKLY_EVENT_IDS": lambda YEAR, SEASONTYPE, WEEK_NUM: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/weeks/{WEEK_NUM}/events",
        "OFFICIALS": lambda EVENT_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/officials",
        "POWERINDEX": lambda EVENT_ID, TEAM_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/powerindex/{TEAM_ID}" # Expected margin of victory & predicted win percentage
    },
    "ATHLETES": {
        "SPLITS": lambda ATHLETE_ID: f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{ATHLETE_ID}/splits",
        "ATHLETES": "https://sports.core.api.espn.com/v3/sports/football/nfl/athletes?limit=20000",
        "ATHLETE": lambda ATHLETE_ID: f"https://sports.core.api.espn.com/v3/sports/football/nfl/athletes/{ATHLETE_ID}",
        "EVENTLOG": lambda YEAR, ATHLETE_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/athletes/{ATHLETE_ID}/eventlog",
        "EVENT_STATS": lambda EVENT_ID, TEAM_ID, ATHLETE_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/{EVENT_ID}/competitions/{EVENT_ID}/competitors/{TEAM_ID}/roster/{ATHLETE_ID}/statistics/0",
        "LEADERS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/leaders",
        "TALENT_PICKS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/talentpicks",
        "GAMELOG": lambda ATHLETE_ID: f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{ATHLETE_ID}/gamelog",
        "COACHES": lambda YEAR: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/coaches?limit=50",
        "STATISTICS_LOG": lambda ATHLETE_ID: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{ATHLETE_ID}/statisticslog",
        "OVERVIEW": lambda ATHLETE_ID: f"https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{ATHLETE_ID}/overview",
        "FREE_AGENTS": lambda YEAR: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/freeagents",
        "DRAFT": lambda YEAR: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/draft"
    },
    "CALENDAR": {
        "ONDAYS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/calendar/ondays",
        "OFFDAYS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/calendar/offdays",
        "BLACKLIST": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/calendar/blacklist",
        "WHITELIST": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/calendar/whitelist",
        "WEEKS": lambda YEAR, SEASONTYPE: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/weeks",
        "WEEK_INFO": lambda YEAR, SEASONTYPE, WEEKNUM: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/weeks/{WEEKNUM}",
        "SEASON": lambda YEAR: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}"
    },
    "SCOREBOARD": {
        "TRANSACTIONS": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/transactions",
        "GROUPS": lambda YEAR, SEASONTYPE: f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/{YEAR}/types/{SEASONTYPE}/groups",
        "FRANCHISES": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/franchises",
        "HEADER": "https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=nfl"
    }
}