import streamlit as st

# Fake sample data (simulating YouTube API response)
sample_results = [
    {
        "Title": "Healthy Aging Secrets After 40",
        "Description": "Learn natural ways to age gracefully. Tips on food, exercise and supplements.",
        "URL": "https://www.youtube.com/watch?v=abc123xyz",
        "Views": 14567,
        "Subscribers": 2300
    },
    {
        "Title": "Longevity Tips You Need to Know",
        "Description": "Want to live longer? Discover the best daily habits backed by science.",
        "URL": "https://www.youtube.com/watch?v=def456pqr",
        "Views": 32000,
        "Subscribers": 1500
    },
    {
        "Title": "Over 50 Health Checklist",
        "Description": "Stay active and healthy over 50 with these quick medical tips.",
        "URL": "https://www.youtube.com/watch?v=ghi789stu",
        "Views": 51000,
        "Subscribers": 850
    },
]

st.title("🧪 YouTube Viral Topic Tool (Demo Mode)")

st.markdown("🚫 This version does not use real API – only for testing UI and display layout.")

# Simulated input
days = st.slider("Enter Days to Simulate Search:", 1, 30, 7)
st.write(f"🔎 Simulating videos from the past {days} days...")

if st.button("Fetch Mock Data"):
    st.success(f"🎯 Found {len(sample_results)} sample videos!")
    for result in sample_results:
        st.markdown(f"""
        **Title:** {result['Title']}  
        **Description:** {result['Description']}  
        **URL:** [Watch here]({result['URL']})  
        **Views:** {result['Views']}  
        **Subscribers:** {result['Subscribers']}
        """)
        st.write("---")
