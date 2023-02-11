class BotObjectHolder:
    bot = None

    @staticmethod
    def get_bot():
        return BotObjectHolder.bot

    @staticmethod
    def set_bot(bot):
        BotObjectHolder.bot = bot