import streamlit as st
import pandas as pd
import os
import urllib.request
from datetime import datetime
import plotly.express as px

# 1. Функція скачування
def download_all_data(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    for i in range(1, 28):
        if not any(f.startswith(f"vhi_id_{i}_") for f in os.listdir(folder_path)):
            url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2024&type=Mean"
            filepath = os.path.join(folder_path, f"vhi_id_{i}_{datetime.now().strftime('%Y%m%d')}.csv")
            try:
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                st.error(f"Не вдалося завантажити ID {i}: {e}")

# 2. Функція обробки даних
@st.cache_data
def load_and_clean_data(folder_path):
    download_all_data(folder_path)
    all_data = []
    noaa_indices = {1:"Cherkasy", 2:"Chernihiv", 3:"Chernivtsi", 4:"Crimea", 5:"Dnipropetrovsk", 6:"Donetsk", 7:"Ivano-Frankivsk", 8:"Kharkiv", 9:"Kherson", 10:"Khmelnytskyy", 11:"Kyiv", 12:"Kyiv City", 13:"Kirovohrad", 14:"Luhansk", 15:"Lviv", 16:"Mykolayiv", 17:"Odessa", 18:"Poltava", 19:"Rivne", 20:"Sevastopol", 21:"Sumy", 22:"Ternopil", 23:"Transcarpathia", 24:"Vinnytsya", 25:"Volyn", 26:"Zaporizhzhya", 27:"Zhytomyr"}
    ua_map = {"Vinnytsya": "Вінницька", "Volyn": "Волинська", "Dnipropetrovsk": "Дніпропетровська", "Donetsk": "Донецька", "Zhytomyr": "Житомирська", "Transcarpathia": "Закарпатська", "Zaporizhzhya": "Запорізька", "Ivano-Frankivsk": "Івано-Франківська", "Kyiv City": "Київ", "Kyiv": "Київська", "Kirovohrad": "Кіровоградська", "Crimea": "Крим", "Luhansk": "Луганська", "Lviv": "Львівська", "Mykolayiv": "Миколаївська", "Odessa": "Одеська", "Poltava": "Полтавська", "Rivne": "Рівненська", "Sevastopol": "Севастополь", "Sumy": "Сумська", "Ternopil": "Тернопільська", "Kharkiv": "Харківська", "Kherson": "Херсонська", "Khmelnytskyy": "Хмельницька", "Cherkasy": "Черкаська", "Chernivtsi": "Чернівецька", "Chernihiv": "Чернігівська"}

    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    for file in files:
        old_id = int(file.split('_')[2])
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        df_temp = pd.read_csv(os.path.join(folder_path, file), skiprows=2, names=headers).drop(columns=['empty']).dropna()
        # Видаляємо значення -1
        df_temp = df_temp[(df_temp['VHI'] != -1) & (df_temp['VCI'] != -1) & (df_temp['TCI'] != -1)]
        df_temp['Year'] = pd.to_numeric(df_temp['Year'].astype(str).str.extract('(\d+)', expand=False)).astype(int)
        df_temp[['Week','VCI','TCI','VHI']] = df_temp[['Week','VCI','TCI','VHI']].apply(pd.to_numeric)
        df_temp['Province_Name'] = ua_map.get(noaa_indices.get(old_id))
        all_data.append(df_temp)
    return pd.concat(all_data, ignore_index=True)

# 3. Callback для скидання
def reset_filters():
    st.session_state.index_type = "VCI"
    st.session_state.area_select = "Вінницька"
    st.session_state.year_range = (1981, 2024)
    st.session_state.week_range = (1, 52)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

# 4. Інтерфейс
st.set_page_config(layout="wide")
st.title("Аналіз індексів VCI, TCI, VHI")
df = load_and_clean_data("vhi_data")

# Ініціалізація стану
if 'index_type' not in st.session_state: reset_filters()

col_controls, col_display = st.columns([1, 3])

with col_controls:
    st.selectbox("Оберіть індекс:", ["VCI", "TCI", "VHI"], key='index_type')
    st.selectbox("Оберіть область:", sorted(df['Province_Name'].unique()), key='area_select')
    st.slider("Інтервал років:", 1981, 2024, key='year_range')
    st.slider("Інтервал тижнів:", 1, 52, key='week_range')
    st.checkbox("Сортувати за зростанням", key='sort_asc')
    st.checkbox("Сортувати за спаданням", key='sort_desc')
    st.button("Скинути фільтри", on_click=reset_filters)

# Фільтрація
filtered_df = df[
    (df['Province_Name'] == st.session_state.area_select) &
    (df['Year'].between(*st.session_state.year_range)) &
    (df['Week'].between(*st.session_state.week_range))
]

if st.session_state.sort_asc: filtered_df = filtered_df.sort_values(by=st.session_state.index_type)
if st.session_state.sort_desc: filtered_df = filtered_df.sort_values(by=st.session_state.index_type, ascending=False)

with col_display:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік області", "Порівняння по областях"])
    with tab1: st.dataframe(filtered_df)
    with tab2: st.plotly_chart(px.line(filtered_df, x='Week', y=st.session_state.index_type, color='Year'), use_container_width=True)
    with tab3: st.plotly_chart(px.bar(df[df['Year'].between(*st.session_state.year_range)].groupby('Province_Name')[st.session_state.index_type].mean().reset_index(), x='Province_Name', y=st.session_state.index_type), use_container_width=True)