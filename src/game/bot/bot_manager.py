from .bot_player import BotPlayer


class BotManager:
    def __init__(self, bot_players):
        self.bots = [BotPlayer(p) for p in bot_players]

    def update(self, app):
        actions = []
        for bot in self.bots:
            action = bot.update(app)
            if action:
                actions.append(action)
        return actions
