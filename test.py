from graph import app

input_data = {"video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
print("🔄 AI is working... please wait (this takes a few seconds).")

result = app.invoke(input_data)

if result.get("error"):
    print(f"❌ Error: {result['error']}")
else:
    print("✅ Success! Here is your LinkedIn Post:\n")
    print("-" * 30)
    print(result.get("linkedin_post"))
    print("-" * 30)