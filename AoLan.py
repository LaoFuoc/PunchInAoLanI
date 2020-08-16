# encoding: utf-8
import datetime
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from lxml import etree

"""获取网页token，登录奥蓝系统进行自动打卡"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Upgrade-Insecure-Requests': '1'
}


def NowTime():
    now = datetime.datetime.now()
    times = now.strftime('%Y-%m-%d %H:%M:%S')
    # 判断当前时间，进行打卡
    if 7 < now.hour < 11:
        morning = 36.4
        midday = 0.0
        late = 0.0
        return morning, midday, late
    if 11 <= now.hour < 19:
        morning = 36.4
        midday = 36.5
        late = 0.0
        return morning, midday, late
    if 19 <= now.hour < 24:
        morning = 36.4
        midday = 36.5
        late = 36.4
        return times, morning, midday, late


def landing_edu(username, password, execution):
    data = {
        'username': username,
        'password': password,
        'authcode': None,
        'execution': execution,
        '_eventId': 'submit'
    }
    session.post('http://i.cque.edu.cn/cas/login?service=http://i.cque.edu.cn:8081/im/system/login/login.zf',
                 headers=headers, data=data)
    url = 'http://i.cque.edu.cn:8081/im/system/application/getAllList.zf?yymc='
    resp = session.post(url, headers=headers)
    text = resp.text
    if re.search('<title>(.*?)</title>', text, re.S) == None:
        print("登陆成功")


    else:
        main(username, password)
        sys.exit()


def Clock(username, password, execution):
    landing_edu(username=username, password=password, execution=execution)
    times, morning, midday, late = NowTime()
    AoLan_Url = 'http://183.230.3.9:866/login.aspx'
    session.get(AoLan_Url, headers=headers)
    Clock_Url = 'http://183.230.3.9:866/txxm/rsbulid/r_3_3_st_xgfkmrdk3.aspx?xq=2019-2020-2&nd=2019&msie=1'
    resp = session.get(Clock_Url, headers=headers)
    html = etree.HTML(resp.text)
    # 获取参数
    VIEWSTATE = html.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    VIEWSTATEGENERATOR = html.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
    dkrq = html.xpath('//*[@id="dkrq"]/@value')[0]
    dkrqdm = html.xpath('//*[@id="dkrqdm"]/@value')[0]
    czsj = times
    uname = html.xpath('//*[@id="xm"]/@value')[0]
    xdm = html.xpath('//*[@id="xdm"]/@value')[0]
    bjhm = html.xpath('//*[@id="bjhm"]/@value')[0]
    xh = html.xpath('//*[@id="xh"]/@value')[0]
    xm = html.xpath('//*[@id="xm"]/@value')[0]
    pkey = html.xpath('//*[@id="pkey"]/@value')[0]
    st_xq = html.xpath('//*[@id="st_xq"]/@value')[0]

    data = {
        '__EVENTTARGET': 'databc',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        '__VIEWSTATEENCRYPTED': '',
        'dkrq': dkrq,
        'dkrqdm': dkrqdm,
        'xczxck': 'on',
        'ck_xczxck': True,
        'ywyxqx': '无',
        'ywyxqxdm': '00',
        'sfzxx': '否',
        'sfzxxdm': 2,
        'jrszd1': '重庆市江津区',
        'jrszd1dm': 500116,
        'jrsffy': '',
        'jrsffydm': '',
        'jrszd2': '',
        'jrszd2dm': '',
        'czjtgjxq': '',
        'styczk': '',
        'tw_cj': morning,
        'tw_wj': midday,
        'tw_nj': late,
        'ptbz': '',
        'uname': uname,
        'czsj': czsj,
        'fdyyj': '',
        'uname2': '',
        'czsj2': '',
        'pzd_lock': 'uname',
        'pzd_lock2': 'uname,fdyyj,uname2,czsj2',
        'pzd_lock3': '',
        'pzd_lock4': '',
        'pzd_y': '',
        'xdm': xdm,
        'bjhm': bjhm,
        'xh': xh,
        'xm': xm,
        'qx_r': 1,
        'qx_i': 1,
        'qx_u': 1,
        'qx_d': 1,
        'qx2_r': '',
        'qx2_i': '',
        'qx2_u': '',
        'qx2_d': '',
        'databcxs': 1,
        'databcdel': 1,
        'xzbz': '',
        'pkey': pkey,
        'pkey4': '',
        'xs_bj': '',
        'bdbz': '',
        'dcbz': 1,
        'cw': '',
        'hjzd': '',
        'xqbz': '',
        'ndbz': '',
        'st_xq': st_xq,
        'st_nd': '',
        'mc': '',
        'smbz': 2,
        'fjmf': '',
        'psrc': '',
        'pa': '',
        'pb': '',
        'pc': '',
        'pd': '',
        'pe': '',
        'pf': '',
        'pg': '',
        'msie': 1,
        'txxmxs': '',
        'tkey': dkrqdm,
        'tkey4': '',
        'jjzt': '',
        'lszt': '',
    }
    res = session.post(Clock_Url, data=data)
    content = etree.HTML(res.text)
    state = content.xpath('//*[@id="cw"]/@value')[0]
    print(state)
    txt = '\n' + uname + '\n晨检温度：' + str(morning) + '\n午检温度：' + str(midday) + '\n晚检温度：' + str(late) + '\n'

    return czsj, txt, state


def send(receivers, message):
    sender = '2168258948@qq.com'
    mess = MIMEMultipart('related')
    subject = '每日打卡详情'
    mess['Subject'] = subject
    mess['From'] = sender
    mess['To'] = ",".join(receivers)
    mess.attach(MIMEText(message))

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender, "ktqobkcycwvjecfa")
        server.sendmail(sender, receivers, mess.as_string())
        server.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


def main(username, password):
    resp = session.post('http://i.cque.edu.cn/cas/login?service=http://i.cque.edu.cn:8081/im/system/login/login.zf',
                        headers=headers)
    text = resp.text
    get_execution = re.search('<input.*?name="execution"\Wvalue="(.*?)"./>', text, re.S)  # 获取登陆过程中的token
    execution = get_execution.group(1)
    print("----请稍等，正在登陆----")
    czsj, txt, state = Clock(username, password, execution)
    info = [czsj, txt, state, '\n']

    return info


if __name__ == '__main__':
    session = requests.session()
#     dicts中存入字典，键为学号，值为密码。
    dicts = {'1712085xxx': 'laofuxxx'}
    infos = []
    for username, password in dicts.items():
        info = main(username, password)
        infos.append(info)
        session = requests.session()
    message = ''.join(map(str, [y for x in infos for y in x]))
    send(['1534372468@qq.com'], message)
