import sys
#sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import pymysql
from configs.configs import config

sql = {
        "sql_drop": "DROP TABLE IF EXISTS Exchange_Rating",
        "sql_create": """CREATE TABLE Exchange_Rating ( 
                     Id INT, Key_ VARCHAR(255),
                     Curr_Type  VARCHAR(45), Symbol VARCHAR(45),
                     Address VARCHAR(255), To_usd FLOAT,
                     To_btc FLOAT,  To_eth FLOAT,  
                     Time CHAR(100), Source CHAR(20) )""",
        "sql_insert": """INSERT INTO Exchange_Rating (Id,Key_,Curr_Type ,Symbol ,Address, To_usd, Time, Source)
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        "sql_insert_coin": """INSERT INTO Exchange_Rating (Id,Key_,Curr_Type, Symbol ,To_usd, Time, Source)
                             VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        "sql_insert_coin_w_be": """INSERT INTO Exchange_Rating (Id,Key_,Curr_Type, Symbol ,To_usd, To_btc, To_eth, Time, Source)
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        "sql_insert_w_be": """INSERT INTO Exchange_Rating (Id,Key_,Curr_Type ,Symbol ,Address, To_usd, To_btc, To_eth, Time, Source)
                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        "sql_select": "select * from Exchange_Rating where symbol = %s"
    }




class Exchange_rating(object):

    def __init__(self):
        self.db = pymysql.connect(host=config.tutti_configs["local_db"]["host"],
                         port=config.tutti_configs["local_db"]["port"],
                         user=config.tutti_configs["local_db"]["user"],
                         password=config.tutti_configs["local_db"]["passwd"],
                         db=config.tutti_configs["local_db"]["db"])
        self.cursor = self.db.cursor()

    def insert_item(self,data):
        for i in data:
            if "to_btc" in i.keys() and "to_eth" in i.keys():
                if i['type'] == "Coin":
                    param = (i['id'], i['key'], i['curr_type'], i['symbol'], i['address'],
                             i['to_usd'], i['to_btc'], i['to_eth'], i['time'], i['source'])
                    self.cursor.execute(sql['sql_insert_w_be'], param)
                    self.db.commit()
                else:
                    param = (i['id'], i['key'], i['curr_type'], i['symbol'], i['address'],
                             i['to_usd'], i["to_btc"], i["to_eth"], i['time'], i['source'])
                    self.cursor.execute(sql["sql_insert_w_be"], param)
                    self.db.commit()
            else:
                if i["type"] == "Coin":
                    param = (i['id'], i['key'], i['curr_type'], i["symbol"], i["to_usd"], i["time"], i["source"])
                    self.cursor.execute(sql["sql_insert_coin"], param)
                    self.db.commit()
                else:
                    param = (i['id'], i['key'], i['curr_type'], i['symbol'], i['address'],
                             i['to_usd'], i['time'], i['source'])
                    self.cursor.execute(sql["sql_insert"], param)
                    self.db.commit()

    def formatter(self,tupp):
        result = []
        for i in tupp:
            res = {}
            res['symbol'] = i[3]
            res['to_usd'] = i[5]
            res['to_btc'] = i[6]
            res['to_eth'] = i[7]
            res['time'] = i[8]
            result.append(res)
        return result

    def get_all_data(self,param):
        self.cursor.execute(sql['sql_select'],param)
        tupps = self.cursor.fetchall()
        return self.formatter(tupps)


if __name__ == '__main__':
    data=[{'id':100,'key':'test','curr_type':'test','address':'0x0000','symbol':'Test','to_usd':1.01,
          'to_btc':2.02,'to_eth':3.03,'time':2019,'source':'test_source','type':'Coin'}]
    rating = Exchange_rating()
    #rating.insert_item(data)
    print(rating.get_all_data("BTC"))
