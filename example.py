from wesdk import *
if __name__ == "__main__":
    bot = Bot()
    if len(sys.argv) > 1:
        print(json.dumps(eval('bot.'+sys.argv[1]), ensure_ascii=False))
        exit(0)
    bot.register("on_open", lambda ws: logging("Connecting to WeChat service .."))
    bot.register("on_close", lambda ws: logging("Byebye~"))
    bot.run()