import streamlit as st
import pandas as pd
import random
import os
import pydeck as pdk # 지도 시각화를 위해 필요합니다 (pyproject.toml에 추가 필요)
import plotly.express as px
import plotly.graph_objects as go
from tracker_web import log_app_usage
from supabase import create_client, Client
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_folium import folium_static


# --- [1] 데이터 로직: 풍성한 팁 생성기 ---
def get_diverse_tips(fine, mode, zone, speed, limit):
    """
    금액을 기반으로 취미/생활 물가를 동적으로 계산하여 팩트 폭력을 생성합니다.
    """
    if fine == 0:
        return ["✅ 완벽한 드라이버입니다! 오늘 아낀 돈으로 여유롭게 따뜻한 차 한 잔을 즐기세요. ☕"]

    tips_pool = []

    # 1. 물리 법칙 기반의 차가운 팩트 체크 (속도 위반 시)
    if mode == "속도 위반" and limit > 0 and speed > limit:
        power_ratio = round((speed / limit) ** 2, 1)
        travel_per_sec = round(speed / 3.6, 1)
        tips_pool.extend([
            f"물리 법칙은 속도 위반을 봐주지 않습니다. 제동 거리와 충격 에너지는 속도의 제곱($v^2$)에 비례하므로, 규정 속도 대비 피해 규모가 무려 **{power_ratio}배** 폭증합니다.",
            f"시속 {speed}km 주행 시, 위험을 인지하고 브레이크로 발을 옮기는 1초의 찰나에 이미 **{travel_per_sec}미터**를 제어 불능 상태로 날아갑니다.",
            "아무리 뛰어난 최신 하체 세팅과 브레이크 시스템을 갖춘 차량도, 타이어의 물리적 접지 한계를 넘어선 과속 앞에서는 무용지물이 됩니다."
        ])
    else:
        tips_pool.append(f"현재 계신 {zone} 구역은 과태료와 벌점이 무겁게 가중 처벌되는 곳입니다. 보행자 예측 불가능성에 대비하는 유일한 무기는 서행뿐입니다.")

    # ---------------------------------------------------------
    # [동적 계산 엔진] 과태료(fine) 금액에 맞춰 횟수와 갯수를 계산합니다.
    # ---------------------------------------------------------
    
    # 2. 레트로 카세트 플레이어 (Sony, Aiwa, Panasonic, Sanyo)
    if fine >= 1200000:
        tips_pool.append("이 엄청난 과태료면 80~90년대 전성기를 누렸던 SONY나 AIWA의 완벽하게 작동하는 S급 레트로 명기(약 120만 원 상당)를 소장할 수 있습니다.")
    else:
        broken_count = fine // 30000
        if broken_count > 0:
            tips_pool.append(f"이 돈이면 수리나 부품 추출용으로 쓰이는 고장 난 일본제(SONY, AIWA, Panasonic, Sanyo) 레트로 워크맨을 무려 **{broken_count}대**나 중고 장터에서 싹쓸이할 수 있습니다.")

    # 3. 자동차 금융 (할부/렌트) 및 유지비
    tips_pool.extend([
        f"요즘 유행하는 신차 장기 렌트나 할부를 이용 중이시라면, 이 과태료({fine:,}원)는 한 달 치 할부 이자나 렌트료의 상당 부분을 허공에 날린 셈입니다.",
        "폭스바겐 골프 GTI, 푸조 208, 마쓰다 MX-5(미아타), 토요타 GR86 같은 경쾌하고 매력적인 유럽/일본제 펀카(Fun Car)의 고급 합성유를 교환하고도 남을 유지비가 사라졌습니다."
    ])

    # 4. 스포츠 (테니스, 골프)
    tennis_hours = fine // 20000  # 코트 대여료 평균 2만원 가정
    screen_golf = fine // 25000   # 스크린 골프 평균 2.5만원 가정
    
    if fine >= 200000:
        tips_pool.append("이 금액이면 비싼 주말 야외 실외 골프장(필드)의 1인 그린피를 내고 탁 트인 자연에서 라운딩을 즐길 수 있습니다.")
    else:
        if screen_golf > 0:
            tips_pool.append(f"이 돈이면 쾌적한 실내 스크린 골프장을 **{screen_golf}번**이나 예약해서 지인들과 게임을 즐길 수 있습니다.")
        if tennis_hours > 0:
            tips_pool.append(f"공공/사설 테니스 코트를 예약해 약 **{tennis_hours}시간** 동안 파트너와 땀 흘리며 랠리를 즐길 수 있는 소중한 코트 대여료입니다.")

    # 5. 레이싱 게임, 심레이싱(Sim-Racing), F1
    f1_tv_months = fine // 15000 # F1 TV 한 달 구독료 대략 산정
    if fine >= 150000:
        tips_pool.append("이 과태료면 로지텍이나 파나텍 같은 심레이싱(Sim Racing) 입문용 스티어링 휠 할부금을 갚거나, 최고급 레이싱 페달을 업그레이드할 수 있습니다.")
    if f1_tv_months > 0:
        tips_pool.append(f"이 돈이면 F1 TV Pro를 **{f1_tv_months}개월** 동안 구독하며 주말마다 편안하게 방구석에서 퀄리파잉과 본선 레이스를 즐길 수 있습니다.")
    tips_pool.append("최신 F1 공식 게임 타이틀이나 그란 투리스모를 구입하고도 치킨을 시켜 먹을 수 있는 돈이 길바닥에 뿌려졌습니다.")

    # 카테고리가 너무 많아지면 화면이 꽉 차므로, 리스트 섞은 뒤 무작위로 2개만 추출해서 보여줍니다.
    random.shuffle(tips_pool)
    return tips_pool[:2]

