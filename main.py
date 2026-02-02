import streamlit as st
from graph import app
import os

st.set_page_config(page_title="AI Video Repurposer", page_icon="🎬", layout="wide")

# 1. Initialize Memory (Session State)
# We check if 'results' exists in memory; if not, we create it as None.
if "results" not in st.session_state:
    st.session_state.results = None

st.title("🎬 AI Video Repurposer")

with st.sidebar:
    st.header("Settings")
    youtube_url = st.text_input("Enter YouTube URL:")
    process_button = st.button("🚀 Start Repurposing", type="primary")

# 2. Logic to Run the Agents
if process_button and youtube_url:
    with st.status("🤖 AI Agents are working...", expanded=True) as status:
        initial_state = {"video_url": youtube_url}
        # Save the output into the persistent session_state memory
        st.session_state.results = app.invoke(initial_state)
        status.update(label="✅ Processing Complete!", state="complete", expanded=False)

# 3. Logic to Display the Results
# Instead of checking the 'process_button', we check our 'memory'
if st.session_state.results:
    results = st.session_state.results
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📱 LinkedIn Post")
        st.text_area("Copy your post:", value=results.get("linkedin_post", ""), height=400)

    with col2:
        st.subheader("🎥 Vertical Short")
        video_path = results.get("shorts_video_path")
        if video_path and os.path.exists(video_path):
            st.video(video_path)
            
            # Now when you click this, the results stay because they are in session_state!
            with open(video_path, "rb") as file:
                st.download_button(
                    label="📥 Download Short",
                    data=file,
                    file_name="ai_short.mp4",
                    mime="video/mp4"
                )