from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    """Extracts the 11-character ID from a YouTube URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def transcription_node(state):
    """
    Modern 2026 Worker Node: Accesses data using .text instead of ['text'].
    """
    url = state.get("video_url")
    video_id = get_video_id(url)
    
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    try:
        # 1. Initialize API
        ytt_api = YouTubeTranscriptApi()
        
        # 2. Get the transcript object
        transcript_list = ytt_api.list(video_id)
        transcript = transcript_list.find_transcript(['en'])
        
        # 3. Fetch the snippets (the snippets are now objects, not dicts)
        transcript_data = transcript.fetch()
        
        # 4. Loop through snippets using .text (this is the fix!)
        # Before we did: item['text'] 
        # Now we do: item.text
        full_transcript = " ".join([item.text for item in transcript_data])
        
        return {"transcript": full_transcript}
        
    except Exception as e:
        return {"error": f"Transcription failed: {str(e)}"}