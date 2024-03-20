import streamlit as st
from model_user import predict as user_predict, get_uid
from page_main import menu

def page2():
# ------------------------------ 标题_Part -------------------------------
    st.markdown('# <center> 🔬Anomaly Detection🔬 </center>', unsafe_allow_html=True)
    st.markdown('### <center> 📝奇思妙想异常舆情监测器📝 </center>', unsafe_allow_html=True)
    st.write("\n  ")
    st.markdown('##### <center> 异常用户鉴别 </center>', unsafe_allow_html=True)
    st.write("\n  ")
    st.write("\n  ")

# ------------------------------ 输入_Part -------------------------------
    select = st.radio(
    "",
    ('昵称', '用户ID'),index=0, horizontal=True, label_visibility="collapsed")
    if select == '昵称':
        st.text_input('请输入待检测用户昵称 ',key="name",help='监测用户可信度')
    elif select == '用户ID':
        st.text_input('请输入待检测用户uid',key="uid",help='监测用户可信度')
    st.text_input('输入你的Cookie以获取更准确结果',key="cookie",help='F12-网络-获取你的Cookie')

# ------------------------------ 输出_Part -------------------------------
    if st.button('识别🔍'):
        uid = ''
        if select == '昵称':
            if (st.session_state.name).strip() == "":
                st.error('用户昵称不能为空！', icon="🚨")
            else:
                uid = get_uid(st.session_state.name)
        else:
            if (st.session_state.uid).strip() == "":
                st.error('用户uid不能为空！', icon="🚨")
            else:
                uid = (st.session_state.uid).strip()
        cookie = (st.session_state.cookie).strip()
        result = user_predict(uid, cookie)
        if result[0]==-1:
            st.error('啊哦，用户不存在！', icon="🚨")
        elif result[0]==-2:
            st.error('啊哦，查询不到该用户的有效信息', icon="🚨")
        else:
            st.markdown(f"##### <center> 🙊虚假用户概率：{result[0]:6.2f} % </center>", unsafe_allow_html=True)
            st.markdown(f"##### <center> 🤬社交机器人概率：{result[1]:6.2f} % </center>", unsafe_allow_html=True)
            st.markdown(f"##### <center> 🖕违规用户概率：{result[2]:6.2f} % </center>", unsafe_allow_html=True)
            st.markdown(f"##### <center> 😶‍🌫网络水军概率：{result[3]:6.2f} % </center>", unsafe_allow_html=True)
            st.markdown(f"##### <center> 🛡️整体可信度： {result[4]:6.2f} % </center>", unsafe_allow_html=True)


if __name__ == "__main__":
    menu()
    page2()