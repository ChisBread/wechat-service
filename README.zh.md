# WeChat Service
- 微信，只是一个服务
![echo](https://github.com/ChisBread/wechat-service/raw/master/images/echo.png)
![inject](https://github.com/ChisBread/wechat-service/raw/master/images/inject.png)

## Quick Start
1. 拉取或者构建docker镜像, 并使用合适的参数启动

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
# optional 可选,微信数据目录
# -v "<path>:/home/app/WeChat Files/"
# -v "<path>:/home/app/.wine/drive_c/users/app/AppData/"
```
2. 打开http://\<Your IP Address\>:8080/vnc.html 并登陆微信
```bash
# 或者使用wesdk中的工具获取二维码/点击登录按钮
from wesdk import *
dotool = DoTool()
dotool.qrcode('./qr.png') # vnc screenshot
# dotool.click_login()
# dotool.switch_account()
```
3. 运行下面的样例
## Examples
### Mini Bots

minibot包含shell机器人和简单的对话机器人; 为避免造成骚扰和引起安全问题, 该样例必须指定可聊天对象
```
# query: 你会思考吗? reply: 我会思考
# query: /sh.exec echo '好玩' reply: 好玩
python3 minibot.py example-config.yaml <chat partner's nickname>
```
### 注册自定义事件函数

Websocket 事件
```python
from wesdk import *
# connect to hook service
bot = Bot(ip='127.0.0.1', port=5555)
bot.register("on_open", lambda ws: logging("hi"))
bot.register("on_close", lambda ws: logging("bye"))
# run event loop
bot.run()
```
消息事件
```python
# Hip hop Bot
bot.register("recv_txt_msg", lambda msg: bot.send_msg('yo', msg['wxid']) if msg['content'] == 'hey' else None)
```
### Info API

联系人列表(包括群)
```bash
# About key 'wxid'
## roomid: *@chatroom
## wechatid: wxid_* or user-defined
python3 example.py 'get_contact_list()'
```
昵称
```bash
# user at contact list
python3 example.py "get_user_nick(${wechatid})"
# user at chatroom
python3 example.py "get_chatroom_member_nick(${roomid},${wechatid})"
```
个人信息
```bash
# self
python3 example.py "get_personal_info()"
# contact (useless)
python3 example.py "get_personal_detail(${wechatid})"
```
发送消息
```bash
# 文本消息: 需要 wechatid 或者 roomid 
# @消息:   需要 wechatid, roomid, nickname
python3 example.py "send_msg(${msg}, ${wechatid}, ${roomid}, ${nickname})"
# 图片或者文件消息:
## wechatid 或者 roomid
## msg: <Windows格式路径> e.g. c:\1.jpg or c:\1.tar.gz
### c:\ <==> 对应容器路径 /home/app/.wine/drive_c 
# 注意: 不需要的参数留空即可
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