
class SessionStats:
    def __init__(self):
        self.rounds_played = 0
        self.rounds_won = 0
        self.best_streak = 0

    def record_round(self, won, current_streak):
        self.rounds_played += 1

        if won:
            self.rounds_won += 1
            self.best_streak = max(
                self.best_streak,
                current_streak
            )
