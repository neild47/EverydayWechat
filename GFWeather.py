import os
import time
from datetime import datetime

import itchat
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from config import config
import utils
from msg_getter import msgGetter

# fire the job again if it was missed within GRACE_PERIOD
GRACE_PERIOD = 15 * 60


class GFWeather:

    def __init__(self):
        pass

    def is_online(self, auto_login=False):
        '''
        判断是否还在线,
        :param auto_login: bool,如果掉线了则自动登录(默认为 False)。
        :return: bool,当返回为 True 时，在线；False 已断开连接。
        '''

        def online():
            '''
            通过获取好友信息，判断用户是否还在线
            :return: bool,当返回为 True 时，在线；False 已断开连接。
            '''
            try:
                if itchat.search_friends():
                    return True
            except:
                return False
            return True

        if online():
            return True
        # 仅仅判断是否在线
        if not auto_login:
            return online()

        # 登陆，尝试 5 次
        for _ in range(5):
            # 命令行显示登录二维码
            # itchat.auto_login(enableCmdQR=True)
            if os.environ.get('MODE') == 'server':
                itchat.auto_login(enableCmdQR=2)
            else:
                itchat.auto_login()
            if online():
                print('登录成功')
                return True
        else:
            print('登录成功')
            return False

    def run(self):
        '''
        主运行入口
        :return:None
        '''
        # 自动登录
        if not self.is_online(auto_login=True):
            return
        for girlfriend in config.girlfriend_list:
            wechat_name = girlfriend.get('wechat_name')
            friends = itchat.search_friends(name=wechat_name)
            if not friends:
                print('昵称有误')
                return
            name_uuid = friends[0].get('UserName')
            girlfriend['name_uuid'] = name_uuid

        # 定时任务
        scheduler = BlockingScheduler()
        # 每天9：30左右给女朋友发送每日一句
        scheduler.add_job(self.send_msg, 'cron', hour=config.alarm_hour,
                          minute=config.alarm_minute, misfire_grace_time=GRACE_PERIOD)
        # 每隔 2 分钟发送一条数据用于测试。
        if utils.isDebug():
            scheduler.add_job(self.send_msg, 'interval', seconds=30)
        scheduler.start()

    def send_msg(self, is_test=False):
        '''
        每日定时开始处理。
        :param is_test:bool, 测试标志，当为True时，不发送微信信息，仅仅获取数据。
        :return: None。
        '''
        print("*" * 50)
        print('获取相关信息...')

        if config.dictum_channel == 1:
            dictum_msg = msgGetter.get_dictum_msg()
        elif config.dictum_channel == 2:
            dictum_msg = msgGetter.get_ciba_msg()
        elif config.dictum_channel == 3:
            dictum_msg = msgGetter.get_lovelive_msg()
        else:
            dictum_msg = ''

        for girlfriend in config.girlfriend_list:
            city_code = girlfriend.get('city_code')
            start_date = girlfriend.get('start_date').strip()
            sweet_words = girlfriend.get('sweet_words')
            today_msg = self.get_message(dictum_msg, city_code=city_code, start_date=start_date,
                                         sweet_words=sweet_words)
            name_uuid = girlfriend.get('name_uuid')
            wechat_name = girlfriend.get('wechat_name')
            print(f'给『{wechat_name}』发送的内容是:\n{today_msg}')

            if not is_test:
                if self.is_online(auto_login=True):
                    itchat.send(today_msg, toUserName=name_uuid)
                # 防止信息发送过快。
                time.sleep(5)

        print('发送成功..\n')

    def get_message(self, dictum_msg='', city_code='101030100', start_date='2018-01-01',
                    sweet_words='From your Valentine'):
        '''
        获取天气信息。网址：https://www.sojson.com/blog/305.html
        :param dictum_msg: str,发送给朋友的信息
        :param city_code: str,城市对应编码
        :param start_date: str,恋爱第一天日期
        :param sweet_words: str,来自谁的留言
        :return: str,需要发送的话。
        '''
        today_msg = f'{msgGetter.get_today_time()}{msgGetter.get_delta_msg(start_date)}{msgGetter.get_weather_msg(city_code)}{dictum_msg}{sweet_words if sweet_words else ""}\n'
        return today_msg


if __name__ == '__main__':
    # 直接运行
    # GFWeather().run()

    # 只查看获取数据，
    # GFWeather().start_today_info(True)

    # 测试获取词霸信息
    # ciba = GFWeather().get_ciba_info()
    # print(ciba)

    # 测试获取每日一句信息
    # dictum = GFWeather().get_dictum_info()
    # print(dictum)

    # 测试获取天气信息
    # wi = GFWeather().get_weather_info('sorry \n')
    # print(wi)
    pass
