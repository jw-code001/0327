import streamlit as st
import os

def render_sidebar_profile():
    # 메뉴 코드는 지우고, 구분선부터 시작합니다.
    st.sidebar.markdown("---") 
    
    # 사진 표시
    image_path = "./my_photo.jpg" 
    if os.path.exists(image_path):
        st.sidebar.image(image_path, use_container_width=True)
    
    # 내 이력 소개
    st.sidebar.markdown("""
    **👨‍💻 주요 역량 및 자격**
    *   🐍 **Python, 데이터 시각화 제공**
    *   🏠 **공인중개사** / 💰 **전산세무 1급**
    *   🇯🇵 **일본어 통번역**
    """)