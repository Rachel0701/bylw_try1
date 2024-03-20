import streamlit as st
from model_saying import predict as saying_predict
from page_main import menu

def page8():
# ------------------------------ 标题_Part -------------------------------
    st.markdown('# <center> 🔬Anomaly Detection🔬 </center>', unsafe_allow_html=True)
    st.markdown('### <center> 📝奇思妙想异常舆情监测器📝 </center>', unsafe_allow_html=True)
    st.write("\n  ")
    st.markdown('##### <center> 用户模型微调 </center>', unsafe_allow_html=True)

    st.write("\n  ")
    st.write("\n  ")


# ------------------------------ 输入_Part -------------------------------
    st.text_input('请输入用户数据',key="text",help='对用户模型进行微调')

# ------------------------------ 输出_Part -------------------------------
    if st.button('微调🔍'):
        user_data = (st.session_state.text).strip()
        result = saying_predict(user_data)
        st.markdown(f"##### <center> 🙊网络谣言概率：{result[0]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 🤬网络暴力概率：{result[1]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 🖕歧视言论概率：{result[2]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 😶‍🌫侵权行为概率：{result[3]:6.2f} % </center>", unsafe_allow_html=True)
        st.markdown(f"##### <center> 🛡️整体可信度： {result[4]:6.2f} % </center>", unsafe_allow_html=True)


if __name__ == "__main__":
    menu()
    page8()