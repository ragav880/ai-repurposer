from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from agents.transcriber import transcription_node
from agents.writer import writer_node
from agents.video_engine import video_clipper_node
from agents.analyst import analyst_node # NEW IMPORT

# 1. State Definition
class AgentState(TypedDict):
    video_url: str
    transcript: Optional[str]
    start_time: Optional[int] # NEW
    end_time: Optional[int]   # NEW
    linkedin_post: Optional[str]
    shorts_video_path: Optional[str]
    error: Optional[str]

# 2. Build Graph
workflow = StateGraph(AgentState)

# 3. Add Nodes
workflow.add_node("extract_transcript", transcription_node)
workflow.add_node("analyze_video", analyst_node) # NEW NODE
workflow.add_node("write_linkedin", writer_node)
workflow.add_node("clip_video", video_clipper_node)

# 4. Define Edges (The Flow)
workflow.add_edge(START, "extract_transcript")

# From transcript, we go to Analyst AND Writer
workflow.add_edge("extract_transcript", "analyze_video")
workflow.add_edge("extract_transcript", "write_linkedin")

# IMPORTANT: Video Clipper MUST wait for the Analyst to finish!
workflow.add_edge("analyze_video", "clip_video")

# End the flow
workflow.add_edge("write_linkedin", END)
workflow.add_edge("clip_video", END)

app = workflow.compile()