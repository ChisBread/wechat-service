import json
from uuid import uuid4

HEART_BEAT=5005
RECV_TXT_MSG=1
RECV_PIC_MSG=3
NEW_FRIEND_REQUEST=37
RECV_TXT_CITE_MSG=49
PIC_MSG=500
AT_MSG=550
TXT_MSG=555
USER_LIST=5000
GET_USER_LIST_SUCCSESS=5001
GET_USER_LIST_FAIL=5002
ATTATCH_FILE = 5003
CHATROOM_MEMBER=5010
CHATROOM_MEMBER_NICK=5020
DEBUG_SWITCH=6000
PERSONAL_INFO=6500
PERSONAL_DETAIL=6550
DESTROY_ALL=9999
JOIN_ROOM=10000


def uuid():
	return str(uuid4())
# get_personal_info 获取登陆微信账号信息
def get_personal_info():
    qs={
        'id':uuid(),
        'type':PERSONAL_INFO,
        'content':'op:personal info',
        'wxid':'null',
    }
    return json.dumps(qs)

# get_personal_detail 获取微信id查询账号信息
def get_personal_detail(wxid):
    qs={
        'id':uuid(),
        'type':PERSONAL_DETAIL,
        'content':'op:personal detail',
        'wxid':wxid,
    }
    return json.dumps(qs)
# get_chatroom_member_nick 获取chatroom 成员昵称
def get_chatroom_member_nick(roomid='null', wxid = 'ROOT'):
    if not roomid:
        roomid = 'null'
    if wxid == 'null' and roomid == 'null':
        raise ValueError("wxid和roomid不能同时为'null'")
    qs={
        'id':uuid(),
        'type':CHATROOM_MEMBER_NICK,
        'roomid':roomid,
        'wxid':wxid,
    }
    return json.dumps(qs)
def get_user_nick(wxid):
    return get_chatroom_member_nick(wxid=wxid)
# get_chatroom_member 获取群的成员信息
def get_chatroom_member(roomid='null'):
    qs = {
        'id':uuid(),
        'type':CHATROOM_MEMBER,
        'wxid':'null',
        'roomid':roomid,
        'content':'op:list member',
    }
    return json.dumps(qs)
# get_contact_list 获取当前通讯录的wxid和roomid
def get_contact_list():
    qs = {  
        'id':uuid(),
        'type':USER_LIST,
        'content':'user list',
        'wxid':'null',
	}
    return json.dumps(qs)
# get_user_list alias of get_contact_list
def get_user_list():
    return get_contact_list()

# destroy_all .
def destroy_all():
    qs={
        'id':uuid(),
        'type':DESTROY_ALL,
        'content':'none',
        'wxid':'node',
    }
    return json.dumps(qs)
# send_msg 在私聊、群聊中发送文本、图片、附件消息
# usage: 
#    wxid, roomid任选其一时, 发送非at消息, 根据msg的形式决定具体类型
#    wxid, roomid, nickname都存在时, 发送at消息
def send_msg(msg, wxid='null', roomid='null', nickname='null', force_type=None):
    if not wxid:
        wxid = 'null'
    if not roomid:
        roomid = 'null'
    if wxid == 'null' and roomid == 'null':
        raise ValueError("wxid和roomid不能同时为'null'")
    if force_type and force_type not in [TXT_MSG, PIC_MSG, ATTATCH_FILE, AT_MSG]:
        raise ValueError("force_type错误, 不存在的类型")
    # 二选一时, 都应该填到wxid
    if roomid != 'null' and wxid == 'null':
        nickname = 'null'
        roomid = 'null'
        wxid = roomid
    lmsg = msg.lower()
    msg_type = TXT_MSG
    # auto type
    if (lmsg.startswith("c:\\") or lmsg.startswith("z:\\")) \
            and (lmsg.endswith('.png') or lmsg.endswith('.jpg') or lmsg.endswith('.jpeg')):
        msg_type = PIC_MSG
    elif (lmsg.startswith("c:\\") or lmsg.startswith("z:\\")) \
            and (lmsg.endswith('.7z') or lmsg.endswith('.zip') \
            or lmsg.endswith('.rar') or lmsg.endswith('.tar') or lmsg.endswith('.tar.gz')):
        msg_type = ATTATCH_FILE
    if force_type is not None:
        msg_type = force_type
    # 指定了群
    if roomid != 'null':
        # 带nickname的文本消息，at处理
        if force_type is None and msg_type == TXT_MSG and nickname != 'null':
            msg_type = AT_MSG
        # 其余的都认为是发群消息
        else:
            wxid = roomid
            roomid = 'null'  
    
    qs={
        'id':uuid(),
        'type':msg_type,
        'roomid':roomid,
        'wxid':wxid,
        'content':msg,
        'nickname':nickname,
        'ext':'null'
    }
    return json.dumps(qs)

# debug_switch debugview调试信息开关，默认为关
def debug_switch():
    qs={
        'id':uuid(),
        'type':DEBUG_SWITCH,
        'content':'off',
        'wxid':'ROOT',
    }
    return json.dumps(qs)
