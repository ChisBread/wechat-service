# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import websocket
import threading
import time
import json
import requests
import os
import sys
import query
websocket._logging._logger.level = -99
def logging(msg):
    now=time.strftime("%Y-%m-%d %X")
    print(f'[{now}]:{msg}')

class Bot(threading.Thread):
    handle_register = {}
    contact_list = {}
    def __init__(self, ip='127.0.0.1', port=5555):
        threading.Thread.__init__(self)
        self.IP = ip
        self.PORT = port
        self.SERVER=f'ws://{ip}:{port}'
        self.ws = websocket.WebSocketApp(self.SERVER, \
            on_open=self.make_on_open(), \
            on_message=self.make_on_message(), \
            on_error=self.make_on_error(), \
            on_close=self.make_on_close())
    def register(self, handle_name, foo):
        self.handle_register[handle_name] = foo
    ########## HTTP API 样例 ##########
    # 发送http请求到hook端
    def __send_http(self, uri, data):
        if isinstance(data, str) or isinstance(data, bytes):
            data = json.loads(data)
        base_data={
            'id':query.uuid(),
            'type':'null',
            'roomid':'null',
            'wxid':'null',
            'content':'null',
            'nickname':'null',
            'ext':'null',
        }
        base_data.update(data)
        url = f'http://{self.IP}:{self.PORT}/{uri}'
        print(base_data)
        rsp = requests.post(url,json={'para':base_data},timeout=5)
        return rsp.json()
    ################## 发送消息 ##################
    def send_msg(self, msg, wxid='null', roomid='null', nickname='null', force_type=None):
        uri = '/api/sendtxtmsg'
        return json.loads(self.__send_http(uri, query.send_msg(msg, wxid, roomid, nickname, force_type)))
    ################## 个人信息 ##################
    # get_personal_info 获取登陆账号的个人信息
    def get_personal_info(self):
        uri = '/api/get_personal_info'
        return self.__send_http(uri, query.get_personal_info())
    # get_personal_detail 获取指定wxid的个人信息
    def get_personal_detail(self, wxid):
        uri = '/api/get_personal_detail'
        return self.__send_http(uri, query.get_personal_detail(wxid))
    # get_user_nick 获取指定wxid的昵称
    def get_user_nick(self, wxid):
        uri='api/getmembernick'
        return json.loads(self.__send_http(uri, query.get_user_nick(wxid)))
    # get_contact_list 获取联系人(wxid和roomid)
    # 似乎不能用
    def get_contact_list(self):
        uri='/api/getcontactlist'
        return json.loads(self.__send_http(uri, query.get_contact_list()))
    ################## 群聊信息 ##################
    # get_chatroom_member 获取指定群的成员
    def get_chatroom_member(self, roomid):
        uri='/api/get_charroom_member_list'
        return json.loads(self.__send_http(uri, query.get_chatroom_member(roomid)))
    # get_chatroom_member_nick 获取群聊成员昵称, 或微信好友的昵称(只填wxid时)
    def get_chatroom_member_nick(self, roomid='null', wxid='ROOT'):
        # 获取指定群的成员的昵称 或 微信好友的昵称
        uri='api/getmembernick'
        return json.loads(self.__send_http(uri, query.get_chatroom_member_nick(roomid, wxid)))

    
    ########## Message Handle ##########
    # 处理异步返回的消息
    def __send_websocket(data):
        self.ws.send(data)
    # wshd_noimplement 未实现/dummy handle
    def wshd_noimplement(self, j):
        logging(f'noimplement:{json.dumps(j, ensure_ascii=False)}')
    # wshd_heart_beat 心跳包
    def wshd_heart_beat(self, j):
        if 'heart_beat' in self.handle_register:
            self.handle_register['heart_beat'](j)
            return
        logging(j['content'])
    # wshd_personal_detail 用微信id查询账号信息
    def wshd_personal_detail(self, j):
        if 'personal_detail' in self.handle_register:
            self.handle_register['personal_detail'](j)
            return
        self.wshd_noimplement(j)
    # wshd_personal_info 登陆账号的信息
    def wshd_personal_info(self, j):
        if 'personal_detail' in self.handle_register:
            self.handle_register['personal_detail'](j)
            return
        self.wshd_noimplement(j)
    # wshd_at_msg 预留函数
    def wshd_at_msg(self, j):
        if 'at_msg' in self.handle_register:
            self.handle_register['at_msg'](j)
            return
        self.wshd_noimplement(j)
    # wshd_chatroom_member_nick 获取昵称
    def wshd_chatroom_member_nick(self, j):
        if 'chatroom_member_nick' in self.handle_register:
            self.handle_register['chatroom_member_nick'](j)
            return
        data=j.content
        for d in data:
            logging(f'nickname:{d.nickname}')
    # wshd_chatroom_member 所有群的成员信息
    def wshd_chatroom_member(self, j):
        if 'chatroom_member' in self.handle_register:
            self.handle_register['chatroom_member'](j)
            return
        data=j.content
        for d in data:
            logging(f'roomid:{d.roomid}')
    # wshd_user_list 联系人
    def wshd_user_list(self, j):
        for item in j['content']:
            self.contact_list[item['wxid']] = item
        if 'user_list' in self.handle_register:
            self.handle_register['user_list'](j)
            return
        # alias
        if 'contact_list' in self.handle_register:
            self.handle_register['contact_list'](j)
            return
        logging('启动完成')
    # wshd_join_room 进群事件
    def wshd_join_room(self, j):
        if 'join_room' in self.handle_register:
            self.handle_register['join_room'](j)
            return
        logging(f'join_room:{j}')
    # wshd_debug_switch debug开关消息
    def wshd_debug_switch(self, j):
        if 'debug_switch' in self.handle_register:
            self.handle_register['debug_switch'](j)
            return
        logging(j)
    # wshd_recv_txt_cite_msg 引用的文字消息
    def wshd_recv_txt_cite_msg(self, msg_json):
        if 'recv_txt_cite_msg' in self.handle_register:
            self.handle_register['recv_txt_cite_msg'](j)
            return
        msgXml=msg_json['content']['content'].replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
        soup=BeautifulSoup(msgXml,'lxml')
        msg_json={
            'content':soup.select_one('title').text,
            'id':msg_json['id'],
            'id1':msg_json['content']['id2'],
            'id2':'wxid_fys2fico9put22',
            'id3':'',
            'srvid':msg_json['srvid'],
            'time':msg_json['time'],
            'type':msg_json['type'],
            'wxid':msg_json['content']['id1']
        }
        
        self.wshd_recv_txt_msg(msg_json)
    # wshd_recv_txt_msg 文字消息
    def wshd_recv_txt_msg(self, msg_json):
        if 'recv_txt_msg' in self.handle_register:
            self.handle_register['recv_txt_msg'](j)
            return
        logging(f'收到消息:{msg_json}')
        msg_content = msg_json['content'].replace('\u2005','')
        if '@chatroom' in msg_json['wxid']:
            roomid = msg_json['wxid'] #群id
            senderid = msg_json['id1'] #个人id
        else:
            roomid = None
            nickname = 'null'
            senderid = msg_json['wxid'] #个人id
        nickname = self.get_chatroom_member_nick(roomid, senderid)['content']['nick']
        key_replys = {
            "ding": "dong",
            "dong": "ding",
        }
        func_replays = [
            {
                "match":lambda x:x.startswith('/echo '),
                "replay":lambda x:x[len("/echo "):],
            }
        ]
        if not roomid:
            nickname = 'null'
        if msg_content in key_replys:
            self.ws.send(query.send_msg(key_replys[msg_content],roomid=roomid,wxid=senderid,nickname=nickname))
        for f in func_replays:
            if not f["match"](msg_content):
                continue
            self.ws.send(query.send_msg(f["replay"](msg_content),roomid=roomid,wxid=senderid,nickname=nickname))
            break
    # wshd_recv_pic_msg 图片消息
    def wshd_recv_pic_msg(self, msg_json):
        if 'recv_pic_msg' in self.handle_register:
            self.handle_register['recv_pic_msg'](j)
            return
        self.wshd_noimplement(msg_json)

    ########## WebSocket Events ##########
    def make_on_open(self):
        def on_open(ws):
            if 'on_open' in self.handle_register:
                self.handle_register['on_open'](ws)
                return
            ws.send(query.get_contact_list())
        return on_open
    def make_on_error(self):
        def on_error(ws, error):
            if 'on_error' in self.handle_register:
                self.handle_register['on_error'](ws, error)
                return
            logging(f'on_error:{error}')
        return on_error
    def make_on_close(self):
        def on_close(ws):
            if 'on_close' in self.handle_register:
                self.handle_register['on_close'](ws)
                return
            logging("closed")
        return on_close
    def make_on_message(self):
        def on_message(ws, message):
            j=json.loads(message)
            resp_type=j['type']
            action={
                query.PERSONAL_DETAIL:self.wshd_personal_detail,
                query.PERSONAL_INFO:self.wshd_personal_info,
                query.CHATROOM_MEMBER_NICK:self.wshd_chatroom_member_nick,
                query.AT_MSG:self.wshd_at_msg,
                query.DEBUG_SWITCH:self.wshd_debug_switch,
                query.CHATROOM_MEMBER:self.wshd_chatroom_member,
                query.RECV_PIC_MSG:self.wshd_recv_pic_msg,
                query.RECV_TXT_MSG:self.wshd_recv_txt_msg,
                query.RECV_TXT_CITE_MSG:self.wshd_recv_txt_cite_msg,
                query.HEART_BEAT:self.wshd_heart_beat,
                query.USER_LIST:self.wshd_user_list,
                query.GET_USER_LIST_SUCCSESS:self.wshd_user_list,
                query.GET_USER_LIST_FAIL:self.wshd_user_list,
                query.JOIN_ROOM:self.wshd_join_room,
                query.TXT_MSG:self.wshd_noimplement,
                query.PIC_MSG:self.wshd_noimplement,
            }
            action.get(resp_type, print)(j)
        return on_message
    
    def run(self):
        self.ws.run_forever()

if __name__ == "__main__":
    h = Bot()
    if len(sys.argv) > 1:
        print(eval('h.'+sys.argv[1]))
        exit(0)
    #h.register("on_open", lambda ws: logging("hi~"))
    h.register("on_close", lambda ws: logging("byebye~"))
    print(h.get_personal_info())
    h.run()