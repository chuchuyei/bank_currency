import os
from selenium import webdriver
from tqdm import tqdm
import pandas as pd
import time

path = r'D:\Users\JYJU\Downloads'
try:
    filename = [f for f in os.listdir(path) if 'ExchangeRate@' in f][0]
    os.remove(os.path.join(path, filename))
except Exception:
    pass

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
print(os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
chromedriver = r'D:\Users\JYJU\tools\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)

def transfer_file(kind_of_currency):
    while True:
        try:
            filename = [f for f in os.listdir(path) if 'ExchangeRate@' in f and os.path.splitext(f)[-1] == '.csv'][0]
            break
        except Exception:
            time.sleep(0.1)
    df = pd.read_csv(os.path.join(path, filename))
    df.reset_index(level=0, inplace=True)
    df.dropna(axis=1,inplace=True)
    df.columns = [u'資料日期', u'幣別', 
                  u'買入匯率', u'買入-現金', u'買入-即期', u'買入-遠期10天', u'買入-遠期30天',
                  u'買入-遠期60天', u'買入-遠期90天', u'買入-遠期120天', u'買入-遠期150天', u'買入-遠期180天',
                  u'賣出匯率', u'賣出-現金', u'賣出-即期', u'賣出-遠期10天', u'賣出-遠期30天',
                  u'賣出-遠期60天', u'賣出-遠期90天', u'賣出-遠期120天', u'賣出-遠期150天', u'買入-遠期180天'
                  ]
    df['資料日期'] = pd.to_datetime(df['資料日期'], format='%Y%m%d')
    new_path = r'D:\Code_JYJU\data'
    df.to_csv(os.path.join(new_path, filename[:12] + '_' + str(kind_of_currency) + filename[12:]),index=False)
    os.remove(os.path.join(path, filename))

currency = ['USD', 'HKD', 'GBP', 'AUD',
            'CAD', 'SGD', 'CHF', 'JPY',
            'ZAR', 'SEK', 'NZD', 'THB',
            'PHP', 'IDR', 'EUR', 'KRW',
            'VND', 'MYR', 'CNY',
            ]
with tqdm(total = len(currency)) as pbar:
    for i in currency:
        url = 'http://rate.bot.com.tw/xrt/flcsv/0/l6m/' + str(i)
        browser.get(url)
        transfer_file(i)
        pbar.update()
browser.close()
