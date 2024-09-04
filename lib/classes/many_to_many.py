class Game:
    def __init__(self, title):
        self._title = title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title) > 0 and not hasattr(self, "title"):
            self._title = title

    def results(self):
        return [result for result in Result.all if result.game == self]

    def players(self):
        return list(set([result.player for result in self.results()]))

    def average_score(self, player):
        if player.num_times_played(self) == 0:
            return 0
        return (
            sum([result.score for result in self.results() if result.player == player])
        ) / player.num_times_played(self)


class Player:
    def __init__(self, username):
        self._username = username

    @classmethod
    def highest_scored(cls, game):
        if len(game.players()) == 0:
            return None
        high_scores = {}
        for player in game.players():
            high_scores[player] = game.average_score(player)
        return max(high_scores, key=high_scores.get)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if isinstance(username, str) and 2 <= len(username) <= 16:
            self._username = username
        # else:
        #     raise Exception

    def results(self):
        return [
            result
            for result in Result.all
            if result.player == self and isinstance(result, Result)
        ]

    def games_played(self):
        return list(
            set(
                [
                    result.game
                    for result in self.results()
                    if isinstance(result.game, Game)
                ]
            )
        )

    def played_game(self, game):
        if self in game.players():
            return True
        else:
            return False

    def num_times_played(self, game):
        return [result.player for result in game.results()].count(self)


class Result:

    all = []

    def __init__(self, player, game, score):
        self._player = player
        self._game = game
        self._score = score
        Result.all.append(self)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        if isinstance(player, Player):
            self._player = player

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, game):
        if isinstance(game, Game):
            self._game = game

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        if isinstance(score, int) and 1 <= score <= 5000 and not hasattr(self, "score"):
            self._score = score
