from langchain_google_genai import ChatGoogleGenerativeAI
import os

def analyst_node(state):
    transcript = state.get("transcript")
    
    # We use Gemini 3 for its reasoning capabilities
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    prompt = f"""
    Analyze the following video transcript. Your goal is to find a viral-worthy 30-second clip.
    The clip should start with a strong hook and end on a high note.
    
    Return ONLY the start and end time in total seconds, separated by a comma.
    Example: 60,90
    
    TRANSCRIPT:
    {transcript}
    """

    try:
        response = llm.invoke(prompt)
        # Use regex or a smarter split to find numbers in case Gemini talks too much
        import re
        numbers = re.findall(r'\d+', response.text)
        if len(numbers) >= 2:
            start = int(numbers[0])
            end = int(numbers[1])
            # Ensure the clip isn't too long for a Short (max 60s)
            if end - start > 60:
                end = start + 59
            return {"start_time": start, "end_time": end}
        raise ValueError("Could not find timestamps")
    except Exception as e:
        # If Gemini gives weird text, we fallback to a safe default
        print(f"Analyst failed, using default: {e}")
        return {"start_time": 10, "end_time": 40}