import schedule
import time
from xtquant import xtdata
import logging

def update_progress(progress):
    '''进度条'''
    bar_length = 40  # 进度条长度
    block = int(round(bar_length * progress))
    text = f"\r[{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
    if progress < 1:
        print(text, end='', flush=True)
    else:
        print(text, flush=True)

# 补充历史数据
def download(stock_list, period):
    logging.info('补充历史数据')

    def callback(data):
        """
        回调函数，更新下载进度。
        """
        update_progress(data['finished'] / data['total'])
        
        # if data['finished'] >= data['total']:
        #     event.set()

    xtdata.download_history_data2(stock_list=stock_list, period=period, callback=callback, incrementally=True)

    return

def scheduler_download():
    stock_list = xtdata.get_stock_list_in_sector('沪深A股')
    download(stock_list=stock_list, period='1d')
    

def init_scheduler():

    # 安排任务在每天的15:10运行
    schedule.every().day.at("15:10").do(scheduler_download)
    
    while True:
        schedule.run_pending()
        time.sleep(1)