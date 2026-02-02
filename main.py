import streamlit as st
import threading
import os
from graph import app

# --------------------------------------------------
# Streamlit Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Video Repurposer",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "processing" not in st.session_state:
    st.session_state.processing = False

if "error" not in st.session_state:
    st.session_state.error = None

# --------------------------------------------------
# Background Worker Function
# --------------------------------------------------
def run_agents(youtube_url: str):
    try:
        initial_state = {"video_url": youtube_url}

        # Run your LangGraph / agents pipeline
        result = app.invoke(initial_state)

        # Save results for UI rendering
        st.session_state.results = result
        st.session_state.error = None

    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.results = None

    finally:
        # Always reset processing flag
        st.session_state.processing = False


# --------------------------------------------------
# UI: Title
# --------------------------------------------------
st.title("🎬 AI Video Repurposer")

# --------------------------------------------------
# UI: Sidebar Controls
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
# Start Processing (NON-BLOCKING)
# --------------------------------------------------
if start_clicked and youtube_url and not st.session_state.processing:
    st.session_state.processing = True
    st.session_state.results = None
    st.session_state.error = None

    threading.Thread(
        target=run_agents,
        args=(youtube_url,),
        daemon=True
    ).start()

# --------------------------------------------------
# Processing Status
# --------------------------------------------------
if st.session_state.processing:
    st.info("🤖 AI Agents are working… this may take a few minutes. Please wait.")

# --------------------------------------------------
# Error Display
# --------------------------------------------------
if st.session_state.error:
    st.error(f"❌ Error: {st.session_state.error}")

# --------------------------------------------------
# Results Display
# --------------------------------------------------
if st.session_state.results:
    results = st.session_state.results

    col1, col2 = st.columns([1, 1])

    # -----------------------------
    # LinkedIn Post
    # -----------------------------
    with col1:
        st.subheader("📱 LinkedIn Post")

        st.text_area(
            "Copy your post:",
            value=results.get("linkedin_post", ""),
            height=400
        )

    # -----------------------------
    # Video Output
    # -----------------------------
    with col2:
        st.subheader("🎥 Vertical Short")

        video_path = results.get("shorts_video_path")

        if video_path:
            st.caption(f"📁 Video path: {video_path}")

        if video_path and os.path.exists(video_path):
            st.video(video_path)

            with open(video_path, "rb") as f:
                st.download_button(
                    label="📥 Download Short",
                    data=f,
                    file_name="ai_short.mp4",
                    mime="video/mp4"
                )
        else:
            st.warning("⚠️ Video file not found. Processing may still be running.")
