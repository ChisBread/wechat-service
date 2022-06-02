from wesdk import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python minibot.py <chat partner's nickname>")
        exit(1)
    bot = Bot()
    minibots =[
        make_shellbot(bot, sys.argv[1:]),
        make_filebot(bot, sys.argv[1:]),
        make_smartbot(bot, sys.argv[1:]),
    ]
    cobot = make_combinebot(bot, minibots)
    bot.register("recv_txt_msg",cobot)
    bot.run()