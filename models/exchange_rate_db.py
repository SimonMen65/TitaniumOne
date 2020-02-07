import sys
#sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import pymysql
from configs.configs import config

sql = {
    "Select_Everything":""" select * from exchange_rate """
}

class Exchange_rate(object):

    def __init__(self):
        self.db = pymysql.connect(host=config.tutti_configs["local_db"]["host"],
                         port=config.tutti_configs["local_db"]["port"],
                         user=config.tutti_configs["local_db"]["user"],
                         password=config.tutti_configs["local_db"]["passwd"],
                         db=config.tutti_configs["local_db"]["db"])
        self.cursor = self.db.cursor()

    def format_processor(self,tupp):
        result = []
        for i in tupp:
            res = {}
            res["id"] = i[0]
            res["key"] = i[1]
            res["curr_type"] = i[2]
            res["symbol"] = i[3]
            res["address"] = i[4]
            res["to_btc"] = i[5]
            res["to_usd"] = i[6]
            result.append(res)
        return result

    def get_all_data(self):
        self.cursor.execute(sql["Select_Everything"])
        tup_data = self.cursor.fetchall()
        return self.format_processor(tup_data)


if __name__ == '__main__':
    ex_rate = Exchange_rate()
    print(ex_rate.get_all_data())