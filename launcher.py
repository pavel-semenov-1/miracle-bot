from bot import MiracleBot
import bot.conf as conf

def main():
    bot = MiracleBot()
    conf.init(bot)
    bot.run()

if __name__ == "__main__":
    main()
