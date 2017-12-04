#-*- coding: utf-8 -*-

#url page mapping
urls = (
    '/', 'index',
    '/output?', 'result',
    '/mail_input','email',
    '/mainpage', 'visuals',
    '/wkrpage', 'subpage',
    '/casepage', 'casepage',
    '/tutorial', 'bootstrap',
    '/testdemo', 'demo',
    '/xml?', 'xmlserver',
    '/lgfile', 'count_holder',
    '/lgfile/(.*)', 'count_down', 
    '/login', 'login',
    '/logout?', 'logout',
    '/jsondata', 'response',
    '/wkrjsondata', 'wkr_response',
    '/casejsondata', 'case_response'
    )

Authenticated = {
    'lei.ji2@hpe.com': 0,
    'guang.liang@hpe.com': 0,
    'mingc@hpe.com': 0,
    'lei.gao@hpe.com': 0,
    'chen.li5@hpe.com': 0,
    'zshi@hpe.com': 0,
    'zu-guo.wang@hpe.com': 0,
    'wenjun.zhu@hpe.com': 0
    }