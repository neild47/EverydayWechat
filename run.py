from GFWeather import GFWeather
import random


def run():
    '''
    主程序入口
    :return:
    '''
    GFWeather().run()


def test_run():
    '''
    运行前的测试
    :return:
    '''
    GFWeather().send_msg(is_test=True)


def test_random():
    r = random.Random()
    print(r.randint(0, 2))


if __name__ == '__main__':
    run()
