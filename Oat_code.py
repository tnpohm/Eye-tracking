import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import zipfile
import os
os.system("pip install plotly pandas numpy requests streamlit")
import plotly.express as px
# -------------------------------
# 📥 โหลดข้อมูลจาก .txt
@st.cache_data
def load_data():
    zip_path = r"C:\Users\Ohm\OneDrive\เดสก์ท็อป\Python_for_INFOVISUAL\combined_with_movie_ids.zip"  # 👉 ใส่ path ที่แท้จริงของไฟล์ zip บนเครื่องคุณ

    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_filename = z.namelist()[0]  # 👉 หรือใส่ชื่อไฟล์ใน zip ตรง ๆ ถ้ารู้ เช่น "data.csv"
        df = pd.read_csv(z.open(csv_filename))

    df = df[df['missing_data'] == 0]
    return df

df = load_data()

# -------------------------------
# 🎯 Sidebar filters
st.sidebar.title("👁️ Eye Tracking Filter")
persons = df['person_id'].unique()
selected_person = st.sidebar.selectbox("เลือกผู้เข้าร่วม:", persons)

filtered_df = df[df['person_id'] == selected_person]

# -------------------------------
# 🎯 Section: Header
st.title("🚀 Eye Tracking Interactive Dashboard")
st.markdown("**ข้อมูลพฤติกรรมสายตาแบบ Interactive เพื่อให้เห็นรูปแบบและความน่าสนใจของการมอง**")

# -------------------------------
# 📈 1. กราฟ Pupil Area ตามเวลา (มี checkbox ควบคุม)
show_pupil_chart = st.sidebar.checkbox("แสดงกราฟ Pupil Area", value=True)

if show_pupil_chart:
    st.subheader("🔬 ขนาดรูม่านตาตามเวลา (Pupil Area)")
    fig_pupil = px.line(
        filtered_df,
        x="time_ms",
        y="pupil_area",
        title="Pupil Area Over Time",
        markers=True
    )
    st.plotly_chart(fig_pupil, use_container_width=True)

# -------------------------------
# 📌 2. Eye Movement Gaze Path
st.subheader("👁️ เส้นทางการเคลื่อนที่ของสายตา")
fig_gaze = px.line(
    filtered_df,
    x="x",
    y="y",
    title="Gaze Path",
    markers=True
)
fig_gaze.update_layout(yaxis=dict(autorange='reversed'))  # เพราะหน้าจอ 0,0 อยู่มุมซ้ายบน
st.plotly_chart(fig_gaze, use_container_width=True)

# -------------------------------
# 🌡️ 3. Heatmap ของตำแหน่งการมอง
st.subheader("🔥 Heatmap ของตำแหน่งการจ้องมอง")
heatmap_fig = px.density_heatmap(
    filtered_df,
    x="x",
    y="y",
    nbinsx=30,
    nbinsy=30,
    color_continuous_scale="Turbo"
)
heatmap_fig.update_layout(yaxis=dict(autorange='reversed'))
st.plotly_chart(heatmap_fig, use_container_width=True)

# -------------------------------
# 💡 4. Eye Scan Animation (simple)
st.subheader("🎥 การจำลองการเคลื่อนที่ของสายตา")
step = st.slider("เลื่อนเพื่อดูทีละจุด:", 0, len(filtered_df) - 1, 1)
single_point = filtered_df.iloc[:step + 1]

fig_anim = px.scatter(
    single_point,
    x="x",
    y="y",
    animation_frame=single_point.index.astype(str),
    size="pupil_area",
    color="time_ms"
)
fig_anim.update_layout(yaxis=dict(autorange='reversed'))
st.plotly_chart(fig_anim, use_container_width=True)