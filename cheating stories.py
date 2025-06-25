import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyAcP7wYgr2MSySie2uOUHt887AI_kYXlZI"

# YouTube API URLs
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

st.title("YouTube Viral Topics Tool (40+ Health Audience)")

# Number of days input
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=10)

# Optional custom keyword input
custom_keyword = st.text_input("Or enter a custom keyword (optional):")

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

# Replace with custom keyword if provided
if custom_keyword:
    keywords = [custom_keyword]

# Fetch Data Button
if st.button("Fetch Data"):
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
                "maxResults": 10,
                "order": "date",
                "key": API_KEY,
            }

            search_response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            search_data = search_response.json()

            # Debug: Show raw response
            st.write("🔎 Raw API data:")
            st.json(search_data)

            if "items" not in search_data or not search_data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = search_data["items"]
            video_ids = [v["id"]["videoId"] for v in videos if "id" in v and "videoId" in v["id"]]
            channel_ids = [v["snippet"]["channelId"] for v in videos if "snippet" in v and "channelId" in v["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Missing video/channel IDs for: {keyword}")
                continue

            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in stats_data or "items" not in channel_data:
                st.warning(f"Stats not found for: {keyword}")
                continue

            for i in range(min(len(videos), len(stats_data["items"]), len(channel_data["items"]))):
                video = videos[i]
                stat = stats_data["items"][i]
                channel = channel_data["items"][i]

                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 100000:  # ✅ Updated from 3000 to 100k for more results
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # Show results
        if all_results:
            st.success(f"🎯 Found {len(all_results)} relevant videos!")
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
            st.warning("No relevant videos found for selected filters.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
