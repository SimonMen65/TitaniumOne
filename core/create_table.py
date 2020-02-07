import sys
sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
import pymysql
from datetime import datetime
import logging
from configs.configs import config


logging.basicConfig(level=config.tutti_configs["local_logging_basic"]["level"],
                    filename=config.tutti_configs["local_logging_basic"]["filename"],
                    datefmt=config.tutti_configs["local_logging_basic"]["datefmt"],
                    format=config.tutti_configs["local_logging_basic"]["format"])
logger = logging.getLogger(__name__)



def main():
    db = pymysql.connect(host=config.tutti_configs["local_db"]["host"],
                         port=config.tutti_configs["local_db"]["port"],
                         user=config.tutti_configs["local_db"]["user"],
                         password=config.tutti_configs["local_db"]["passwd"],
                         db=config.tutti_configs["local_db"]["db"])
    cursor = db.cursor()
    cursor.execute(config.main_configs["sql_drop"])
    cursor.execute(config.main_configs["sql_create"])
    db.commit()
    db.close()
    logger.info("New Local_Data Created")

if __name__ == '__main__':
    main()

def test_main(): #判断需要创建的Table存在就可以
    db = pymysql.connect(host=config.tutti_configs["local_db"]["host"],
                         port=config.tutti_configs["local_db"]["port"],
                         user=config.tutti_configs["local_db"]["user"],
                         password=config.tutti_configs["local_db"]["passwd"],
                         db=config.tutti_configs["local_db"]["db"])
    cursor = db.cursor()
    cursor.execute("SELECT table_name FROM information_schema.TABLES WHERE table_name ='Exchange_Rating'")
    db.close()

