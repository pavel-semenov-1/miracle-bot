from bot import MiracleBot
import bot.conf as conf

def main():
    conf.init()
    bot = MiracleBot()
    bot.run()

if __name__ == "__main__":
    main()
