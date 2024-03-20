import streamlit as st
from model_event import predict as event_predict
from page_main import menu

def page3():
# ------------------------------ 标题_Part -------------------------------
    st.markdown('# <center> 🔬Anomaly Detection🔬 </center>', unsafe_allow_html=True)
    st.markdown('### <center> 📝奇思妙想异常舆情监测器📝 </center>', unsafe_allow_html=True)
    st.write("\n  ")
    st.markdown('##### <center> 异常事件鉴别 </center>', unsafe_allow_html=True)
    st.write("\n  ")
    st.write("\n  ")
# ------------------------------ 输入_Part -------------------------------
    st.text_input('请输入待检测事件或关键词',key="event",help='监测事件异常程度')
    st.text_input('输入你的Cookie以获取更准确结果',key="cookie",help='F12-网络-获取你的Cookie')

# ------------------------------ 输出_Part -------------------------------
    if st.button('识别🔍'):
        event_data = (st.session_state.event).strip()
        cookie = (st.session_state.cookie).strip()
        result = event_predict(event_data, cookie)
        st.markdown(f"##### <center> 🙊炒作事件概率：{result[0]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 🤬反转事件概率：{result[1]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 🖕热点事件概率：{result[2]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 🛡️整体可信度： {result[3]:6.2f} % </center>", unsafe_allow_html=True)


if __name__ == "__main__":
    menu()
    page3()