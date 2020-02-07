#!/usr/bin/env python3
# coding: utf-8
import sys
#sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import requests
from bs4 import BeautifulSoup
from configs.configs import config
import logging
import pytest



logging.basicConfig(level=config.tutti_configs["local_logging_basic"]["level"],
                    filename=config.tutti_configs["local_logging_basic"]["filename"],
                    datefmt=config.tutti_configs["local_logging_basic"]["datefmt"],
                    format=config.tutti_configs["local_logging_basic"]["format"])
logger = logging.getLogger(__name__)

def job(url):
    res = []
    try:
        web_data = requests.get(url)  #请求网络数据
        soup = BeautifulSoup(web_data.text, "lxml")
        #print(web_data)
        currency_name = soup.select(config.Obtain_configs["curr_name"])  #获取数据里的货币名称，价格和简称
        currency_price = soup.select(config.Obtain_configs["curr_price"])
        currency_symbol = soup.select(config.Obtain_configs["curr_symbol"])
        for symbol,price,name in zip(currency_symbol,currency_price,currency_name):
            data = {
                "name": name.get_text(),
                "symbol": symbol.get_text(),
                "price": price.get_text()
            }  #将每一个货币的信息打包成一个dictionary，加入到最终返回的列表里
            res.append(data)

    except:#一般是网络不稳定，网络延迟过高，网站服务器问题
        logger.error("Obtain Error",exc_info = True)
    return res


def main():
    result = {}
    res = job(config.Obtain_configs["url"])
    if res == []:
        return "Error:BTC and ETH currency can't be found"
    else:
        for i in res:
            if i["symbol"] == "BTC":
                result["BTC"] = float(i["price"][1:])
            elif i["symbol"] == "ETH":
                result["ETH"] = float(i["price"][1:])
            else:
                pass
        if "BTC" in result.keys() and "ETH" in result.keys():
            return result
        else:
            print("BTC and ETH currency can't be found")
            return False


if __name__ == "__main__":
    print(main())


def test_job_return(): #job函数输入一个url，获取这个URL的信息，把源码进行提取转换，最后输出一个列表，测试返回值是列表
    assert type(job("https://coinmarketcap.com/1")) == type([])
    assert len(job("https://coinmarketcap.com/1")) >5
    assert type(job("https://coinmarketcap.com/1")[0]) == type({})


@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_len_job_inside_return(index): #测试前五个字典中每个包含三种信息
    assert len(job("https://coinmarketcap.com/1")[index]) == 3


def test_main_return(): #测试主函数返回的是字典
    assert type(main()) == type({})


def test_len_main_return(): #测试主函数返回的字典的长度为2
    assert len(main().keys()) == 2


def test_content_main_return(): #测试BTC和ETH在主函数返回的字典里
    assert "BTC" in main() and "ETH" in main()


@pytest.mark.parametrize("name",["BTC","ETH"])
def test_dict_value_main_return(name): #测试主函数返回的字典里的value是浮点值
    assert type(main()[name]) == type(1.11)

