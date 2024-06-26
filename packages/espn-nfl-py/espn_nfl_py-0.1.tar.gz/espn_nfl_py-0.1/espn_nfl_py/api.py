import requests
from .endpoints import ENDPOINTS
from .exceptions import APIError

def _get(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise APIError(f"API request failed with status {response.status_code}")
        return response.json()

class ESPNAPI:
    def get_athlete(athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["ATHLETE"](athlete_id))
        
    def get_event(event_id):
        return _get(ENDPOINTS["GAMES"]["EVENT"](event_id))
    
    def get_events():
        return _get(ENDPOINTS["GAMES"]["EVENTS"])
    
    def get_bet_provider(bet_provider_id):
        return _get(ENDPOINTS["ODDS"]["BET_PROVIDER"](bet_provider_id))
    
    def get_providers():
        return _get(ENDPOINTS["ODDS"]["PROVIDERS"])

    def get_probabilities(event_id):
        return _get(ENDPOINTS["ODDS"]["PROBABILITIES"](event_id))

    def get_odds(event_id):
        return _get(ENDPOINTS["ODDS"]["ODDS"](event_id))

    def get_predictor(event_id):
        return _get(ENDPOINTS["ODDS"]["PREDICTOR"](event_id))

    def get_ats(year, team_id):
        return _get(ENDPOINTS["ODDS"]["ATS"](year, team_id))

    def get_futures(year):
        return _get(ENDPOINTS["ODDS"]["FUTURES"](year))

    def get_h2h(event_id, bet_provider_id):
        return _get(ENDPOINTS["ODDS"]["H2H"](event_id, bet_provider_id))

    def get_odds_records(year, team_id):
        return _get(ENDPOINTS["ODDS"]["ODDS_RECORDS"](year, team_id))

    def get_game_odds(event_id, bet_provider_id):
        return _get(ENDPOINTS["ODDS"]["GAME_ODDS"](event_id, bet_provider_id))

    def get_qbr(year, week_num):
        return _get(ENDPOINTS["ODDS"]["QBR"](year, week_num))

    def get_past_performances(team_id, bet_provider_id):
        return _get(ENDPOINTS["ODDS"]["PAST_PERFORMANCES"](team_id, bet_provider_id))

    def get_athletes(year, team_id):
        return _get(ENDPOINTS["TEAMS"]["ATHLETES"](year, team_id))

    def get_team_events(year, team_id):
        return _get(ENDPOINTS["TEAMS"]["EVENTS"](year, team_id))

    def get_teams():
        return _get(ENDPOINTS["TEAMS"]["TEAMS"])

    def get_team(team_id):
        return _get(ENDPOINTS["TEAMS"]["TEAM"](team_id))

    def get_season_teams(year):
        return _get(ENDPOINTS["TEAMS"]["SEASON_TEAMS"](year))

    def get_season_team(year, team_id):
        return _get(ENDPOINTS["TEAMS"]["SEASON_TEAM"](year, team_id))

    def get_season_leaders(year, season_type):
        return _get(ENDPOINTS["TEAMS"]["SEASON_LEADERS"](year, season_type))

    def get_record(year, season_type, team_id):
        return _get(ENDPOINTS["TEAMS"]["RECORD"](year, season_type, team_id))

    def get_depthcharts(year, team_id):
        return _get(ENDPOINTS["TEAMS"]["DEPTHCHARTS"](year, team_id))

    def get_roster(team_id):
        return _get(ENDPOINTS["TEAMS"]["ROSTER"](team_id))

    def get_detailed_roster(team_id):
        return _get(ENDPOINTS["TEAMS"]["DETAILED_ROSTER"](team_id))

    def get_schedule(team_id, year):
        return _get(ENDPOINTS["TEAMS"]["SCHEDULE"](team_id, year))

    def get_injuries(team_id):
        return _get(ENDPOINTS["TEAMS"]["INJURIES"](team_id))

    def get_statistics(year, season_type, team_id):
        return _get(ENDPOINTS["TEAMS"]["STATISTICS"](year, season_type, team_id))

    def get_projection(year, team_id):
        return _get(ENDPOINTS["TEAMS"]["PROJECTION"](year, team_id))

    def get_season_standing(year, season_type, conference_id):
        return _get(ENDPOINTS["TEAMS"]["SEASON_STANDING"](year, season_type, conference_id))

    def get_game_summary(event_id):
        return _get(ENDPOINTS["GAMES"]["SUMMARY"](event_id))

    def get_play_by_play(event_id):
        return _get(ENDPOINTS["GAMES"]["PLAY_BY_PLAY"](event_id))

    def get_linescores(event_id, team_id):
        return _get(ENDPOINTS["GAMES"]["LINESCORES"](event_id, team_id))

    def get_scoring(event_id, team_id):
        return _get(ENDPOINTS["GAMES"]["SCORING"](event_id, team_id))

    def get_game_roster(event_id, team_id):
        return _get(ENDPOINTS["GAMES"]["ROSTER"](event_id, team_id))

    def get_talent_picks(year, season_type, week_num):
        return _get(ENDPOINTS["GAMES"]["TALENT_PICKS"](year, season_type, week_num))

    def get_weekly_event_ids(year, season_type, week_num):
        return _get(ENDPOINTS["GAMES"]["WEEKLY_EVENT_IDS"](year, season_type, week_num))

    def get_officials(event_id):
        return _get(ENDPOINTS["GAMES"]["OFFICIALS"](event_id))

    def get_powerindex(event_id, team_id):
        return _get(ENDPOINTS["GAMES"]["POWERINDEX"](event_id, team_id))

    def get_athlete_splits(athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["SPLITS"](athlete_id))

    def get_athletes_list():
        return _get(ENDPOINTS["ATHLETES"]["ATHLETES"])

    def get_athlete_eventlog(year, athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["EVENTLOG"](year, athlete_id))

    def get_athlete_event_stats(event_id, team_id, athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["EVENT_STATS"](event_id, team_id, athlete_id))

    def get_leaders():
        return _get(ENDPOINTS["ATHLETES"]["LEADERS"])

    def get_talent_picks_athlete():
        return _get(ENDPOINTS["ATHLETES"]["TALENT_PICKS"])

    def get_athlete_gamelog(athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["GAMELOG"](athlete_id))

    def get_coaches(year):
        return _get(ENDPOINTS["ATHLETES"]["COACHES"](year))

    def get_statistics_log(athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["STATISTICS_LOG"](athlete_id))

    def get_athlete_overview(athlete_id):
        return _get(ENDPOINTS["ATHLETES"]["OVERVIEW"](athlete_id))

    def get_free_agents(year):
        return _get(ENDPOINTS["ATHLETES"]["FREE_AGENTS"](year))

    def get_draft(year):
        return _get(ENDPOINTS["ATHLETES"]["DRAFT"](year))

    def get_ondays():
        return _get(ENDPOINTS["CALENDAR"]["ONDAYS"])

    def get_offdays():
        return _get(ENDPOINTS["CALENDAR"]["OFFDAYS"])

    def get_blacklist():
        return _get(ENDPOINTS["CALENDAR"]["BLACKLIST"])

    def get_whitelist():
        return _get(ENDPOINTS["CALENDAR"]["WHITELIST"])

    def get_weeks(year, season_type):
        return _get(ENDPOINTS["CALENDAR"]["WEEKS"](year, season_type))

    def get_week_info(year, season_type, week_num):
        return _get(ENDPOINTS["CALENDAR"]["WEEK_INFO"](year, season_type, week_num))

    def get_season(year):
        return _get(ENDPOINTS["CALENDAR"]["SEASON"](year))

    def get_transactions():
        return _get(ENDPOINTS["SCOREBOARD"]["TRANSACTIONS"])

    def get_groups(year, season_type):
        return _get(ENDPOINTS["SCOREBOARD"]["GROUPS"](year, season_type))

    def get_franchises():
        return _get(ENDPOINTS["SCOREBOARD"]["FRANCHISES"])

    def get_header():
        return _get(ENDPOINTS["SCOREBOARD"]["HEADER"])
    
    def get_team_leaders():
        return _get(ENDPOINTS["TEAMS"]["TEAM_LEADERS"])
