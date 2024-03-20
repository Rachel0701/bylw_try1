from keras.models import load_model
import pickle
import numpy as np
from keras import preprocessing
import re
import jieba
import requests
import json
import time
import random
import logging
import os
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

#------------------------------获取用户uid------------------------------
def get_uid(nickname):
    try:
        res = json.loads(requests.get(
            f'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{nickname}&page_type=searchall',
            timeout=1).text)
        try:
            uid = res['data']['cards'][0]['card_group'][0]['user']['id']
        except:
            uid = res['data']['cards'][0]['card_group'][0]['users'][0]['id']
        return uid
    except Exception as e:
        print(e)
        return np.NAN

#------------------------------爬取用户微博------------------------------
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
           'Connection': 'keep-alive0'}
session = requests.Session()
def reptile_userweibo(uid):
    N = 0
    text_content = []
    weibo_url = "https://weibo.com/ajax/statuses/mymblog?uid="+str(uid)+"&page=1&feature=0"
    time.sleep(random.randint(1,4))
    for page in range(1, 10):
        try:
            resp = session.get(weibo_url, headers=headers).content
            resp = json.loads(resp)
            since_id = resp["data"]["since_id"]
            weibo_list = resp["data"]["list"]
            for weibo in weibo_list:
                N += 1
                text = weibo["text_raw"].replace(',', '，').replace('\n', '')
                text_content.append(text)
            print("Page:", page, ", all weibos:", N)
            # time.sleep(random.randint(1,2))
            print(1)
            weibo_url = "https://weibo.com/ajax/statuses/mymblog?uid=" + str(uid) + "&page=" + str(
                page + 1) + "&since_id=" + since_id
        except:
            if page == 1:
                print("The user is not exist!")
                return ["No user"]
            else:
                break

    if N > 0:
        print(f"Have reptiled {N} weibos.")
        return text_content
    else:
        print("The user has no weibo")
        return ['No weibo']


#-----------------------------加载模型------------------------------
tk = pickle.load(open('model/tokenizer_saying.pickle', 'rb'))
user_model = load_model('model/model_user.h5')

#-----------------------------数据预测------------------------------
def predict(uid, Cookie):
    if len(Cookie)>0:
        headers['Cookie'] = Cookie
    print("检测用户uid：",uid)
    text_content = reptile_userweibo(uid)
    if text_content[0]=='No weibo':
        return [-2]
    elif text_content[0]=='No user':
        return [-1]
    # print(text_content)
    text = ''
    for t in text_content:
        text += txt_cut(t)
    print(text)
    if (len(text)==0):
        return [-1] # 没有有效微博
    max_len = 500
    data = tk.texts_to_sequences(text)
    data = np.array(data)
    data = preprocessing.sequence.pad_sequences(data, maxlen=max_len)

    # 调用模型
    out = user_model.predict(data)
    field = np.argmax(out, axis=1)
    r1 = out[0][0][1]*100
    r2 = out[1][0][1]*100
    r3 = out[2][0][1]*100
    r4 = out[3][0][1]*100
    print("虚假用户概率：", format(r1, '.2f'), '%')
    print("社交机器人概率：", format(r2, '.2f'), '%')
    print("违规用户概率：", format(r3, '.2f'), '%')
    print("网络水军概率：", format(r4, '.2f'), '%')
    s = [r1,r2,r3,r4]
    print("整体可信度：", format(100-max(s), '.2f'), '%')
    s.append(100 - max(s))
    return s

if __name__ == "__main__":
    uid = "3204030340"
    Cookie = 'UOR=,,login.sina.com.cn; SINAGLOBAL=3056619161507.6167.1702989076722; SCF=AtXc8RHEcCo3U61Im-Ib1azeOGor7DximBJGLHEkl7nQqyi4r2mTnvjE1IRFMLvpheQHej95sOqOn9Zhimd6tos.; ULV=1710560381307:14:6:3:7647649124847.022.1710560381293:1710157983036; XSRF-TOKEN=vNTQVFoMANI1Lq5hNhwHe0QY; ALF=1713368516; SUB=_2A25I_BCTDeRhGeNO4lcR8yvEwzSIHXVocCxbrDV8PUJbkNAGLXH-kW1NTrGZdgVXeDThhkj4pvouvd5FCGeDQayJ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhhlXEk-6CQ9MfX0FcCJpvl5JpX5KMhUgL.Fo-71K-7e0-R1hn2dJLoIXeLxK-LBK-L1hMLxKqL1h5L1-BLxK-LBKqL1K.LxKqL1heLBoeLxK-LB.eLBK5LxK.L1-eL1h2LxKMLB.-L128keKn4; WBPSESS=uKojIli8KfTYUjluM9RcxeR4spusdj91ek7sFvZPFdlp1X6sNiLx4rZEazg9J6JxDa58QskBXh9edI1EGbkzgoDHO1x_UCebQhhW4dHecwu9NykemaxSsm5jsLxOLCDIMA4vVZWBqNGc9ld5UZOppg=='
    print("检测用户：", uid)
    s = predict(uid, Cookie)