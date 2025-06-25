import streamlit as st
import requests
from datetime import datetime, timedelta

# ✅ Tumhari valid API key
API_KEY = "AIzaSyCOQc0TZ5nrpCET2hkX3IOvCJqOJDiLB7k"

# YouTube API URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

st.title("📈 YouTube Viral Topic Finder (Health 40+)")

# User input
days = st.number_input("Search videos from last __ days:", 1, 30, 7)
custom_keyword = st.text_input("Or enter your own keyword (optional):")

# Default keywords
keywords = [
    "Healthy Aging", "Longevity Tips", "Wellness Over 40", "Biohacking", "Healthy Lifestyle",
    "Natural Health", "Age Gracefully", "Over 50 Health", "Mind Body Health", "Energy After 40",
    "Brain Health", "Memory Boost", "Sleep Hacks", "Better Sleep After 40", "Stress Relief Tips",
    "Joint Health", "Fit Over 50", "Weight Loss Over 40", "Anti Inflammatory Diet",
    "Intermittent Fasting Over 40", "Hormone Balance After 40", "Menopause Health Tips",
    "Walking Benefits After 50", "Supplements for Seniors", "Anti-Aging Nutrition",
    "Heart Health Over 40", "Bone Strength After 50", "Mobility Exercises for Seniors"
]

# Use custom keyword if entered
if custom_keyword:
    keywords = [custom_keyword]

if st.button("Fetch Videos"):
    try:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        for keyword in keywords:
            st.write(f"🔍 Searching: **{keyword}**")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "publishedAfter": start_date,
                "maxResults": 5,
                "order": "date",
                "key": API_KEY,
            }

            search_response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            search_data = search_response.json()

            # 🔴 Check for quota or invalid key errors
            if "error" in search_data:
                st.error(f"❌ API Error: {search_data['error']['message']}")
                break

            if "items" not in search_data or not search_data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = search_data["items"]
            video_ids = [v["id"]["videoId"] for v in videos]
            channel_ids = [v["snippet"]["channelId"] for v in videos]

            # Get video stats
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_data = requests.get(YOUTUBE_VIDEO_URL, params=stats_params).json()

            # Get channel stats
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_data = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params).json()

            if "items" not in stats_data or "items" not in channel_data:
                st.warning(f"Stats not found for: {keyword}")
                continue

            # Combine & show results
            for i in range(len(videos)):
                try:
                    video = videos[i]
                    stat = stats_data["items"][i]
                    channel = channel_data["items"][i]

                    title = video["snippet"].get("title", "N/A")
                    description = video["snippet"].get("description", "")[:200]
                    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                    views = int(stat["statistics"].get("viewCount", 0))
                    subs = int(channel["statistics"].get("subscriberCount", 0))

                    if subs < 100000:
                        all_results.append({
                            "Title": title,
                            "Description": description,
                            "URL": video_url,
                            "Views": views,
                            "Subscribers": subs
                        })
                except:
                    continue

        # Display final result
        if all_results:
            st.success(f"🎯 Found {len(all_results)} videos:")
            for result in all_results:
                st.markdown(f"""
                **Title:** {result['Title']}  
                **Description:** {result['Description']}  
                **URL:** [Watch here]({result['URL']})  
                **Views:** {result['Views']}  
                **Subscribers:** {result['Subscribers']}
                """)
                st.write("---")
        else:
            st.warning("No videos found matching the criteria.")

    except Exception as e:
        st.error(f"💥 Error: {e}")
