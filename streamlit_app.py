import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Define the prompt for the AI model
prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Function to extract transcript details from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('v=')[1].split('&')[0]  # Improved extraction
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Failed to fetch transcript: {e}")
        return None

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(api_key, transcript_text, prompt):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to convert video to blog post with structured sections
def convert_to_blog(api_key, transcript_text, prompt):
    # Generate the summary which will form the main content of the blog
    summary = generate_gemini_content(api_key, transcript_text, prompt)
    
    # Blog post structure
    blog_post = f"""
## Introduction
Start with an engaging introduction that hooks the reader, providing a brief overview of the video's topic and why it's worth reading about.

## Key Takeaways
- Highlight the most impactful points or insights from the video.
- Offer quick, bullet-point summaries for readers who want the essence of the video's content.

## Main Content
{summary}

## Conclusion
Wrap up the blog post by summarizing the key points discussed, reflecting on their importance, and possibly suggesting further reading or action based on the video's content.
    """
    return blog_post

# Streamlit UI setup
st.title("YouTube Blog Post Generator")

# Instructions for obtaining a Google API Key
st.markdown("""
### How to Obtain a Google API Key
1. Visit the [Google Cloud Console](https://makersuite.google.com/app/apikey/).
2. Create a new project or select an existing one.
3. Navigate to the "APIs & Services > Credentials" page.
4. Click on "Create Credentials" and select "API key".
5. Your new API key will be displayed; copy and use it here.
""")

# API Key Input
api_key = st.text_input("Enter your Google API Key:", type="password")

# YouTube Video Link Input
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    # Extract and display video thumbnail
    video_id = youtube_link.split('v=')[1].split('&')[0]
    thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)

    # Extract transcript for further processing
    transcript_text = extract_transcript_details(youtube_link) if youtube_link else ""

    # Layout for buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Get Summary"):
            if transcript_text:
                summary = generate_gemini_content(api_key, transcript_text, prompt)
                st.markdown("## Detailed Notes:")
                st.write(summary)

    with col2:
        if st.button("Convert to Blog"):
            if transcript_text:
                blog_post = convert_to_blog(api_key, transcript_text, prompt)
                st.markdown("## Blog Post:")
                st.markdown(blog_post)
