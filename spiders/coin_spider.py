# coding: utf-8
import sys
sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import requests
from bs4 import BeautifulSoup
import time
import pytest
import logging,socket,urllib3,OpenSSL
from configs.configs import config
from datetime import datetime
from spiders import btc_eth



logging.basicConfig(level=config.tutti_configs["local_logging_basic"]["level"],
                    filename=config.tutti_configs["local_logging_basic"]["filename"],
                    datefmt=config.tutti_configs["local_logging_basic"]["datefmt"],
                    format=config.tutti_configs["local_logging_basic"]["format"])
logger = logging.getLogger(__name__)


def process_time(time):
    #返回一个符合mysql语法的时间字符￿￿￿￿￿￿，分钟以每十分钟向下取整
    return str(time.year)+ str(time.month).zfill(2)+str(time.day).zfill(2)+ "_" \
           +str(time.hour).zfill(2) +str(time.minute//10*10).zfill(2)


def job(url,be_cur):
    #发起网络请求，整理网络返回数据，最终返回一个包含货币名称，简称，兑美元价格的列表
    res = []
    web_data = requests.get(url,timeout= (2.5, 5)) #平均请求时间1.7秒左右，设置链接超时时间2.5秒，读取超时2.4秒
    #print(web_data)#每一次访问都会打印一次网络状态
    logger.info(web_data)
    soup = BeautifulSoup(web_data.text, "lxml")
    currency_name = soup.select(config.CoinMKT_configs["name_info"])
    currency_price = soup.select(config.CoinMKT_configs["price_info"])
    currency_symbol = soup.select(config.CoinMKT_configs["symbol_info"])
    time = process_time(datetime.now())
    if be_cur == False:
        for symbol,price,name in zip(currency_symbol,currency_price,currency_name):
            data = {
                "name": name.get_text(),
                "symbol": symbol.get_text(),
                "to_usd": float(price.get_text()[1:]),
                "time": time
            }
            res.append(data)
        return res
    else:
        for symbol,price,name in zip(currency_symbol,currency_price,currency_name):
            data = {
                "name": name.get_text(),
                "symbol": symbol.get_text(),
                "to_usd": float(price.get_text()[1:]),
                "to_btc":float(price.get_text()[1:])/be_cur["BTC"],
                "to_eth":float(price.get_text()[1:])/be_cur["ETH"],
                "time": time
            }
            res.append(data)
        return res



def main():
    #主程序，会打印程序运行的时间，返回包含所有货币信息的列表
    urls = config.CoinMKT_configs["urls"]
    be_cur = btc_eth.main()
    res = []
    for i in range(len(urls)):
        try:
            res.extend(job(urls[i],be_cur))
            if i == len(urls) -1:#最后一个url访问后直接结束即可
                pass
            else:
                time.sleep(8) #每次切换页面需要等待一段时间，防止被禁
        except RuntimeError:
            logger.error("RunTimeError", exc_info=True)
            print("RuntimeError")
            pass
        except requests.exceptions.ConnectTimeout:
            logger.error("Time Out", exc_info=True)
            print("Time out")
            pass
        except socket.timeout:
            logger.error("Web Socket Timeout")
            print("Web Socket Timeout")
            pass
        except urllib3.exceptions.ReadTimeoutError:
            logger.error("Read Time Out")
            print("Web Read Time Out")
            pass
        except requests.exceptions.ReadTimeout:
            logger.error("Read Time Out")
            print("Web Read Time Out")
            pass
        except OpenSSL.SSL.WantReadError:
            logger.error("Want Read Error")
            print("Want Read Error")
            pass
        except requests.exceptions.ConnectionError:
            logger.error("Web Connection Error")
            print("Connection Error")
            pass
        except:
            logger.error("One Page Jumped",exc_info = True)
            pass
        continue
    return res


if __name__ == "__main__":
    print(main()) # 最多是24

'''
==========================================================================================================================================
==========================================================================================================================================
'''

be_cur = {"BTC":10,"ETH":5}

#注意，测试的时候记得调整配置文件访问对的页面数量
@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_job_return(index): #测试返回值是列表，如果有Internet Error，会跳过
    assert type(job("https://coinmarketcap.com/1",be_cur)) == type([])
    assert len(job("https://coinmarketcap.com/1",be_cur)) > 5
    assert type(job("https://coinmarketcap.com/1",be_cur)[0]) == type({})
    assert len(job("https://coinmarketcap.com/1",be_cur)[index]) == 6

@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_main_return(index): #测试主函数返回的是列表
    assert type(main()) == type([])
    assert len(main()) > 5
    assert type(main()[index]) == type({})
    assert len(main()[index]) == 6
    assert "name" in main()[index] and "symbol" in main()[index] and "time" in main()[index]
