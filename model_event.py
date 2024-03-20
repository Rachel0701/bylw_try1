from keras.models import load_model
import pickle
import numpy as np
from keras import preprocessing
import re
import jieba
import requests
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import logging
import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('jieba').setLevel(logging.ERROR)

#------------------------------分词------------------------------
fs = open("data/stoplist.txt", 'r', encoding='utf-8')
stoplist = fs.read()
stoplist = stoplist.split('\n')
def txt_cut(text):
    text = re.sub(u'[^\u4e00-\u9fa5]', '', text)
    words = jieba.lcut(text, cut_all=False)  # 精确模式
    new_text = ""
    for w in words:
        if (w not in stoplist and len(w) > 1):
            new_text += w + ' '
    return new_text

#------------------------------爬取用户微博------------------------------
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
           'Connection': 'keep-alive0'}
session = requests.Session()
firefox_options = Options()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')
driver = webdriver.Firefox(options=firefox_options)
start=time.perf_counter()

def reptile_eventweibo(event):
    contents = []
    N = 0
    for page in range(1, 10):
        driver.get(f"https://s.weibo.com/weibo?q={event}&page={str(page)}")
        time.sleep(3)
        elements = driver.find_elements(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div[1]/div[2]/div")
        if len(elements) == 0:
            elements = driver.find_elements(By.XPATH,"/html/body/div[1]/div[2]/div/div[2]/div[1]/div[4]/div")
            if len(elements) == 0:
                break
        for ele in elements:
            try:
                content = ele.find_element(By.XPATH,"./div/div[1]/div[2]/p[1]").text
                content = content.replace(',', '').replace('\n', '')
                if (content in contents):
                    continue
                N += 1
                contents.append(content)
                print("No.", N, "content:", content)
            except:
                pass

    if N>0:
        return contents
    else:
        return ["No weibo"]


#-----------------------------加载模型------------------------------
tk = pickle.load(open('model/tokenizer_saying.pickle', 'rb'))
user_model = load_model('model/model_event.h5')

#-----------------------------数据预测------------------------------
def predict(event, cookie):
    headers['Cookie'] = cookie
    print("检测事件：",event)
    text_content = reptile_eventweibo(event)
    print(text_content)
    text = ''
    for t in text_content:
        text += txt_cut(t)
    print(text)
    max_len = 2000
    data = tk.texts_to_sequences(text)
    data = np.array(data)
    data = preprocessing.sequence.pad_sequences(data, maxlen=max_len)

    # 调用模型
    out = user_model.predict(data)
    field = np.argmax(out, axis=1)
    r1 = out[0][0][1]*100
    r2 = out[1][0][1]*100
    r3 = out[2][0][1]*100
    print("炒作事件概率：", format(r1, '.2f'), '%')
    print("反转事件概率：", format(r2, '.2f'), '%')
    print("热点事件概率：", format(r3, '.2f'), '%')
    s = [r1,r2,r3]
    print("整体可信度：", format(100-max(s), '.2f'), '%')
    s.append(100-max(s))
    return s

if __name__ == "__main__":
    event = "浙江"
    cookie = 'UOR=,,login.sina.com.cn; SINAGLOBAL=3056619161507.6167.1702989076722; SCF=AtXc8RHEcCo3U61Im-Ib1azeOGor7DximBJGLHEkl7nQqyi4r2mTnvjE1IRFMLvpheQHej95sOqOn9Zhimd6tos.; ALF=1713443909; SUB=_2A25I_fcVDeRhGeFK7lUQ-C3EzjqIHXVoc3bdrDV8PUJbkNAGLXnwkW1NQykrGRcSjTUc1Eqw_d_hP3CCsGp_PUDz; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWL10zFF0_wmT4FVHJv6-df5JpX5KMhUgL.FoMXSKMp1heRSKq2dJLoI0YLxK-LBK-L1hMLxKqL1h5L1-BLxK-LBKqL1K.LxKqL1heLBoeLxK-LB.eLBK5LxK.L1-eL1h2LxKMLB.-L122t; XSRF-TOKEN=db8g0MK6qxfQDFqgvYT3R0B3; _s_tentry=weibo.com; Apache=4367608314028.0796.1710863176101; ULV=1710863176191:18:10:4:4367608314028.0796.1710863176101:1710858922534; WBPSESS=PuoeF5nLUrWcRk_lox86y-trS1AIRv9fFM5kjReCW8XwYUYY6OMyFxWFv96TvjNsrAMd42-9jhQ9PFIHdGnVZ-TZ-WvtcFeEQkfhrgsntj21Mdsu9LggHZKRGTj-mTIxZKLkLYWhyxe15NmphaAuuA=='
    s = predict(event, cookie)
