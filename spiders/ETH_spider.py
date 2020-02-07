import sys
#sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytest
import logging
import socket, urllib3, OpenSSL
from spiders import btc_eth
from configs.configs import config


logging.basicConfig(level=config.tutti_configs["local_logging_basic"]["level"],
                    filename=config.tutti_configs["local_logging_basic"]["filename"],
                    datefmt=config.tutti_configs["local_logging_basic"]["datefmt"],
                    format=config.tutti_configs["local_logging_basic"]["format"])
logger = logging.getLogger(__name__)


def process_time(time):
    ##返回一个符合mysql语法的时间字符￿￿￿￿￿￿，分钟以每十分钟向下取整
    return str(time.year)+ str(time.month).zfill(2)+str(time.day).zfill(2)+ "_" \
           +str(time.hour).zfill(2) +str(time.minute//10*10).zfill(2)


def find_name(txt):
    #找到原始信息中货币名称
    if "(" in txt: #如果获取的信息中包含"（"，那么"（"左边的就是货币的姓名
        pos1 = txt.find("(")
        return txt[:pos1]
    else: #如果没有，就把这个字符串打印出来
        pass


def find_symbol(txt):
    #找到原始信息中货币的简称（symbol）
    if "(" in txt and ")" in txt: #如果原始数据里有左右括号，那么返回括号中间的名字
        pos1 = txt.find('(')
        pos2 = txt.rfind(')')
        return txt[pos1+1:pos2]
    else: #如果没有，打印出来
        pass


def get_three_currencies(txt):
    #返回原始信息中包含的兑美元，比特币，以太币汇率
    try:
        pos1 = txt.find("$")     #按照currency返回的字符串中.的位置找到相应的几个汇率
        pos2 = txt.find("B")
        pos3 = txt.find("E")
        to_usd = txt[:pos1 + 8]
        to_btc = txt[pos1 + 8:pos2].strip("\xa0")
        to_eth = txt[pos2+3:pos3].strip("\xa0")
        return [to_usd, to_btc, to_eth]
    except:
        logger.error("Failed When Getting Currency",exc_info = True)
        raise ValueError("Can't Find Currency,Locate EtherScanSpider.get_three_currencies")


def get_data_by_one(address,currency,be_cur):
    #返回一个包含各个代币名称，简称，地址，三个汇率构成的字典的列表
    res = []
    if be_cur == False:
        for addr, curr in zip(address,currency):
            to_usd = float(get_three_currencies(curr.get_text())[0][1:])
            data= {
                "name":find_name(addr.get_text()),
                "symbol":find_symbol(addr.get_text()),
                "address": addr.get("href")[7:],
                "to_usd": to_usd,
                "time": process_time(datetime.now())
            }
            res.append(data)
    else:
        for addr, curr in zip(address,currency):
            to_usd = float(get_three_currencies(curr.get_text())[0][1:])
            data= {
                "name":find_name(addr.get_text()),
                "symbol":find_symbol(addr.get_text()),
                "address": addr.get("href")[7:],
                "to_usd": to_usd,
                "to_btc": to_usd/be_cur["BTC"],
                "to_eth": to_usd/be_cur["ETH"],
                "time": process_time(datetime.now())
            }
            res.append(data)
    return res


def job(url,be_cur):
    #主要请求方法，可以将网络上返回的源代码处理，并最终返回信息列表
    web_data = requests.get(url,timeout = (2,5)) #平均一个页面需要1.3秒，设置链接超时为2秒，读取超时为5秒
    logger.info(web_data)
    #print(web_data) #每次访问页面打印一个响应状态
    soup = BeautifulSoup(web_data.text, "lxml")
    address = soup.select(config.ETH_configs["address_info"])
    currency = soup.select(config.ETH_configs["currency_info"])
    return get_data_by_one(address, currency,be_cur)


def main():
    #主函数，访问ethscan的每个页面，会打印程序运行时间，最后返回包含全部货币信息的列表
    be_cur = btc_eth.main()
    urls = config.ETH_configs["urls"]
    result = []
    for i in range(len(urls)):
        try:
            result.extend(job(urls[i],be_cur))
        except requests.exceptions.ConnectTimeout:
            logger.error("Request Time Out")
            print("Request Time out")
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
            logger.error("Some Error Happened", exc_info=True)
            pass
        continue
    return result


if __name__ == "__main__":
    print(main())


'''
==============================================================================================================================
==============================================================================================================================
'''

be_cur = {"BTC":10,"ETH":5}
def test_find_name(): #测试Find_name，最终会返回"（"左边的字符串
    assert find_name("Bitfinex LEO Token (LEO)") == "Bitfinex LEO Token "
    assert type(find_name("sdklakls")) == type(None)
    assert find_symbol("Bitfinex LEO Token (LEO)") == "LEO"


def test_find_symbol(): #如果字符串里面没有左右括号的话，不返回任何值
    assert type(find_symbol("sdklakls(")) == type(None)


def test_get_three_currencies(): #测试get_three_currencies返回值应该是包含三个字符串的列表
    assert get_three_currencies("$33.75490.0028598313 Btc0.112326 Eth") ==  ['$33.7549','0.0028598313', '0.112326']

@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_job_return(index): #测试job返回的是一个列表，如果有Internet Error，会跳过
    assert type(job("https://etherscan.io/tokens?p=10",be_cur)) ==type([])
    assert len(job("https://etherscan.io/tokens?p=10",be_cur)) > 10
    assert type(job("https://etherscan.io/tokens?p=10",be_cur)[index]) == type({})
    assert len(job("https://etherscan.io/tokens?p=10",be_cur)[index]) == 7

@pytest.mark.parametrize("index",[1,2,3,4,5])
def test_main_return(index): #测试主函数返回的是一个列表
    assert type(main()) == type([])
    assert len(main()) >5
    assert type(main()[index]) == type({})
    assert len(main()[index]) == 7