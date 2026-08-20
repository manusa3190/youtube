import streamlit as st

from tools.download import download_mp3, download_mp4

OUTPUT_DIR = "downloads"

st.title("YouTube Video Downloader")


url = st.text_input("YouTube動画のURLを入力してください", key="url")

if url:
    st.video(url)
else:
    st.write("URLを入力してください")

col1, col2, col3 = st.columns(3)
with col1:
    st.text_input("開始時間", value="0:00", key="start_time")
with col2:
    st.text_input("終了時間", value="0:00", key="stop_time")
with col3:
    st.selectbox("出力形式", ["mp3", "mp4"], key="format")


if st.button("Download"):
    st.write(f"Downloading {st.session_state.url}")
    if st.session_state.format == "mp3":
        output_path = download_mp3(
            st.session_state.url,
            st.session_state.start_time,
            st.session_state.stop_time,
        )
    else:
        output_path = download_mp4(
            st.session_state.url,
            st.session_state.start_time,
            st.session_state.stop_time,
        )
    st.write("Download complete")
    if st.session_state.format == "mp3":
        st.audio(output_path)
    else:
        st.video(output_path)
