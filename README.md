# WeChat Service
- Run your WeChat as a service

## TODO
- *remove all binaries*
  - ~~Python Injector instead of auto-inject.exe binary~~
  - Build auto.dll from source

## Usage
1. Pull(or build) and run your wechat service
2. open noVNC http://<Your IP Address>:8080/vnc.html and login wechat
3. run the following example
### Examples
#### Ding-Dong Bot:

```bash
python3 bot/bot.py
```
#### Register your own function to the message event

Websocket events
```python
h.register("on_open", lambda ws: logging("hi"))
h.register("on_close", lambda ws: logging("bye"))
```
Receive at message
```python
# Hip hop Bot
h.register("recv_txt_msg", lambda msg: h.send_msg('yo', msg['wxid']) if msg['content'] == 'hey' else None)
```
#### Info API

Pull all contact info (chatroom and user)
```bash
# About key 'wxid'
## roomid: *@chatroom
## wechatid: wxid_* or user-defined
python3 bot/bot.py 'get_contact_list()'
```
Nickname
```bash
# user at contact list
python3 bot/bot.py "get_user_nick(${wechatid})"
# user at chatroom
python3 bot/bot.py "get_chatroom_member_nick(${roomid},${wechatid})"
```
Personal info
```bash
# self
python3 bot/bot.py "get_personal_info()"
# contact (useless)
python3 bot/bot.py "get_personal_detail(${wechatid})"
```
Send message
```bash
# TXT MSG: wechatid or roomid is required
# AT MSG: wechatid and roomid and nickname is required
python3 bot/bot.py "send_msg(${msg}, ${wechatid}, ${roomid}, ${nickname})"
# sending picture or file:
## wechatid or roomid
## msg: <windows file path> e.g. c:\1.jpg or c:\1.tar.gz
### c:\ <==> /home/app/.wine/drive_c in container
```

# Build Image
```bash
./build-docker.sh
```
## Credit
- https://github.com/chisbread/wechat-box
- https://github.com/cixingguangming55555/wechat-bot
## docker run
```
sudo docker run -it --name wechat-service --rm  \
    -e HOOK_PROC_NAME=WeChat \
    -e HOOK_DLL=auto.dll \
    -e WC_AUTO_RESTART="yes" \
    -e INJ_CONDITION="[ \"\`sudo netstat -tunlp | grep 5555\`\" != '' ] && exit 0 ; sleep 5 ; curl 'http://127.0.0.1:8680/hi' 2>/dev/null | grep -P 'code.:0'" \
    -e TARGET_CMD=wechat-start \
    -v "<path>:/home/app/WeChat Files/" \
    -v "<path>:/home/app/.wine/drive_c/users/user/Application Data/" \
    -v "<path>:/home/app/.wine/drive_c/temp/wechat/" \
    -p 8080:8080 -p 5555:5555 -p 5900:5900 \
    chisbread/wechat-service:latest
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
            WC_AUTO_RESTART: "yes"
            INJMON_LOG_FILE: "/dev/stdout"
            # 微信的登陆态判断接口
            INJ_CONDITION: " [ \"`sudo netstat -tunlp | grep 5555`\" != '' ] && exit 0 ; sleep 5 ; curl 'http://127.0.0.1:8680/hi' 2>/dev/null | grep -P 'code.:0'"
            HOOK_PROC_NAME: "WeChat"
            TARGET_CMD: "wechat-start"
            HOOK_DLL: "auto.dll"
            #optional INJMON_LOG_FILE: "/dev/null"
        ports:
            - "8080:8080" # noVNC
            - "5555:5555" # websocket server
        volumes:
            - "<path>:/home/app/WeChat Files/" 
            - "<path>:/home/app/.wine/drive_c/users/user/Application Data/"
            - "<path>:/home/app/.wine/drive_c/temp/wechat/" # hook config
        tty: true

```