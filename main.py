import streamlit as st
import threading
import os
from graph import app

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Video Repurposer",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# Session State Init
# --------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "processing" not in st.session_state:
    st.session_state.processing = False

if "job_done" not in st.session_state:
    st.session_state.job_done = False

if "error" not in st.session_state:
    st.session_state.error = None

if "worker_result" not in st.session_state:
    st.session_state.worker_result = None


# --------------------------------------------------
# Background Worker (NO Streamlit calls here!)
# --------------------------------------------------
def run_agents_worker(youtube_url: str):
    try:
        initial_state = {"video_url": youtube_url}
        result = app.invoke(initial_state)

        # Store result ONLY as plain data
        st.session_state.worker_result = result
        st.session_state.job_done = True

    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.job_done = True


# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🎬 AI Video Repurposer")


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    youtube_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    start_clicked = st.button(
        "🚀 Start Repurposing",
        type="primary",
        disabled=st.session_state.processing
    )


# --------------------------------------------------
# Start job (non-blocking)
# --------------------------------------------------
if start_clicked and youtube_url and not st.session_state.processing:
    st.session_state.processing = True
    st.session_state.job_done = False
    st.session_state.worker_result = None
    st.session_state.results = None
    st.session_state.error = None

    threading.Thread(
        target=run_agents_worker,
        args=(youtube_url,),
        daemon=True
    ).start()


# --------------------------------------------------
# While processing
# --------------------------------------------------
if st.session_state.processing and not st.session_state.job_done:
    st.info("🤖 AI Agents are working… this may take a few minutes.")


# --------------------------------------------------
# Job completed → move result into UI state
# --------------------------------------------------
if st.session_state.processing and st.session_state.job_done:
    st.session_state.processing = False
    st.session_state.results = st.session_state.worker_result
    st.experimental_rerun()   # 👈 CRITICAL


# --------------------------------------------------
# Error display
# --------------------------------------------------
if st.session_state.error:
    st.error(f"❌ Error: {st.session_state.error}")


# --------------------------------------------------
# Results UI
# --------------------------------------------------
if st.session_state.results:
    results = st.session_state.results

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📱 LinkedIn Post")
        st.text_area(
            "Copy your post:",
            value=results.get("linkedin_post", ""),
            height=400
        )

    with col2:
        st.subheader("🎥 Vertical Short")

        video_path = results.get("shorts_video_path")
        st.caption(f"📁 Video path: {video_path}")

        if video_path and os.path.exists(video_path):
            st.video(video_path)

            with open(video_path, "rb") as f:
                st.download_button(
                    "📥 Download Short",
                    f,
                    file_name="ai_short.mp4",
                    mime="video/mp4"
                )
        else:
            st.warning("⚠️ Video file not found.")
