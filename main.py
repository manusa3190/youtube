import streamlit as st

from tools.download import download_mp3, download_mp4

st.title("YouTube Video Downloader")


url = st.text_input("YouTube動画のURLを入力してください", key="url")

if url:
    st.video(url)
else:
    st.write("URLを入力してください")

col1, col2, col3 = st.columns(3)
with col1:
    st.text_input("開始時間", value="", key="start_time", placeholder="例: 0:30")
with col2:
    st.text_input("終了時間", value="", key="stop_time", placeholder="例: 1:30")
with col3:
    st.selectbox("出力形式", ["mp3", "mp4"], key="format")


if st.button("ダウンロード"):
    st.write("Downloading...")
    if st.session_state.format == "mp3":
        data, file_name = download_mp3(
            st.session_state.url,
            st.session_state.start_time,
            st.session_state.stop_time,
        )
        mime = "audio/mpeg"
    else:
        data, file_name = download_mp4(
            st.session_state.url,
            st.session_state.start_time,
            st.session_state.stop_time,
        )
        mime = "video/mp4"

    st.session_state.download_data = data
    st.session_state.download_file_name = file_name
    st.session_state.download_mime = mime
    st.write("Download complete")

if "download_data" in st.session_state:
    st.download_button(
        label="保存",
        data=st.session_state.download_data,
        file_name=st.session_state.download_file_name,
        mime=st.session_state.download_mime,
        on_click="ignore",
    )
