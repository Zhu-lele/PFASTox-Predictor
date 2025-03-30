import streamlit as st
import pandas as pd

# 设置 Streamlit 页面主题
st.set_page_config(page_title="PFASTox Database", layout="wide")

# 数据文件地址（raw GitHub 链接）
file_url = "https://raw.githubusercontent.com/Zhu-lele/PFASTox-Predictor/main/PFAS_toxicity_data.xlsx"

# 页面样式（天蓝色为主）
page_style = """
    <style>
        body { background-color: #87CEEB; }
        .title-large { font-size: 26px; font-weight: bold; text-align: center; color: #00008B; margin-bottom: 40px; }
        .description-box { font-size: 22px; text-align: center; color: #00008B; margin-bottom: 30px; }
        .contact-box { font-size: 16px; text-align: center; color: #ffffff; background-color: #00008B; padding: 15px; border-radius: 10px; margin-top: 30px; }
        section[data-testid="stSidebar"] { background-color: #87CEEB !important; }
        section[data-testid="stSidebar"] * { font-size: 24px !important; color: #ffffff !important; }
        section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] select,
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] div[data-testid="stSelectboxLabel"] {
            color: #00008B !important; font-weight: bold !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="select"] div {
            color: #00008B !important; font-weight: bold !important;
        }
        section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] select {
            height: 50px !important; font-size: 20px !important; padding: 10px !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stSelectboxLabel"] {
            font-size: 18px !important; font-weight: bold !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="select"] div {
            font-size: 18px !important; font-weight: bold !important;
        }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 页面导航
page = st.sidebar.radio("", ["主页", "数据预览", "数据筛选"])

# 主页
if page == "主页":
    st.markdown('<div class="title-large">🌊 欢迎来到 PFAS Toxicity Database 🌍</div>', unsafe_allow_html=True)
    st.markdown('<div class="description-box">PFASTox Database中包含了约5000种PFAS对4种鱼类的生态毒性数据</div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Zhu-lele/PFASTox-Predictor/main/model_diagram.png", use_container_width=True)
    st.markdown("""
        <div class="contact-box">
            本数据库由大连理工大学 李雪花教授课题组 开发<br>
            如有任何问题，欢迎联系我们 📧 <b>Zhu_lll@163.com</b>
        </div>
    """, unsafe_allow_html=True)

# 数据预览
elif page == "数据预览":
    st.markdown('<div class="title-large">🔬 毒性数据预览</div>', unsafe_allow_html=True)
    try:
        df = pd.read_excel(file_url)
        st.write("### 📊 全部数据")
        st.dataframe(df, height=600)
    except Exception as e:
        st.error(f"❌ 数据加载失败: {e}")

# 数据筛选
elif page == "数据筛选":
    st.markdown('<div class="title-large">🔍 数据筛选</div>', unsafe_allow_html=True)
    try:
        df = pd.read_excel(file_url)
        st.sidebar.markdown('<div class="sidebar-title">🔍 输入筛选条件</div>', unsafe_allow_html=True)

        # 可筛选字段
        filter_column = st.sidebar.selectbox("选择筛选列", ["Chemicals", "CAS", "SMILES", "Species"])
        input_value = st.sidebar.text_input(f"请输入 {filter_column} 值")
        dropdown_value = st.sidebar.selectbox(f"或从 {filter_column} 中选择", [""] + list(df[filter_column].dropna().unique()))
        selected_value = input_value if input_value else dropdown_value

        if selected_value:
            filtered_df = df[df[filter_column].astype(str).str.contains(selected_value, case=False, na=False)]
            st.write(f"### 筛选结果 - {filter_column}: {selected_value}")
            st.dataframe(filtered_df, height=600)
            csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 下载筛选数据 (CSV)", data=csv_filtered, file_name="filtered_data.csv", mime="text/csv")
        else:
            st.info("请填写或选择筛选条件。")
    except Exception as e:
        st.error(f"❌ 数据加载失败: {e}")
