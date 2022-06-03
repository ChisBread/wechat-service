import os
import wesdk.query as query

def filebot(bot, msg):
    file = msg['content']
    force_type = query.ATTATCH_FILE
    lfile = file.lower()
    if lfile.endswith('.jpg') or lfile.endswith('.jpeg') or lfile.endswith('.png'):
        force_type = query.PIC_MSG
    bot.send_msg(file, wxid=msg['senderid'],roomid=msg['roomid'],nickname=msg['nickname'], force_type=force_type)

def shellbot(bot, msg):
    reply = '\n'
    p = os.popen(msg['content'],"r")
    while 1:
        line = p.readline()
        if not line: break
        reply+=line
    bot.send_msg(reply, wxid=msg['senderid'],roomid=msg['roomid'],nickname=msg['nickname'])

def smartbot(bot, msg):
    reply = msg['content']
    reply = reply.replace('是不是', '是')
    reply = reply.replace('？', '!')
    reply = reply.replace('?', '!')
    reply = reply.replace('吗', '')
    reply = reply.replace('你', '__PH_YOU__')
    reply = reply.replace('我', '你')
    reply = reply.replace('__PH_YOU__', '我')
    bot.send_msg(reply, wxid=msg['senderid'],roomid=msg['roomid'],nickname=msg['nickname'])

def make_combinebot(minibots):
    def retbot(bot, msg):
        for mbot in minibots:
            if mbot(bot, msg):
                break
    return retbot
