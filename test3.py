# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    : 
# @Software: PyCharm

import datetime
import logging
import random
import threading
from queue import Queue
import time

from WechatPCAPI import WechatPCAPI

logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()
clientList = []


def on_message(message):
    queue_recved_message.put(message)


def getText():
    textArray = '是的翻盖手机房管局哦史丹佛阿松大瘦肉首发式发生分公司的公司的阿文阿萨大更符合符合法规和从v从v豆腐干豆腐干问啊问啊撒大苏打法国发过破iu一头热我美女吧v出现在'
    return "".join(random.sample(textArray, 10)) + "-" + datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')


def getRandomTime():
    timeArray = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    return random.choice(timeArray)


# 消息处理示例 仅供参考
def thread_handle_message(wx_inst):
    while True:
        message = queue_recved_message.get()
        print("message", message)
        # if 'msg' in message.get('type'):
        #     # 这里是判断收到的是消息 不是别的响应
        #     msg_content = message.get('data', {}).get('msg', '')
        #     send_or_recv = message.get('data', {}).get('send_or_recv', '')
        #     if send_or_recv[0] == '0':
        #         # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
        #         wx_inst.send_text('filehelper', '收到消息:{}'.format(msg_content))


def main():
    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print('个人信息', wx_inst.get_myself())

    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()

    time.sleep(10)
    # wx_inst.send_text(to_user='filehelper', msg='777888999')
    # time.sleep(1)
    # wx_inst.send_link_card(
    #     to_user='filehelper',
    #     title='博客',
    #     desc='我的博客，红领巾技术分享网站',
    #     target_url='http://www.honglingjin.online/',
    #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # )
    # time.sleep(1)
    #
    # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # time.sleep(1)
    #
    # wx_inst.send_file(to_user='filehelper', file_abspath=r'C:\Users\Leon\Desktop\1.txt')
    # time.sleep(1)
    #
    # wx_inst.send_gif(to_user='filehelper', gif_abspath=r'C:\Users\Leon\Desktop\08.gif')
    # time.sleep(1)
    #
    # wx_inst.send_card(to_user='filehelper', wx_id='gh_6ced1cafca19')

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
    # wx_inst.get_member_of_chatroom('21889884145@chatroom')

    # 新增@群里的某人的功能
    # wx_inst.send_text(to_user='21889884145@chatroom', msg='', at_someone='wxid_qmbk7jpjb61g12')
    # 读取文件

    # wx_inst.send_file(to_user='21889884145@chatroom',
    #                   file_abspath=r'C:\Users\cindata-hrs\Desktop\云途\5月23日福建收货数据....xlsx')
    while True:
        text = getText()
        wx_inst.send_text(to_user='wxid_3nb2dqkhdi6622', msg=text)
        t = getRandomTime()
        time.sleep(t)


if __name__ == '__main__':
    main()
    # print(getText())
    # print(getRandomTime())
