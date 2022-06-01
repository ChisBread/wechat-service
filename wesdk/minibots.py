import os
def make_combinebot(bot, minibots):
    def retbot(msg):
        for mbot in minibots:
            if mbot(msg):
                break
    return retbot
    
def make_shellbot(bot, adnicks):
    def retbot(msg):
        if not msg['content'].startswith('/sh.exec'):
            return False
        if '@chatroom' in msg['wxid']:
            roomid = msg['wxid'] #群id
            senderid = msg['id1'] #个人id
        else:
            roomid = None
            nickname = 'null'
            senderid = msg['wxid'] #个人id
        fromnick = bot.get_chatroom_member_nick(roomid, senderid)['content']['nick']
        if fromnick not in adnicks:
            return False
        reply = ''
        command = msg['content'][len('/sh.exec'):]
        p = os.popen(command,"r")
        while 1:
            line = p.readline()
            if not line: break
            reply+=line
        bot.send_msg(reply, msg['wxid'])
        return True
    return retbot
    
def make_smartbot(bot, chatnicks):
    def retbot(msg):
        if  msg['content'][-1] not in ['？', '?', '吗'] \
            and '是不是' not in msg['content']:
            return False
        if '@chatroom' in msg['wxid']:
            roomid = msg['wxid'] #群id
            senderid = msg['id1'] #个人id
        else:
            roomid = None
            nickname = 'null'
            senderid = msg['wxid'] #个人id
        fromnick = bot.get_chatroom_member_nick(roomid, senderid)['content']['nick']
        if fromnick not in chatnicks:
            return False
        reply = msg['content']
        reply = reply.replace('是不是', '是')
        reply = reply.replace('？', '!')
        reply = reply.replace('?', '!')
        reply = reply.replace('吗', '')
        reply = reply.replace('你', '__PH_YOU__')
        reply = reply.replace('我', '你')
        reply = reply.replace('__PH_YOU__', '我')
        if not reply:
            return False
        bot.send_msg(reply, roomid=roomid,wxid=senderid,nickname=fromnick)
        return True
    return retbot