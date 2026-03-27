import streamlit as st
import pandas as pd
# 데이터 관리 모듈
from modules.data_manager import SheetManager
# 시각화 모듈
from modules.visualizer import SkinVisualizer
# 페이지 UI 모듈
from pages.form.normal import show_normal_form
from pages.about.me import render_sidebar_profile

# --- [규칙] 페이지 설정은 가장 맨 위에 딱 한 번만! ---
st.set_page_config(page_title="Skin AI Analysis", layout="wide")

# --- [함수 1] 구글 응답 결과 요약 보고서 ---
def render_business_summary(df):
    st.subheader("📝 문항별 응답 요약 (Top Selection)")    
    if df.empty:
        st.info("데이터가 충분하지 않습니다.")
        return

    summary_list = []
    for i in range(1, len(df.columns)):
        col_name = df.columns[i]
        # 주관식 키워드 판별
        if "주로 사용" in col_name or "바라는 점" in col_name:
            top_val = "주관식 응답"
            count = f"{df[col_name].nunique()}개의 의견"
        else:
            # 콤마로 연결된 다중 응답 처리
            series = df[col_name].astype(str).str.split(', ').explode()
            top_choice = series.value_counts()
            top_val = top_choice.index[0] if not top_choice.empty else "-"
            count = f"{top_choice.values[0]}명" if not top_choice.empty else "0명"

        summary_list.append({
            "문항": f"Q{i}",
            "내용": col_name[:25] + "...",
            "최다 답변": top_val,
            "수치": count
        })
    st.table(pd.DataFrame(summary_list))

# --- [함수 2] 시각화 대시보드 ---
def render_visual_dashboard(df):
    st.subheader("📊 실시간 데이터 시각화")
    viz = SkinVisualizer(df)
    col1, col2 = st.columns(2)
    with col1: viz.plot_target_distribution()
    with col2: viz.plot_skin_concerns()
    st.divider()
    viz.plot_visit_vs_reason()

# --- 메인 실행부 ---
def main():
    # [에러 해결 지점] try - except 구문을 완성합니다.
    try:
        db = SheetManager()
        df = db.get_all_responses_df()
    except Exception as e:
        # 에러가 나면 화면에 빨간 메시지를 띄우고 빈 표(DataFrame)를 만듭니다.
        st.error(f"데이터 로드 중 오류 발생: {e}")
        df = pd.DataFrame() 

    # 🧭 사이드바 설정
    st.sidebar.title("🧭 Navigation")
    menu = st.sidebar.selectbox("Go to", ["Home", "Normal Survey", "AI Prediction"])

    # 사이드바 하단: 깃허브 링크 및 프로필
    st.sidebar.markdown("---")
    st.sidebar.link_button("🚀 My GitHub 바로가기", "https://github.com/jw-code001/0327")
    
# 3. 사이드바 - 프로필 호출 (me.py의 함수 실행)
    # 이제 me.py에는 메뉴 코드가 없으므로 충돌이 나지 않습니다.
    render_sidebar_profile()

    # 메뉴별 화면 출력
    if menu == "Home":
        st.write("# 🏠 Dashboard Home")
        if not df.empty:
            render_business_summary(df)
            st.divider()
            render_visual_dashboard(df)
        else:
            st.info("수집된 데이터가 없습니다. 설문을 진행해 주세요.")
            
    elif menu == "Normal Survey":
        show_normal_form()

    elif menu == "AI Prediction":
        st.write("## 🤖 AI 분석 리포트 (준비 중)")

if __name__ == "__main__":
    main()