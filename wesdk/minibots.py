import os
import wesdk.query as query
import requests
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
# make_weatherbot 感谢sojson提供的免费接口
## citycode见: https://github.com/baichengzhou/weather.api/blob/master/src/main/resources/citycode-2019-08-23.json
def make_weatherbot(citycode='101010100'):
    def retbot(bot, msg):
        weather = requests.get('http://t.weather.sojson.com/api/weather/city/'+citycode).json()
        reply = "\n%s\n"%weather['cityInfo']['city']
        reply += "今日天气:\n    湿度:%s 空气污染:%s 气温:%s\n"%tuple([weather['data'].get(key, '未知') for key in ['shidu', 'quality', 'wendu']])
        reply += "明日天气:\n    %s~%s %s"%tuple([weather['data']['forecast'][0].get(key, '未知') for key in ['low', 'high', 'type']])
        bot.send_msg(reply, wxid=msg['senderid'],roomid=msg['roomid'],nickname=msg['nickname'])
    return retbot
def make_combinebot(minibots):
    def retbot(bot, msg):
        for mbot in minibots:
            if mbot(bot, msg):
                break
    return retbot
