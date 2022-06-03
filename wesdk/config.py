#coding: utf-8

import copy
import yaml
import re
import sys
import traceback
import importlib
import wesdk.minibots as minibots
from collections.abc import Mapping
# rule_wrapper 根据规则, 对minibot函数进行封装
def rule_wrapper(conf, bot_rule):
    rule = copy.deepcopy(bot_rule)
    # pattern 兼容list和str类型, 预编译正则表达式
    if 'pattern' in rule:
        if isinstance(rule['pattern'], list):
            for i, pat in enumerate(rule['pattern']):
                rule['pattern'][i] = re.compile(pat)
        else:
            rule['pattern'] = re.compile(rule['pattern'])
    # chat-rule 兼容list和str类型
    if 'chat-rule' in rule:
        if isinstance(rule['chat-rule'], list):
            for i, rulename in enumerate(rule['chat-rule']):
                rule['chat-rule'][i] = conf['chat-rules'][rulename]
        else:
            rule['chat-rule'] = [conf['chat-rules'][rule['chat-rule']]]
    # 全局minibot映射
    if 'minibot' in rule:
        rule['minibot'] = conf['minibots'][rule['minibot']]
    def wrapped_bot(bot, msg):
        # OR ...
        pat_pass = False
        mt = None
        if isinstance(rule['pattern'], list):
            for pat in rule['pattern']:
                mt = pat.search(msg['content'])
                if mt:
                    pat_pass = True
                    break
        else:
            mt = rule['pattern'].search(msg['content'])
            if mt:
                pat_pass = True
        if not pat_pass:
            return False
        # AND ...
        for chat_rule in rule['chat-rule']:
            chat_rule_pass = False
            if 'nickname' in chat_rule:
                nickrule = chat_rule['nickname']
                if isinstance(nickrule, list):
                    for pat in nickrule:
                        if pat.search(msg['nickname']):
                            chat_rule_pass = True
                            break
                elif nickrule.search(msg['nickname']):
                    chat_rule_pass = True
            
            if 'senderid' in chat_rule and msg['senderid'] in chat_rule['senderid']:
                chat_rule_pass = True
            if 'roomid' in chat_rule and msg['roomid'] in chat_rule['roomid']:
                chat_rule_pass = True
            
            if not chat_rule_pass:
                return False
        
        if 'pattern-trim' in rule:
            msg['content'] = msg['content'][0:mt.span()[0]] + msg['content'][mt.span()[1]:]
        rule['minibot'](bot, msg)
        return True
    return wrapped_bot

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source
# load_bots: 加载配置文件中定义的bot规则
## 返回minibot函数 combine(bot, msg)
def load_bots(filepath, updates={}):
    conf = None
    with open(filepath, 'r', encoding="utf-8") as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    if not conf:
        return None
    deep_update(conf, updates)
    if isinstance(conf.get('sys', {}).get('path', []), list):
        sys.path += conf.get('sys', {}).get('path', [])
    imports = {}
    # 将minibots配置文件解析为形如foo(bot, msg)的函数
    for key, val in conf['minibots'].items():
        if 'import' in val:
            if val['import'] not in imports:
                imports[val['import']] = importlib.import_module(val['import'])
            imp = imports[val['import']]
            conf['minibots'][key] = eval('imp.'+val['function'])
        else:
            conf['minibots'][key] = eval(val['function'])
    # 预编译chat-rules规则
    for key, val in conf['chat-rules'].items():
        if 'nickname' in val:
            if isinstance(val['nickname'], list):
                for i, pat in enumerate(val['nickname']):
                    conf['chat-rules'][key]['nickname'][i] = re.compile(pat)
            else:
                conf['chat-rules'][key]['nickname'] = re.compile(val['nickname'])
    
    bots = []
    for i, bot_rule in enumerate(conf['reply-rules']):
        bots.append(rule_wrapper(conf, bot_rule))
    return minibots.make_combinebot(bots)