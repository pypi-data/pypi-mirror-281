from xtquant import xtdata

def init_qmt():
    xtdata.connect()
    # xtdata.download_sector_data()

def get_snapshot():
    stock_list = xtdata.get_stock_list_in_sector('上证A股')
    # xtdata.download_history_data()