#!/usr/bin/env bash
mkdir docker_buiding || true
# update injector-box
if [ ! -d docker_buiding/injector-box ]; then
    git clone https://github.com/ChisBread/injector-box docker_buiding/injector-box
else
    cd docker_buiding/injector-box
    git pull
    cd -
fi
if [ ! -d docker_buiding/injector-box/target ]; then
    git clone https://github.com/ChisBread/wechat-box docker_buiding/injector-box/target
else
    cd docker_buiding/injector-box/target
    git pull
    cd -
fi
if [ ! -f docker_buiding/injector-box/target/root/WeChatSetup-v3.6.0.18.exe ]; then
    wget -P docker_buiding/injector-box/target/root https://github.com/ChisBread/wechat-box/releases/download/binary-resource/WeChatSetup-v3.6.0.18.exe
fi
cp bin_deps/auto.dll docker_buiding/injector-box/root/drive_c/injector
cd docker_buiding/injector-box
sudo docker build -t chisbread/wechat-service:latest .
cd -
