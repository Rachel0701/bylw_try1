from keras.models import load_model
import pickle
import numpy as np
from keras import preprocessing
import re
import jieba
import pandas as pd
import logging
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('jieba').setLevel(logging.ERROR)

def change(x):
    if (x<10):
        return x
    elif (x<40):
        return x * 2 # 10~40 -> 0~80
    elif (x<90):
        return 80+(x-40)*0.2 # 40~90 -> 80~90
    else:
        return x

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

# -----------------------------数据预测------------------------------
def predict(text):
    # 加载模型
    tk = pickle.load(open('model/tokenizer_saying.pickle', 'rb'))
    field_model = load_model('model/model_saying.h5')

    text = [txt_cut(text)]
    print(text)
    max_len = 50
    data = tk.texts_to_sequences(text)
    data = np.array(data)
    data = preprocessing.sequence.pad_sequences(data, maxlen=max_len)

    # 调用模型
    out = field_model.predict(data)
    field = np.argmax(out, axis=1)
    r1 = out[0][0][1] * 100
    r2 = out[1][0][1] * 100
    r3 = out[2][0][1] * 100
    r4 = out[3][0][1] * 100
    print("网络谣言概率：", format(r1, '.2f'), '%')
    print("网络暴力概率：", format(r2, '.2f'), '%')
    print("歧视言论概率：", format(r3, '.2f'), '%')
    print("侵权行为概率：", format(r4, '.2f'), '%')
    s = [r1, r2, r3, r4]
    print("整体可信度：", format(100 - max(s), '.2f'), '%')
    s.append(100 - max(s))
    return s



if __name__ == "__main__":
    text = "教皇劝乌克兰要有举白旗的勇气"
    print("检测文本：", text)
    s = predict(text)