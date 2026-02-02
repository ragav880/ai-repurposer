import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def writer_node(state):
    transcript = state.get("transcript")
    if not transcript:
        return {"error": "No transcript available."}

    # UPDATED MODEL NAME FOR 2026
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

    prompt = f"""
    You are a professional Content Creator. Rewrite this transcript into an engaging LinkedIn post.
    Use hooks, bullet points, and 3 hashtags.
    
    TRANSCRIPT:
    {transcript}
    """

    try:
        # 3. Ask Gemini to write the post
        response = llm.invoke(prompt)
        
        # 4. FIX: Extract the text content correctly
        # In the 2026 version of LangChain, .content is the standard.
        # If .content is a list (like in your terminal), we join it.
        if isinstance(response.content, list):
            # Find the text block and join them
            final_text = "".join([block['text'] for block in response.content if block['type'] == 'text'])
        else:
            final_text = response.content
            
        return {"linkedin_post": final_text}
    except Exception as e:
        return {"error": f"AI Writer failed: {str(e)}"}