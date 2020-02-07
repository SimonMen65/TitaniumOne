# coding: utf-8
import sys
import os

class Config(object):
    DEBUG = False
    def __getitem__(self, key):
        return self.__getattribute__(key)

class DevelopmentConfig(Config):
    ETH_configs = {
        "urls": ["https://etherscan.io/tokens?p=" + \
                 str(n) for n in range(1, 20)],  # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值20
        "address_info": "div.media-body >h3 >a",
        "currency_info": "td.text-nowrap",
        "sql_drop": "DROP TABLE IF EXISTS DataETHScan",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataETHScan ( 
                 Id INT, Name CHAR(128),
                 Symbol CHAR(30), Address CHAR(255),
                 To_usd FLOAT, To_btc FLOAT, 
                 To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataETHScan (Name,Symbol,Address, To_usd, To_btc, To_eth, Time)
                                             VALUES (%s,%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句
        "sql_insert_exception": """INSERT INTO DataETHScan (Name,Symbol,Address, To_usd, Time)
                                                             VALUES (%s,%s,%s,%s,%s)""",

    }

    EOS_configs = {
        "urls": ["https://eospark.com/api/v2/tokens?token_name=&page=" + str(n) + \
                 "&size=20&sort_field=total&sort_order=descend" for n in range(1, 30)],
        # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值203,一般使用30即可
        "sql_drop": "DROP TABLE IF EXISTS DataEOSPark",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataEOSPark ( 
                 Id INT, Name CHAR(128),
                 Symbol CHAR(30), Account CHAR(255),
                 To_usd FLOAT, To_btc FLOAT, 
                 To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataEOSPark 
                        (Symbol, Account, To_usd,To_btc, To_eth,Time)
                         VALUES (%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句
    }

    CoinMKT_configs = {
        "urls": ["https://coinmarketcap.com/" + str(n) for n in range(1, 24)],  # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值24
        "name_info": "td.currency-name >a",  # 网站源代码名称检索位置
        "price_info": "td.text-right >a.price",  # 网站源代码价格检索位置
        "symbol_info": "td.currency-name >span >a",  # 网站源代码简称检索位置
        "sql_drop": "DROP TABLE IF EXISTS DataCoinMKT",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataCoinMKT ( 
                 Id INT, Name CHAR(128),
                 Symbol CHAR(30), Address CHAR(255),
                 To_usd FLOAT, To_btc FLOAT, 
                 To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataCoinMKT 
                        (Name,Symbol,To_usd,To_btc, To_eth,Time)
                         VALUES (%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句

    }

    Obtain_configs = {
        "url": "https://coinmarketcap.com/1",
        "curr_name": "td.currency-name >a",
        "curr_price": "td.text-right >a.price",
        "curr_symbol": "td.currency-name >span >a",

    }

    API_configs = {
        "sql_select": "select * from Exchange_Rating where symbol = %s"
    }
    tutti_configs = {
        "local_logging_basic": {
            "level": "INFO",
            "filename": '/Users/simonmenn/Desktop/Data_v4/output.log',
            "datefmt": '%Y/%m/%d %H:%M:%S',
            "format": '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
        "local_logging_web": {
            "level": "INFO",
            "filename": '/Users/simonmenn/Desktop/Data_v4/web_output.log',
            "datefmt": '%Y/%m/%d %H:%M:%S',
            "format": '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
        "local_db": {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "passwd": "simon0605!",
            "db": "Currency_Test"
        }
    }

class ProductionConfig(Config):
    ETH_configs = {
        "urls": ["https://etherscan.io/tokens?p=" + \
                 str(n) for n in range(1, 20)],  # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值20
        "address_info": "div.media-body >h3 >a",
        "currency_info": "td.text-nowrap",
        "sql_drop": "DROP TABLE IF EXISTS DataETHScan",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataETHScan ( 
                     Id INT, Name CHAR(128),
                     Symbol CHAR(30), Address CHAR(255),
                     To_usd FLOAT, To_btc FLOAT, 
                     To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataETHScan (Name,Symbol,Address, To_usd, To_btc, To_eth, Time)
                                                 VALUES (%s,%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句
        "sql_insert_exception": """INSERT INTO DataETHScan (Name,Symbol,Address, To_usd, Time)
                                                                 VALUES (%s,%s,%s,%s,%s)""",

    }

    EOS_configs = {
        "urls": ["https://eospark.com/api/v2/tokens?token_name=&page=" + str(n) + \
                 "&size=20&sort_field=total&sort_order=descend" for n in range(1, 30)],
        # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值203,一般使用30即可
        "sql_drop": "DROP TABLE IF EXISTS DataEOSPark",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataEOSPark ( 
                     Id INT, Name CHAR(128),
                     Symbol CHAR(30), Account CHAR(255),
                     To_usd FLOAT, To_btc FLOAT, 
                     To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataEOSPark 
                            (Symbol, Account, To_usd,To_btc, To_eth,Time)
                             VALUES (%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句
    }

    CoinMKT_configs = {
        "urls": ["https://coinmarketcap.com/" + str(n) for n in range(1, 24)],  # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值24
        "name_info": "td.currency-name >a",  # 网站源代码名称检索位置
        "price_info": "td.text-right >a.price",  # 网站源代码价格检索位置
        "symbol_info": "td.currency-name >span >a",  # 网站源代码简称检索位置
        "sql_drop": "DROP TABLE IF EXISTS DataCoinMKT",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataCoinMKT ( 
                     Id INT, Name CHAR(128),
                     Symbol CHAR(30), Address CHAR(255),
                     To_usd FLOAT, To_btc FLOAT, 
                     To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataCoinMKT 
                            (Name,Symbol,To_usd,To_btc, To_eth,Time)
                             VALUES (%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句

    }

    Obtain_configs = {
        "url": "https://coinmarketcap.com/1",
        "curr_name": "td.currency-name >a",
        "curr_price": "td.text-right >a.price",
        "curr_symbol": "td.currency-name >span >a",

    }


    API_configs = {
        "sql_select": "select * from Exchange_Rating where symbol = %s"
    }
    tutti_configs = {
        "local_logging_basic": {
            "level": "INFO",
            "filename": '/Users/simonmenn/Desktop/Data_v4/output.log',
            "datefmt": '%Y/%m/%d %H:%M:%S',
            "format": '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
        "local_logging_web": {
            "level": "INFO",
            "filename": '/Users/simonmenn/Desktop/Data_v4/web_output.log',
            "datefmt": '%Y/%m/%d %H:%M:%S',
            "format": '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
        "local_db": {
        "host":'rm-8vb68f7gdz7ficbt1o.mysql.zhangbei.rds.aliyuncs.com',
        'port': 3200,
        'user':'bitdesk',
        'passwd':'TestNode-Bitdesk$118118',
        'db':'bitdesk'
        },
    }

class TestConfig(Config):
    ETH_configs = {
        "urls": ["https://etherscan.io/tokens?p=" + \
                 str(n) for n in range(1, 2)],  # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值20
        "address_info": "div.media-body >h3 >a",
        "currency_info": "td.text-nowrap",
        "sql_drop": "DROP TABLE IF EXISTS DataETHScan",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataETHScan ( 
                     Id INT, Name CHAR(128),
                     Symbol CHAR(30), Address CHAR(255),
                     To_usd FLOAT, To_btc FLOAT, 
                     To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataETHScan (Name,Symbol,Address, To_usd, To_btc, To_eth, Time)
                                                 VALUES (%s,%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句
        "sql_insert_exception": """INSERT INTO DataETHScan (Name,Symbol,Address, To_usd, Time)
                                                                 VALUES (%s,%s,%s,%s,%s)""",

    }

    EOS_configs = {
        "urls": ["https://eospark.com/api/v2/tokens?token_name=&page=" + str(n) + \
                 "&size=20&sort_field=total&sort_order=descend" for n in range(1, 3)],
        # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值203,一般使用30即可
        "sql_drop": "DROP TABLE IF EXISTS DataEOSPark",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataEOSPark ( 
                     Id INT, Name CHAR(128),
                     Symbol CHAR(30), Account CHAR(255),
                     To_usd FLOAT, To_btc FLOAT, 
                     To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataEOSPark 
                            (Symbol, Account, To_usd,To_btc, To_eth,Time)
                             VALUES (%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句
    }

    CoinMKT_configs = {
        "urls": ["https://coinmarketcap.com/" + str(n) for n in range(1, 2)],  # 数据来源网址,改变范围可以获取完整数据或测试数据，最大值24
        "name_info": "td.currency-name >a",  # 网站源代码名称检索位置
        "price_info": "td.text-right >a.price",  # 网站源代码价格检索位置
        "symbol_info": "td.currency-name >span >a",  # 网站源代码简称检索位置
        "sql_drop": "DROP TABLE IF EXISTS DataCoinMKT",  # 删除先前表格sql语句
        "sql_create": """CREATE TABLE DataCoinMKT ( 
                     Id INT, Name CHAR(128),
                     Symbol CHAR(30), Address CHAR(255),
                     To_usd FLOAT, To_btc FLOAT, 
                     To_eth FLOAT, Time CHAR(100))""",  # 创建表格sql语句
        "sql_insert": """INSERT INTO DataCoinMKT 
                            (Name,Symbol,To_usd,To_btc, To_eth,Time)
                             VALUES (%s,%s,%s,%s,%s,%s)""",  # 填充表格sql语句

    }

    Obtain_configs = {
        "url": "https://coinmarketcap.com/1",
        "curr_name": "td.currency-name >a",
        "curr_price": "td.text-right >a.price",
        "curr_symbol": "td.currency-name >span >a",

    }

    API_configs = {
        "sql_select": "select * from Exchange_Rating where symbol = %s"
    }

    tutti_configs = {
        "local_logging_basic": {
            "level": "INFO",
            "filename": '/Users/simonmenn/Desktop/Data_v4/output.log',
            "datefmt": '%Y/%m/%d %H:%M:%S',
            "format": '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
        "local_logging_web": {
            "level": "INFO",
            "filename": '/Users/simonmenn/Desktop/Data_v4/web_output.log',
            "datefmt": '%Y/%m/%d %H:%M:%S',
            "format": '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
        "local_db": {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "passwd": "simon0605!",
            "db": "Currency_Test"
        },
    }

mapping = {
    'dev':DevelopmentConfig,
    'pro':ProductionConfig,
    'test':TestConfig,
    'default':DevelopmentConfig
}


num = len(sys.argv)-1
if num!= 1:
    #exit("参数错误,必须传环境变量!比如: python xx.py dev|pro|default")
    app_env = 'default'
    config = mapping[app_env]()
else:
    env = sys.argv[1]
    app_env = os.environ.get('app_env',env).lower()
    config = mapping[app_env]()

