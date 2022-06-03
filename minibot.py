from wesdk import *
def hippopbot(bot, msg):
    bot.send_msg('yo',msg['senderid'],msg['roomid'],msg['nickname'])
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
    combinebot = load_bots(sys.argv[1], updates)
    if not combinebot:
        print("config parse error.")
        exit(1)
    bot.register("recv_txt_msg",lambda msg: combinebot(bot, msg))
    bot.run()
