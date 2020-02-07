import sys
sys.path.append("/Users/simonmenn/Desktop/Data_v4/")
from datetime import datetime
import time
from core import interaction
import logging
from configs.configs import config

logging.basicConfig(level=config.tutti_configs["local_logging_basic"]["level"],
                    filename=config.tutti_configs["local_logging_basic"]["filename"],
                    datefmt=config.tutti_configs["local_logging_basic"]["datefmt"],
                    format=config.tutti_configs["local_logging_basic"]["format"])
logger = logging.getLogger(__name__)

def process_time(time):
    ##返回一个符合mysql语法的时间字符￿￿￿￿￿￿，分钟向下取整至十分钟
    return str(time.year)+ str(time.month).zfill(2)+str(time.day).zfill(2)+ "_" \
           +str(time.hour).zfill(2) +str(time.minute//10*10).zfill(2)


def self_check():
    #自检函数，程序只在每个十分钟开始的时候才运行
    now = datetime.now()
    if now.minute%10 < 4:
        pass
    else:
        print("Waiting")
        time.sleep((10-now.minute%10)*60)


def main():
    Run = True
    self_check()
    store_min = process_time(datetime.now())
    interaction.main()
    logger.warning("One Round Finished")
    while Run:
        nowtime = datetime.now()
        if process_time(nowtime) != store_min:
            try:
                interaction.main()
                store_min = process_time(datetime.now())
                logger.warning("One Round Finished")
            except:
                logger.error("Some Error Happened", exc_info=True)
                pass
        else:
            time.sleep(10)



if __name__ == '__main__':
    main()
