#!/home/cees/.virtualenvs/ceasaro_py/bin/python
# coding=utf-8
import sys
import argparse
from copy import deepcopy

__version__ = '0.1'


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--teams', type=int, default=3, help="Number of teams in group")
    parser.add_argument('-pw', '--points_win', type=int, default=3, help="Points if a team wins a match")
    parser.add_argument('-pd', '--points_draw', type=int, default=1, help="Points if teams draw a match")
    parser.add_argument('-pl', '--points_loss', type=int, default=0, help="Points if a team losses a match")
    return parser


class CompetitionResult(object):

    def __init__(self, points_win, points_draw, points_loss):
        self.points_win = points_win
        self.points_draw = points_draw
        self.points_loss = points_loss
        self.matches = []

    def add_match(self, match_result):
        self.matches.append(match_result)

    def points_per_team(self):
        team_points = {}
        for m in self.matches:
            if m.team_1 not in team_points.keys():
                team_points[m.team_1] = 0
            if m.team_2 not in team_points.keys():
                team_points[m.team_2] = 0
            if m.team_1 == m.winner:
                team_points[m.team_1] += self.points_win
            elif m.team_2 == m.winner:
                team_points[m.team_2] += self.points_win
            else:
                team_points[m.team_1] += self.points_draw
                team_points[m.team_2] += self.points_draw
        return team_points

    def clone(self):
        return deepcopy(self)

    def __repr__(self):
        return f"Competition ({len(self.matches)} matches)"


class MatchResult(object):

    def __init__(self, team_1, team_2, winner=None):
        self.team_1 = team_1
        self.team_2 = team_2
        self.winner = winner

    def __repr__(self):
        return f"{self.team_1} - {self.team_2} = {self.winner}"


def sim_competition(args):
    teams = range(args.teams)
    results = [CompetitionResult(args.points_win, args.points_draw, args.points_loss)]
    for team in teams:
        for opponent in [t for t in teams if t != team]:
            draw_results = [r.clone() for r in results]
            lose_results = [r.clone() for r in results]
            # WIN
            for win_result in results:
                win_result.add_match(MatchResult(team, opponent, winner=team))

            # DRAW
            for draw_result in draw_results:
                draw_result.add_match(MatchResult(team, opponent))
            results += draw_results

            # LOSE
            for lose_result in lose_results:
                lose_result.add_match(MatchResult(team, opponent, winner=opponent))
            results += lose_results
    return results


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    results = sim_competition(args)
    for r in results:
        print(r)
        print("points:")
        print(f"    {r.points_per_team()}")


if __name__ == '__main__':
    sys.exit(main())

