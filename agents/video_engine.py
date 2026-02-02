import os
from yt_dlp import YoutubeDL
from moviepy import VideoFileClip
from moviepy.video.fx import Crop

def video_clipper_node(state):
    url = state.get("video_url")
    
    # NEW: Get times from the Analyst (default to 10-40 if missing)
    start_time = state.get("start_time", 10)
    end_time = state.get("end_time", 40)
    
    output_raw = "raw_clip.mp4"
    output_final = "shorts_video.mp4"

    for f in [output_raw, output_final]:
        if os.path.exists(f): os.remove(f)

    try:
        # 1. Download segment
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'external_downloader': 'ffmpeg',
            'external_downloader_args': ['-ss', str(start_time), '-to', str(end_time)],
            'outtmpl': output_raw,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 2. MoviePy v2.x Logic
        clip = VideoFileClip(output_raw)
        w, h = clip.size
        target_width = int((h * 9 / 16) // 2) * 2 # Even number fix
        
        final_clip = clip.with_effects([
            Crop(width=target_width, height=h, x_center=w/2, y_center=h/2)
        ])
        
        # 3. Write file
        final_clip.write_videofile(
            output_final, 
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-pix_fmt", "yuv420p", "-profile:v", "high", "-level:v", "4.1"],
            temp_audiofile="temp-audio.m4a", 
            remove_temp=True
        )
        
        clip.close()
        if os.path.exists(output_raw): os.remove(output_raw)

        return {"shorts_video_path": output_final}

    except Exception as e:
        return {"error": f"Video Clipping failed: {str(e)}"}