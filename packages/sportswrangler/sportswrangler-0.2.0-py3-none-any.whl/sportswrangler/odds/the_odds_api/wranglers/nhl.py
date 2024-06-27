from typing import Literal

from sportswrangler.odds.the_odds_api.utils.classes import NHLKeyMapping
from sportswrangler.odds.the_odds_api.wranglers.base import TheOddsApiWrangler
from sportswrangler.utils.enums import Sport


class TheOddsOddsApiNHLWrangler(TheOddsApiWrangler):
    sport: Sport = Sport.NHL
    _player_prop_markets: list[
        Literal[
            "player_goal_scorer_anytime",
            "player_points",
            "player_assists",
            "player_shots_on_goal",
            "player_total_saves",
            "player_blocked_shots",
            "player_power_play_points",
            "player_goal_scorer_first",
            "player_goal_scorer_last",
        ]
    ] = [
        "player_goal_scorer_anytime",
        "player_points",
        "player_assists",
        "player_shots_on_goal",
        "player_total_saves",
        "player_blocked_shots",
        "player_power_play_points",
        "player_goal_scorer_first",
        "player_goal_scorer_last",
    ]
    _player_prop_key_mapping: NHLKeyMapping = {
        "player_goal_scorer_anytime": "G",
        "player_points": "PTS",
        "player_assists": "AST",
        "player_shots_on_goal": "S",
        "player_total_saves": "SV",
        "player_blocked_shots": "BLK",
        "player_power_play_points": "PPP",
        "player_goal_scorer_first": "FG",
        "player_goal_scorer_last": "LG",
    }
