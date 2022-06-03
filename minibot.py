from wesdk import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python config.py <path of config.yaml> <>")
        exit(1)
    updates = {
        "chat-rules":{
            "admin":{
                "nickname":sys.argv[2:]
            }
        }
    }
    bot = Bot()
    retbots = loadbots(sys.argv[1], updates)
    if not retbots:
        print("config parse error.")
        exit(1)
    cobot = minibots.make_combinebot(retbots)
    bot.register("recv_txt_msg",lambda msg: cobot(bot, msg))
    bot.run()
