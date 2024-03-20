import streamlit as st

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="🌍",
    initial_sidebar_state="collapsed",
    # layout="wide",
)

def menu():
    st.sidebar.page_link("page_main.py", label="主页")
    st.sidebar.write("\n  ")
    st.sidebar.title("异常鉴别")
    st.sidebar.page_link("pages/page1.py", label="异常言论鉴别")
    st.sidebar.page_link("pages/page2.py", label="异常用户鉴别")
    st.sidebar.page_link("pages/page3.py", label="异常事件鉴别")
    st.sidebar.title("实时监测")
    st.sidebar.page_link("pages/page4.py", label="实时言论监测")
    st.sidebar.page_link("pages/page5.py", label="实时用户监测")
    st.sidebar.page_link("pages/page6.py", label="实时事件监测")
    st.sidebar.title("模型微调")
    st.sidebar.page_link("pages/page7.py", label="言论模型微调")
    st.sidebar.page_link("pages/page8.py", label="用户模型微调")
    st.sidebar.page_link("pages/page9.py", label="事件模型微调")
def HomePage():
    menu()
    st.markdown('# <center> 🔬Anomaly Detection🔬 </center>', unsafe_allow_html=True)
    st.markdown('### <center> 📝奇思妙想舆情异常监测器📝 </center>', unsafe_allow_html=True)
    st.write("\n  ")
    st.write("\n  ")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col2.button("登录")
    col5.button("注册")

if __name__ == "__main__":
    HomePage()
