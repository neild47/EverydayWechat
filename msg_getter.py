import requests
from bs4 import BeautifulSoup
from config import config
import utils
from datetime import datetime
from one_ids import oneIds
import random


class MsgGetter:
    def get_ciba_msg(self):
        '''
        从词霸中获取每日一句，带英文。
        :return:str ,返回每日一句（双语）
        '''
        print('获取格言信息（双语）...')
        resp = requests.get('http://open.iciba.com/dsapi')
        if resp.status_code == 200 and utils.isJson(resp):
            conentJson = resp.json()
            content = conentJson.get('content')
            note = conentJson.get('note')
            return f"{content}\n{note}\n"
        else:
            print("没有获取到数据")
            return None

    def get_dictum_msg(self):
        '''
        获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
        :return: str， 一句格言或者短语
        '''
        print('获取格言信息...')
        user_url = 'http://wufazhuce.com/'
        resp = requests.get(user_url, headers=config.headers)
        if resp.status_code == 200:
            soup_texts = BeautifulSoup(resp.text, 'lxml')
            # 『one -个』 中的每日一句
            every_msg = soup_texts.find_all('div', class_='fp-one-cita')[0].find('a').text
            return every_msg + "\n"
        print('每日一句获取失败')
        return ''

    def get_random_ONE_msg(self):
        url = "http://wufazhuce.com/one/"
        random_id = random.Random().randint(0, len(oneIds) - 1)
        resp = requests.get(url + str(random_id), headers=config.headers)
        if resp.status_code == 200:
            soup_texts = BeautifulSoup(resp.text, 'lxml')
            msg = soup_texts.find_all("div", class_='one-cita')[0].text
            return msg + "\n"
        return ''

    def get_lovelive_msg(self):
        '''
        从土味情话中获取每日一句。
        :return: str,土味情话
        '''
        print('获取土味情话...')
        resp = requests.get("https://api.lovelive.tools/api/SweetNothings")
        if resp.status_code == 200:
            return resp.text + "\n"
        else:
            print('每日一句获取失败')
            return None

    def get_weather_msg(self, city_code):
        weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'
        resp = requests.get(url=weather_url)
        if resp.status_code == 200 and utils.isJson(resp) and resp.json().get('status') == 200:
            weatherJson = resp.json()
            # 今日天气
            today_weather = weatherJson.get('data').get('forecast')[1]
            # 今日日期
            today_time = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')
            # 今日天气注意事项
            notice = today_weather.get('notice')
            # 温度
            high = today_weather.get('high')
            high_c = high[high.find(' ') + 1:]
            low = today_weather.get('low')
            low_c = low[low.find(' ') + 1:]
            temperature = f"温度 : {low_c}/{high_c}"

            # 风
            fx = today_weather.get('fx')
            fl = today_weather.get('fl')
            wind = f"{fx} : {fl}"

            # 空气指数
            aqi = today_weather.get('aqi')
            aqi = f"空气 : {aqi}"
            return f'{notice}\n{temperature}\n{wind}\n{aqi}\n'
        return ""

    def get_delta_msg(self, start):
        if start:
            try:
                start_datetime = datetime.strptime(start, "%Y-%m-%d")
                day_delta = (datetime.now() - start_datetime).days
                delta_msg = f'宝贝这是我们在一起的第 {day_delta} 天。\n'
            except:
                delta_msg = ''
        else:
            delta_msg = ''
        return delta_msg

    def get_today_time(self):
        return datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日') + "\n"

    def get_drink_msg(self):
        strs = ['快喝水！！！', '起来走达走达喝点水', '起来溜达溜达喝点水', '久坐对身体不好，起来喝点水', '快起来喝水']
        r = random.Random()
        return strs[r.randint(0, len(strs) - 1)]

    def get_msg_by_channel(self, channel):
        channelToMsgFunc = {1: self.get_random_ONE_msg, 2: self.get_ciba_msg, 3: self.get_lovelive_msg}
        if channelToMsgFunc[channel]:
            return channelToMsgFunc[channel]()
        return ''


msgGetter = MsgGetter()
