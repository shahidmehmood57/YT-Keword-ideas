import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyAcP7wYgr2MSySie2uOUHt887AI_kYXlZI"

# YouTube API URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool (40+ Health Audience)")

# Input Field
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of health-related keywords for 40+ audience
keywords = [
    "Healthy Aging", "Longevity Tips", "Wellness Over 40", "Biohacking", "Healthy Lifestyle",
    "Natural Health", "Age Gracefully", "Over 50 Health", "Mind Body Health", "Energy After 40",
    "Brain Health", "Memory Boost", "Sleep Hacks", "Better Sleep After 40", "Stress Relief Tips",
    "Joint Health", "Fit Over 50", "Weight Loss Over 40", "Anti Inflammatory Diet",
    "Intermittent Fasting Over 40", "Hormone Balance After 40", "Menopause Health Tips",
    "Walking Benefits After
