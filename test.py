# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    : 
# @Software: PyCharm

import logging
import os
import threading
import time
from queue import Queue

import pandas as pd
from WechatPCAPI import WechatPCAPI

logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()
clientList = []


def on_message(message):
    queue_recved_message.put(message)


def read_excel(path):
    # path = r"C:\Users\cindata-hrs\Desktop\云途\SendData.xlsx"
    df = pd.read_excel(path, header=0)
    return df['内容'].values.tolist()


def init(path):
    df = pd.read_excel(path, header=0)
    clientCodeList = df['客户代码'].values.tolist()
    clientList = []
    for code in clientCodeList:
        clientList.append({'code': code})


def updateWxid(chatroom_id, chatroom_name):
    for item in clientList:
        if item['code'] in chatroom_name:
            item['wxid'] = chatroom_id
            break


def updateWxidTest(chatroom_id, chatroom_name):
    clientList.append({'code': chatroom_name, 'wxid': chatroom_id})


# 消息处理示例 仅供参考
def thread_handle_message(wx_inst):
    while True:
        message = queue_recved_message.get()
        print("message", message)
        if 'friend::chatroom' in message.get('type'):
            chatroom_id = message.get('data', {}).get('chatroom_id', '')
            chatroom_name = message.get('data', {}).get('chatroom_name', '')
            # updateWxid(chatroom_id, chatroom_name)
            updateWxidTest(chatroom_id, chatroom_name)
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
    path = r"C:\Users\cindata-hrs\Desktop\云途\SendData.xlsx"
    clientExcelPath = r"C:\Users\cindata-hrs\Desktop\云途\8.3价格通知\客户代码对接群汇总.xlsx"
    while True:
        print("os.path.exists(path)", os.path.exists(path))
        if os.path.exists(path):
            # 初始化
            init(clientExcelPath)
            # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的回调返回
            print("获取最新的好友群信息")
            wx_inst.update_frinds()
            # 等待读取好友群的线程操作完成
            time.sleep(10)
            # print("clientList", clientList)
            datas = read_excel(path)
            os.remove(path)
            if len(datas) > 0:
                for data in datas:
                    wx_inst.send_text(to_user='filehelper', msg=data)
                    time.sleep(2)
        else:
            time.sleep(5)
    # wx_inst.send_file(to_user='21889884145@chatroom',
    #                   file_abspath=r'C:\Users\cindata-hrs\Desktop\云途\5月23日福建收货数据....xlsx')




if __name__ == '__main__':
    main()
