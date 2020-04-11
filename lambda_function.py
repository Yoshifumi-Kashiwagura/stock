
from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3
from datetime import datetime
import csv
import pandas as pd

def lambda_handler(event, contxt):
    options = webdriver.ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    driver = webdriver.Chrome(
        executable_path="./bin/chromedriver",
        chrome_options=options
    )

    driver.get("https://kabuoji3.com/stock/1301/2020/")
    tableElem = driver.find_element_by_css_selector(".stock_table.stock_data_table")
    trs = tableElem.find_elements(By.TAG_NAME, "tr")

    for i in range(1,len(trs)):
        tds = trs[i].find_elements(By.TAG_NAME, "td")
        line = ""
        for j in range(0,len(tds)):
            if j < len(tds)-1:
                line += "%s\t" % (tds[j].text)
            else:
                line += "%s" % (tds[j].text)
        print (line+"\r\n")
        with open('/tmp/tmp.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(line)
    driver.close()
    bucket = 'kashiwastock'    # ⑤バケット名を指定
    s3 = boto3.resource('s3')  
#    key = 'test_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'  # ⑥オブジェクトのキー情報を指定
#    file_contents = 'Lambda test'  # ⑦ファイルの内容
#    obj = s3.Object(bucket,key)     # ⑧バケット名とパスを指定
#    obj.put( Body=file_contents )   # ⑨バケットにファイルを出力
    bucket = s3.Bucket('kashiwastock')
    bucket.upload_file('/tmp/tmp.csv', 'stock/tmp.csv')
    pd.read_csv("/tmp/tmp.csv")
    return