from wesdk import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python minibot.py <chat partner's nickname>")
        exit(1)
    bot = Bot()
    cobot = make_combinebot(bot, [make_shellbot(bot, sys.argv[1:]), make_smartbot(bot, sys.argv[1:])])
    bot.register("recv_txt_msg",cobot)
    bot.run()