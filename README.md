# WeChat Service
- Run your WeChat as a service

## TODO
- *remove all binaries*
  - ~~Python Injector instead of auto-inject.exe binary~~
  - Build auto.dll from source

## Usage
- Ding-Dong Bot:
```bash
python bot/bot.py
```
# Build Image
```bash
./build-docker.sh
```
## Credit
- https://github.com/chisbread/wechat-box
- https://github.com/cixingguangming55555/wechat-bot

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
            INJ_CONDITION: "sleep 5; curl 'http://127.0.0.1:8680/hi' 2>/dev/null | grep -P 'code.:0'" 
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