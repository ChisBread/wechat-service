# WeChat Service
- Run your WeChat as a service

## TODO
- *remove all binaries*
  - ~~Python Injector instead of auto-inject.exe binary~~
  - Build auto.dll from source

## Usage
- Ding-Dong Bot:
  - https://github.com/chisbread/wechat-service/tree/master/root/drive_c/demo-service/service.py


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
            DEMO_SERVICE: "no"
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