# 1 Supabase에서 실데이터 가져오기
@st.cache_data(ttl=60)
def fetch_real_data():
    try:
        # 1. 금고(Secrets)에서 열쇠 꺼내기 시도
        if "url" not in st.secrets or "key" not in st.secrets:
            # 현재 금고에 뭐가 들어있는지 키값만 확인 (보안상 값은 출력 안 함)
            existing_keys = list(st.secrets.to_dict().keys())
            st.error(f"🚨 [Secret Error] 금고에 URL이나 KEY가 없습니다.")
            st.info(f"현재 인식된 키 목록: {existing_keys}")
            return pd.DataFrame()

        url = st.secrets["url"]
        key = st.secrets["key"]

        # 2. Supabase 클라이언트 생성 시도
        supabase: Client = create_client(url, key)
        
        # 3. 데이터 호출 시도
        response = supabase.table("usage_logs").select("*").eq("app_name", "school_zone_fine_web").execute()
        return pd.DataFrame(response.data)

    except Exception as e:
        st.error(f"🚨 [Unknown Error] 예상치 못한 에러가 발생했습니다: {e}")
        return pd.DataFrame()

# --- [2] 대시보드 로직 (나중에 Supabase 데이터와 연결) ---
def render_dashboard(df):
    df = fetch_real_data()

    st.subheader("🌐 실시간 전국 교통 안전 트렌드")
    
    if not df.empty:
        st.write("📍 **현재 접속 및 조회 발생 지역**")

        # '레이어 컨트롤러' 고급 지도 호출
        render_advanced_map(df)

        # 1. 한국 중심 좌표로 지도 생성
        # tiles="OpenStreetMap"은 한국 지명을 한글로 아주 잘 보여줍니다.
        # m = folium.Map(location=[36.5, 127.5], zoom_start=7, tiles="OpenStreetMap")

        # 2. 데이터 포인트 찍기
        # for _, row in df.iterrows():
        #     # 영문 도시명을 한글로 변환 (아까 만든 딕셔너리 활용)
        #     city_map = {"Namyangju": "남양주", "Seoul": "서울", "Gyeonggi-do": "경기도"}
        #     city_ko = city_map.get(row['city'], row['city'])
            
        #     folium.CircleMarker(
        #         location=[row['lat'], row['lon']],
        #         radius=7,
        #         popup=f"{city_ko} 조회 발생",
        #         color="#FF4B4B",
        #         fill=True,
        #         fill_color="#FF4B4B",
        #         fill_opacity=0.7
        #     ).add_to(m)

        # # [추가할 부분] 점이 하나라도 있으면, 데이터들의 최소/최대 위경도를 계산해 화면을 맞춥니다.
        # if len(df) > 0:
        #     sw = [df['lat'].min(), df['lon'].min()]
        #     ne = [df['lat'].max(), df['lon'].max()]
        #     m.fit_bounds([sw, ne])

        # 3. 지도 출력
        # st_folium(m, height=500, use_container_width=True, returned_objects=[])

        st.divider()

        # 데이터 분석 (JSON 파싱)
        # details 컬럼의 JSON 데이터를 데이터프레임 컬럼으로 확장
        details_df = pd.json_normalize(df['details'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 인기 검색 구역 TOP 5")
            st.caption("※ Y축 눈금은 사람들이 해당 구역의 과태료를 조회해 본 '검색 횟수(건)'를 의미합니다.")
            if 'zone' in details_df.columns:
                zone_counts = details_df['zone'].value_counts().head(5)
                st.bar_chart(zone_counts)
            else:
                st.write("데이터 수집 중...")

        with col2:
            if 'fine' in details_df.columns:
                total_fine = details_df['fine'].sum()
                st.metric(label="총 방어 과태료 합계", value=f"{total_fine:,}원")
                st.caption("※ 시뮬레이션을 통해 인지한 잠재적 과태료 절감액입니다.")

def calculate_fine(zone_type, speed_diff, vehicle_type):
    # 기본 과태료 테이블 (승용차 기준)
    if "보호구역" in zone_type:
        # 보호구역은 일반 도로의 약 2배 가깝게 가중처벌됩니다.
        if speed_diff <= 20: return 70000
        elif speed_diff <= 40: return 100000
        elif speed_diff <= 60: return 130000
        else: return 160000 # 60km/h 초과 시
    else:
        # 일반도로 기준
        if speed_diff <= 20: return 40000
        elif speed_diff <= 40: return 70000
        elif speed_diff <= 60: return 100000
        else: return 130000

def calculate_penalty_points(zone_type, speed_diff):
    """
    위반 구역과 초과 속도(speed_diff)에 따른 현실적인 벌점 계산 로직
    """
    if speed_diff <= 0:
        return 0  # 속도 위반 아님

    if "보호구역" in zone_type:
        # 보호구역 (어린이/노인/장애인) 기준 엄격한 벌점 적용
        if speed_diff <= 20: 
            return 15
        elif speed_diff <= 40: 
            return 30
        elif speed_diff <= 60: 
            return 60   # 즉시 면허 정지 (40점 이상)
        else: 
            return 120  # 60km/h 초과 시 120일 면허 정지
    else:
        # 일반 도로 기준 벌점 적용
        if speed_diff <= 20: 
            return 0    # 20km/h 이하 초과는 보통 과태료만 부과 (벌점 없음)
        elif speed_diff <= 40: 
            return 15
        elif speed_diff <= 60: 
            return 30
        else: 
            return 60   # 즉시 면허 정지

# 캐시를 60초 유지하되, 아까 만든 '새로고침' 버튼으로 강제 초기화할 수 있습니다.
@st.cache_data(ttl=60)
def get_all_usage_data():
    """Supabase의 usage_logs 테이블에서 데이터를 가져와 데이터프레임으로 반환합니다."""
    try:
        # secrets.toml에 저장된 Supabase 인증 정보 사용
        url = st.secrets["url"]
        key = st.secrets["key"]
        supabase: Client = create_client(url, key)

        # usage_logs 테이블에서 school_zone_fine_web에서 발생한 데이터만 조회
        response = supabase.table("usage_logs").select("*").eq("app_name", "school_zone_fine_web").execute()
        
        # 가져온 데이터를 Pandas DataFrame으로 변환하여 반환
        if response.data:
            return pd.DataFrame(response.data)
        else:
            return pd.DataFrame() # 데이터가 아직 없으면 빈 껍데기 반환
            
    except Exception as e:
        # DB 연결 실패 등의 에러 발생 시 조용히 빈 데이터프레임 반환
        return pd.DataFrame()

def render_advanced_map(df):
    try:
        # 🎯 1. 1차 필터링: 대상 앱과 액션만 분리
        target_app = 'school_zone_fine_web'
        target_action = 'check_clicked'

        df_target = df[
            (df['app_name'] == target_app) & 
            (df['action'] == target_action)
        ].copy()

        if df_target.empty:
            st.info("📍 아직 과태료 조회를 실행한 사용자가 없습니다. 첫 번째 주인공이 되어보세요!")
            return

        # 🔍 2. 2차 필터링: 유효한 위치 데이터만 골라내기
        valid_condition = (
            df_target['lat'].notna() & 
            df_target['lon'].notna() & 
            (df_target['lat'] != 0) & 
            (df_target['lon'] != 0) &
            (df_target['lat'].astype(str) != "") &
            (df_target['lon'].astype(str) != "")
        )

        clean_df = df_target[valid_condition]
        total_count = len(df_target)
        missing_count = total_count - len(clean_df)

        # 📣 3. 위치 정보 누락 안내 문구
        if missing_count > 0:
            st.caption(f"👀 보안망(VPN) 접속 등으로 위치 파악이 어려운 {missing_count}건의 로그는 지도 표시에서 제외되었습니다.")

        if clean_df.empty:
            return

        # --- 🎛️ 4. UI 컨트롤 패널 ---
        style_options = {
            "기본 지도 (OpenStreetMap)": "open-street-map",
            "밝은 지도 (Carto Positron)": "carto-positron",
            "어두운 지도 (Carto Darkmatter)": "carto-darkmatter"
        }
        selected_style_name = st.selectbox("🗺️ 지도 스타일", list(style_options.keys()))
        selected_style = style_options[selected_style_name]

        # 📊 5. 데이터 집계: 툴팁 표시를 위해 도시별로 데이터를 묶습니다.
        # 툴팁에 예쁘게 출력되도록 컬럼 이름을 '조회건수'로 지정합니다.
        clean_df['city'] = clean_df['city'].fillna('알 수 없음').replace('', '알 수 없음')
        city_counts = clean_df.groupby(['city', 'lat', 'lon']).size().reset_index(name='조회건수')

        # 🎯 6. 🔥 히트맵 렌더링 (농도 기반 + 깔끔한 툴팁)
        fig = px.density_mapbox(
            city_counts, 
            lat='lat', 
            lon='lon', 
            z='조회건수', # 가중치를 '조회건수'로 주어 히트맵 농도 결정
            radius=35,
            center=dict(lat=36.5, lon=127.5), 
            zoom=6.5,
            mapbox_style=selected_style,
            height=700,
            color_continuous_scale="Reds",
            hover_name='city', # 툴팁 맨 위에 굵은 글씨로 도시 이름 표시
            hover_data={
                'lat': False,  # 👈 위도 숨김
                'lon': False,  # 👈 경도 숨김
                'city': False, # hover_name과 중복되므로 한 번만 나오게 숨김
                '조회건수': True # 우리가 보고 싶은 건수만 표시
            }
        )

        # 레이아웃 튜닝
        fig.update_layout(
            margin={"r":0, "t":0, "l":0, "b":0},
            showlegend=False, 
            dragmode="pan"
        )

        # 화면 출력
        st.plotly_chart(
            fig, 
            use_container_width=True, 
            config={
                'scrollZoom': True, 
                'displayModeBar': False,
                'locale': 'ko' 
            }
        )

    except Exception as e:
        st.error(f"대시보드 렌더링 중 오류가 발생했습니다: {e}")

# --- [3] 메인 UI ---
def main():
    # 1. 세션 상태 초기화 (main 함수 최상단)
    if "analysis_result" not in st.session_state:
        st.session_state["analysis_result"] = None
        
    st.set_page_config(page_title="교통 법규 종합 포털", page_icon="⚖️", layout="wide")
    
    # 트래커 실행 (앱 오픈 로그)
    # log_app_usage("school_zone_fine_web", "app_opened")
    # ✅ 최초 1회만 쌓임
    if "app_opened_logged" not in st.session_state:
        log_app_usage("school_zone_fine_web", "app_opened")
        st.session_state["app_opened_logged"] = True  # "이미 기록함" 도장 꽝!

    st.title("⚖️ 잡학다식 교통 법규 마스터")
    
    # 탭 구성
    main_tab, dash_tab = st.tabs(["🚀 과태료 시뮬레이터", "📊 데이터 대시보드"])

    with main_tab:
        # 좌우 비율을 1:1.2로 나누어 결과창을 조금 더 넓게 배치합니다.
        col_input, col_result = st.columns([1, 1.2])
        
        # ⬅️ 1. 상황 설정 (입력부)
        with col_input:
            st.header("⚙️ 상황 설정")
            v_type = st.selectbox("차종", ["승용차", "승합차"])
            z_type = st.selectbox("단속 구역", ["일반도로", "보호구역 (어린이/노인/장애인)", "고속도로"])
            v_mode = st.radio("위반 유형", ["속도 위반", "불법 주정차"])
            
            # 모든 입력값은 여기서 결정됩니다.
            if v_mode == "속도 위반":
                limit = st.selectbox("제한 속도 (km/h)", [30, 40, 50, 60, 70, 80, 90, 100, 110], index=0)
                speed = st.number_input("주행 속도 (km/h)", min_value=0, value=limit+20)
            else:
                p_type = st.radio("주차 위치", ["일반 구역", "소화전/소방시설"])

            # 버튼을 눌러야 결과가 계산되도록 설정
            calc_btn = st.button("🚨 내 지갑 운명 확인하기")

        # ➡️ 2. 분석 결과 (출력부)
        with col_result:
            st.header("📝 분석 결과")
            
            # ==========================================
            # 1. 데이터 계산 및 세션 저장 (버튼 클릭 시 발동)
            # ==========================================
            if calc_btn:
                # 초기화: 어떤 경로에서도 에러가 나지 않도록 기본값 설정
                fine = 0
                points = 0
                speed_diff = 0
                
                # [데이터 로깅]
                log_app_usage("school_zone_fine_web", "analysis_performed")

                # [과태료 계산 로직]
                if v_mode == "속도 위반":
                    speed_diff = speed - limit
                    if speed_diff > 0:
                        fine = calculate_fine(z_type, speed_diff, v_type)
                        points = calculate_penalty_points(z_type, speed_diff)
                        
                elif v_mode == "불법 주정차":
                    fine = 40000  # 설정하신 기본 과태료
                    # 주정차의 경우 speed_diff는 의미 없으므로 0 유지

                # [인사이트 팁 생성]
                tips = get_diverse_tips(
                    fine, v_mode, z_type, 
                    speed if v_mode == "속도 위반" else 0, 
                    limit if v_mode == "속도 위반" else 0
                )

                # 🎯 [핵심] 모든 결과를 세션 상태에 '박제'합니다.
                # 이렇게 저장해두면 화면이 새로고침되어도 결과가 사라지지 않습니다.
                st.session_state["analysis_result"] = {
                    "v_mode": v_mode,
                    "z_type": z_type,
                    "p_type": p_type if v_mode == "불법 주정차" else "",
                    "speed_diff": speed_diff,
                    "fine": fine,
                    "points": points,
                    "tips": tips
                }

                # [DB 로그 전송]
                log_app_usage(
                    "school_zone_fine_web", 
                    "check_clicked", 
                    details={
                        "v_mode": v_mode,
                        "fine": fine,
                        "zone": z_type,
                        "limit": limit if v_mode == "속도 위반" else 0,
                        "speed": speed if v_mode == "속도 위반" else 0,
                        "v_type": v_type
                    }
                )

            # ==========================================
            # 2. 화면 출력 로직 (버튼 바깥에 위치)
            # ==========================================
            # 세션에 저장된 결과가 있다면 무조건 화면에 그립니다.
            if "analysis_result" in st.session_state and st.session_state["analysis_result"]:
                res = st.session_state["analysis_result"]
                
                st.markdown("---")
                # st.subheader("📝 분석 결과")

                if res["v_mode"] == "속도 위반":
                    if res["speed_diff"] <= 0:
                        st.success("✅ 규정 속도를 준수하고 계십니다! 모범 운전자시네요.")
                    else:
                        st.error(f"### 예상 과태료: {res['fine']:,}원")
                        if res["points"] > 0:
                            st.warning(f"#### 부과 벌점: {res['points']}점")
                        if res["points"] >= 40:
                            st.error(f"⚠️ **면허 정지 위험:** 누적 벌점이 {res['points']}점으로 면허 정지 대상입니다.")
                            
                elif res["v_mode"] == "불법 주정차":
                    st.warning(f"📍 {res['z_type']} 내 {res['p_type']} 불법 주정차 적발!")
                    st.error(f"### 예상 과태료: {res['fine']:,}원")

                # [잡학다식 인사이트 출력]
                st.markdown("---")
                st.subheader("💡 잡학다식 인사이트")
                for tip in res["tips"]:
                    st.write(f"• {tip}")

            else:
                # 아직 버튼을 누르기 전일 때만 안내 문구를 띄웁니다.
                st.info("왼쪽에서 상황을 설정한 후 '🚨 내 지갑 운명 확인하기' 버튼을 눌러주세요.")

    with dash_tab:
        # 대시보드 탭에 처음 들어왔을 때만 기록
        if "dash_tab_logged" not in st.session_state:
            log_app_usage("school_zone_fine_web", "dashboardTab_opened")
            st.session_state["dash_tab_logged"] = True
            
        # 1. 강력한 새로고침 버튼 (데이터 강제 동기화)
        col_sync, _ = st.columns([1, 4])
        with col_sync:
            if st.button("🔄 실시간 데이터 동기화"):
                st.cache_data.clear() # 스트림릿의 기억을 강제로 지웁니다.
                st.rerun()            # 화면을 즉시 새로고침합니다.

        # 2. 실제 Supabase 데이터 가져오기 (샘플 데이터 삭제!)
        try:
            # 대표님이 기존에 만들어두신 실제 DB 호출 함수명으로 변경해 주세요.
            # 예: df = load_data_from_supabase() 또는 df = get_usage_logs()
            df = get_all_usage_data() 
            
            if not df.empty:
                render_dashboard(df)
            else:
                st.info("수집된 데이터가 아직 없습니다. 시뮬레이터를 먼저 실행해 주세요.")
        except Exception as e:
            st.error(f"데이터베이스 연결 오류: {e}")

if __name__ == "__main__":
    main()