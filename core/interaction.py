import sys
sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import pymysql,logging
from datetime import datetime
import time
from spiders import ETH_spider
from spiders import coin_spider
from spiders import EOS_spider
from configs.configs import config
from models import exchange_rate_db
from models import exchange_rating_db


logging.basicConfig(level=config.tutti_configs["local_logging_basic"]["level"],
                    filename=config.tutti_configs["local_logging_basic"]["filename"],
                    datefmt=config.tutti_configs["local_logging_basic"]["datefmt"],
                    format=config.tutti_configs["local_logging_basic"]["format"])
logger = logging.getLogger(__name__)


def extract_from_exchange_rate():
    #从原先的exchange_rate表格中提取信息
    try:
        exchange_rate_data = exchange_rate_db.Exchange_rate()
        return exchange_rate_data.get_all_data()
    except: #如果没有任何信息，就会返回空列表
        logger.error("Unable to Fetch From Original",exc_info = True)
        return []


def match_w_ETH(addr,ETH_result):
    for i in ETH_result:
        if i["address"] == addr:
            return i
    return False


def match_w_EOS(symbol,account,EOS_result):
    for i in EOS_result:
        if i["symbol"] == symbol and i["account"] == account:
            return i
    return False


def match_w_EOS_by_name(symbol,EOS_result):
    for i in EOS_result:
        if i["symbol"] == symbol:
            return i
    return False


def match_w_CoinMKT(symbol,CoinMKT_result):
    for i in CoinMKT_result:
        if i["symbol"] == symbol:
            return i
    return False


def find_account(eos_address):
    pos = eos_address.find("@")
    return eos_address[pos+1:]


def add_info(type,id,deal,key,curr_type,address):
    if type == "Coin":
        deal['id'] = id
        deal['key'] = key
        deal['curr_type'] = curr_type
        deal['address'] = None
        deal['source'] = "CoinMKT"
        deal['type'] = "Coin"
        return deal

    elif type == 'ETH':
        deal['id'] = id
        deal['key'] = key
        deal['curr_type'] = curr_type
        deal['address'] = address
        deal['source'] = "Etherscan"
        deal['type'] = "ETH"
        return deal

    elif type == "EOS":
        deal['id'] = id
        deal['key'] = key
        deal['curr_type'] = curr_type
        deal['address'] = address
        deal['source'] = "EOSPark"
        deal['type'] = "EOS"
        return deal
    else:
        logger.error("Other Types Exist")


def match(CoinMKT,ETH,EOS):
    res = []
    res_multi = []
    alien = []
    local = extract_from_exchange_rate()
    for i in local:
        if i['symbol']== None or i['symbol'] == '':
            deal = match_w_CoinMKT(i["key"],CoinMKT)
            if deal == False:
                alien.append(deal)
            else:
                res.append(add_info("Coin",i['id'],deal,i['key'],i['curr_type'],i['address']))

        elif i["curr_type"] == "ETH":
            deal = match_w_ETH(i["address"],ETH)
            if deal == False:
                alien.append(deal)
            else:
                res.append(add_info("ETH",i['id'],deal,i['key'],i['curr_type'],i['address']))

        elif i["curr_type"] == "EOS":
            deal = match_w_EOS(i["symbol"],find_account(i["address"]),EOS)
            if deal == False:
                alien.append(deal)
            else:
                res.append(add_info("EOS",i['id'],deal,i['key'],i['curr_type'],i['address']))

        else:
            deal = (match_w_CoinMKT(i['symbol'],CoinMKT),match_w_ETH(i['address'],ETH),match_w_EOS_by_name(i['symbol'],EOS))
            if deal == (False,False,False):
                alien.append(deal)
            else:
                if deal[1] == False and deal[2] == False:
                    res.append(add_info("Coin",i['id'],deal[0],i['key'],i['curr_type'],i['address']))
                else:
                    res_multi.append(deal)

    if len(local) == len(res) + len(alien) + len(res_multi):
        logger.info('Number Checked')
    else:
        logger.warning("Number Not Checked")
    return res




def main():
    begin = datetime.now()
    Coin = coin_spider.main()
    ETH = ETH_spider.main()
    EOS = EOS_spider.main()
    data = match(Coin, ETH, EOS)
    rating = exchange_rating_db.Exchange_rating()
    rating.insert_item(data)
    rating.db.close()
    print(len(data))
    end = datetime.now()
    print(datetime.now(), "Exchange_Rating Filled")
    logger.info("Exchange_Rating Filled")
    logger.warning("时间总计" + str(end - begin))
    print("总用时", end - begin)



if __name__ == '__main__':
    main()