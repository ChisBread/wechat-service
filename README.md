[简体中文](./README.zh.md)

[免责声明](./Disclaimer.md)

# WeChat Service
- Let your WeChat run as a service
![echo](https://github.com/ChisBread/wechat-service/raw/master/images/echo.png)
![inject](https://github.com/ChisBread/wechat-service/raw/master/images/inject.png)
## Quick Start
1. Pull(or build) and run your wechat service

```bash
# pull
sudo docker pull chisbread/wechat-service
# or build
# ./build-injector-box.sh
sudo docker run -it --name wechat-service --rm  \
    -e HOOK_PROC_NAME=WeChat \
    -e HOOK_DLL=auto.dll \
    -e TARGET_AUTO_RESTART="yes" \
    -e INJ_CONDITION="[ \"\`sudo netstat -tunlp | grep 5555\`\" != '' ] && exit 0 ; sleep 5 ; curl 'http://127.0.0.1:8680/hi' 2>/dev/null | grep -P 'code.:0'" \
    -e TARGET_CMD=wechat-start \
    -p 8080:8080 -p 5555:5555 -p 5900:5900 \
    --add-host=dldir1.qq.com:127.0.0.1 \
    chisbread/wechat-service:latest
# optional
# -v "<path>:/home/app/WeChat Files/"
# -v "<path>:/home/app/.wine/drive_c/users/user/Application Data/"

## tips. mount cifs (https://docs.unmanic.app/docs/advanced/docker_compose_cifs_mounts)
```
2. open noVNC http://\<Your IP Address\>:8080/vnc.html and login wechat
```bash
# Use wesdk to click the login button, or get the QR code
from wesdk import *
dotool = DoTool()
dotool.qrcode('./qr.png') # vnc screenshot
# dotool.click_login()
# dotool.switch_account()
```
3. run the following example
## Examples
### Mini Bot
The minibot contains shell bot and "smart" bot; to avoid harassment and security concerns, the sample must specify who can chat
```
# query: 你会思考吗? reply: 我会思考
# query: /sh.exec echo '好玩' reply: 好玩
python3 minibot.py example-config.yaml <chat partner's nickname>
```
### Register your own function to the message event

Websocket events
```python
from wesdk import *
# connect to hook service
bot = Bot(ip='127.0.0.1', port=5555)
bot.register("on_open", lambda ws: logging("hi"))
bot.register("on_close", lambda ws: logging("bye"))
# run event loop
bot.run()
```
Receive at message
```python
# Hip hop Bot
bot.register("recv_txt_msg", lambda msg: bot.send_msg('yo', msg['wxid']) if msg['content'] == 'hey' else None)
```
### Info API

Pull all contact info (chatroom and user)
```bash
# About key 'wxid'
## roomid: *@chatroom
## wechatid: wxid_* or user-defined
python3 example.py 'get_contact_list()'
```
Nickname
```bash
# user at contact list
python3 example.py "get_user_nick(${wechatid})"
# user at chatroom
python3 example.py "get_chatroom_member_nick(${roomid},${wechatid})"
```
Personal info
```bash
# self
python3 example.py "get_personal_info()"
# contact (useless)
python3 example.py "get_personal_detail(${wechatid})"
```
Send message
```bash
# TXT MSG: wechatid or roomid is required
# AT MSG: wechatid and roomid and nickname is required
python3 example.py "send_msg(${msg}, ${wechatid}, ${roomid}, ${nickname})"
# sending picture or file:
## wechatid or roomid
## msg: <windows file path> e.g. c:\1.jpg or c:\1.tar.gz
### c:\ <==> /home/app/.wine/drive_c in container
```

## docker-compose
```yaml
version: "3.3"

services:
    wechat-service:
        image: "chisbread/wechat-service:latest"
        restart: unless-stopped
        container_name: "wechat-service"
        environment:
            TARGET_AUTO_RESTART: "yes"
            INJMON_LOG_FILE: "/dev/stdout"
            # 微信的登陆态判断接口
            INJ_CONDITION: " [ \"`sudo netstat -tunlp | grep 5555`\" != '' ] && exit 0 ; sleep 5 ; curl 'http://127.0.0.1:8680/hi' 2>/dev/null | grep -P 'code.:0'"
            HOOK_PROC_NAME: "WeChat"
            TARGET_CMD: "wechat-start"
            HOOK_DLL: "auto.dll"
            #optional INJMON_LOG_FILE: "/dev/null"
            #optional TARGET_LOG_FILE: "/dev/stdout"
        ports:
            - "8080:8080" # noVNC
            - "5555:5555" # websocket server
            - "5900:5900" # vnc server
        extra_hosts:
            - "dldir1.qq.com:127.0.0.1"
        volumes:
            - "<path>:/home/app/WeChat Files/" 
            - "<path>:/home/app/.wine/drive_c/users/app/AppData/"
            - "<path>:/home/app/.wine/drive_c/temp/wechat/" # hook config
        tty: true

```

## Credit
- https://github.com/chisbread/wechat-box
- https://github.com/cixingguangming55555/wechat-bot

## TODO
- *remove all binaries*
  - ~~Python Injector instead of auto-inject.exe binary~~
  - Build auto.dll from source
