FROM chisbread/wechat-box:latest
# clear payloads
RUN sudo rm -r /payloads
COPY root/ /
# init with GUI
RUN bash -c 'nohup /entrypoint.sh 2>&1 &' && sleep 5 && /payloads.sh \
    && sudo chown -R app:app /drive_c \
    && cp -r /drive_c/* /home/app/.wine/drive_c/ \
    && sudo rm /tmp/.X0-lock
#settings
ENTRYPOINT ["/serv-entrypoint.sh"]
