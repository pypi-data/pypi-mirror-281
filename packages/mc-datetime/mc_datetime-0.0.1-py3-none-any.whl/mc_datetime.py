import datetime
import time


def str_to_datetime(datetime_str, pattern='%Y-%m-%d'):
    """
    返回datetime_str对应datetime类型对象
    :param datetime_str: 'YYYYMMDD'格式字符串日期
    :param pattern: 日期格式化类型 '%Y-%m-%d'
    :return: 对应的datetime类型的对象
    """
    return datetime.datetime.strptime(datetime_str, pattern)


def datetime_to_str(datetime_obj, pattern="%Y-%m-%d"):
    """
    返回datetime对象对应的指定pattern的日期字符串
    :param datetime_obj: datetime对象
    :param pattern: 日期格式化类型 '%Y-%m-%d %H:%M:%S'
    :return: 时间对应的字符串
    """
    return datetime_obj.strftime(pattern)


def datetime_str_modify(datetime_str, days=0, hours=0, minutes=0, seconds=0, return_type="str", datetime_pattern='%Y-%m-%d %H:%M:%S', pattern="%Y-%m-%d %H:%M:%S"):
    """
    获取给定的日期字符串往前或者往后推days天数得到的datetime对象或者字符串类型
    :param datetime_str: 日期字符串
    :param days: 要往前或者往后推的天数
    :param hours: 要往前或者往后推的小时数
    :param minutes: 要往前或者往后推的分钟数
    :param seconds: 要往前或者往后推的秒数
    :param return_type: 返回的类型，"str"或者"datetime"
    :param datetime_pattern: datetime_str对应的格式
    :param pattern 返回字符串时的指定格式
    :return:
    """
    datetime_obj = datetime.datetime.strptime(datetime_str, datetime_pattern)
    timedelta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    res = datetime_obj + timedelta
    if return_type == "datetime":
        return res
    res = res.strftime(pattern)
    return res


def current_date(pattern="%Y-%m-%d %H:%M:%S"):
    """
    获取当前日期
    :param: pattern:指定获取日期的格式
    :return: 字符串 "2020-06-15 14:57:23"
    """
    return time.strftime(pattern, time.localtime(time.time()))


def gen_dates(b_date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield b_date + day * i


def get_date_list(start="", end="", datetime_pattern="%Y-%m-%d", pattern="%Y-%m-%d"):
    """
    获取日期列表
    :param start: 开始日期(str, eg:"2021-01-12")
    :param end: 结束日期(str, eg:"2021-01-19")
    :param datetime_pattern: 开始和结束日期的格式
    :param pattern: 结果中的日期格式，默认"%Y-%m-%d"
    :return: 字符串列表，包含start和end
    """
    try:
        start = datetime.datetime.strptime(start, datetime_pattern)
        end = datetime.datetime.strptime(end, datetime_pattern)
    except Exception as e:
        return []
    end = end + datetime.timedelta(days=1)
    data = []
    for date in gen_dates(start, (end - start).days):
        data.append(date.strftime(format=pattern))
    return data


def get_datetime_after(days=0, hours=0, minutes=0, seconds=0, pattern="%Y-%m-%d %H:%M:%S"):
    """
    获取当前日期往后或者往前推的日期
    :param days: 天
    :param hours: 时
    :param minutes: 分
    :param seconds: 秒
    :param pattern: 结果中的日期格式，默认"%Y-%m-%d %H:%M:%S"
    :return: 完整日期
    """
    return (datetime.datetime.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)).strftime(pattern)


def date_to_mktime(the_date, pattern="%Y-%m-%d %H:%M:%S", use_hex=False):
    """
    日期转为时间戳
    :param the_time: 字符串日期，如"2024-01-01"
    :param pattern: 结果中的日期格式，默认"%Y-%m-%d %H:%M:%S"
    :param use_hex: 返回结果是否使用16进制
    """
    strp = time.strptime(the_date, pattern)
    mktime = time.mktime(strp)
    return mktime if not use_hex else hex(int(mktime))[2:]
