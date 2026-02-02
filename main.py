import streamlit as st
import threading
import os
import json
from graph import app

RESULT_FILE = "job_result.json"

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Video Repurposer",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "processing" not in st.session_state:
    st.session_state.processing = False

if "results" not in st.session_state:
    st.session_state.results = None

if "error" not in st.session_state:
    st.session_state.error = None


# --------------------------------------------------
# Background Worker (PURE PYTHON ONLY)
# --------------------------------------------------
def run_agents_worker(youtube_url: str):
    try:
        result = app.invoke({"video_url": youtube_url})

        with open(RESULT_FILE, "w") as f:
            json.dump(result, f)

    except Exception as e:
        with open(RESULT_FILE, "w") as f:
            json.dump({"error": str(e)}, f)


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
# Start Processing
# --------------------------------------------------
if start_clicked and youtube_url and not st.session_state.processing:
    st.session_state.processing = True
    st.session_state.results = None
    st.session_state.error = None

    # Remove old result file if exists
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)

    threading.Thread(
        target=run_agents_worker,
        args=(youtube_url,),
        daemon=True
    ).start()


# --------------------------------------------------
# Poll for Result File
# --------------------------------------------------
if st.session_state.processing:
    st.info("🤖 AI Agents are working… this may take a few minutes.")

    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE) as f:
            data = json.load(f)

        st.session_state.processing = False

        if "error" in data:
            st.session_state.error = data["error"]
        else:
            st.session_state.results = data

        st.experimental_rerun()


# --------------------------------------------------
# Error
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
