import streamlit as st
import matplotlib.pyplot as plt
from app.kafka import video_comments, kafka_produce
from textblob import TextBlob

# Function to analyze sentiments
def analyze_sentiments(comments):
    sentiments = [TextBlob(comment['comment']).sentiment.polarity for comment in comments]
    return {
        'positive': sum(s > 0 for s in sentiments),
        'negative': sum(s < 0 for s in sentiments),
        'neutral': len(sentiments) - sum(s > 0 or s < 0 for s in sentiments),
    }

# Streamlit app title
st.title("Sentiment Analysis of YouTube Comments")


# Create a sidebar for configuration
st.sidebar.header("Configuration")

# Default API Key
default_api_key = ""  # Replace with your key, be cautious!

# Check if API key is already stored in session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = default_api_key  # Set default key

# Input for YouTube API Key in the sidebar
api_key = st.sidebar.text_input("YouTube API Key", type="password", value=st.session_state.api_key)

# Update session state if the user enters a new API key
if api_key != st.session_state.api_key:
    st.session_state.api_key = api_key

# Documentation link for obtaining the API key
st.sidebar.markdown(
    "[Get a YouTube API key](https://developers.google.com/youtube/registering_an_application)"
)

# Input for YouTube video ID in the main area
video_id = st.text_input("Enter YouTube Video ID (e.g., cc6Y4LbmiLU):")

# Button to fetch comments and send to Kafka
if st.button("Fetch Comments and Send to Kafka"):

    if video_id and st.session_state.api_key:
        try:
            comments = video_comments(video_id, st.session_state.api_key)  # Fetch comments using the API key
            if comments:
                total_comments = len(comments)  # Count total comments
                kafka_produce(comments)  # Produce comments to Kafka

                # Display the total number of comments
                st.write(f"Total Comments: {total_comments}")

                # Analyze sentiments
                sentiment_counts = analyze_sentiments(comments)

                # Visualize the YouTube video
                st.video(f"https://www.youtube.com/watch?v={video_id}")

                # Show bar chart for sentiment analysis
                labels = list(sentiment_counts.keys())
                counts = list(sentiment_counts.values())

                if any(count > 0 for count in counts):  # Check if any counts are greater than 0
                    fig, ax = plt.subplots()
                    ax.bar(labels, counts, color=['green', 'red', 'grey'])
                    ax.set_ylabel('Number of Comments')
                    ax.set_title('Sentiment Analysis of Comments')
                    ax.set_ylim(0, max(counts) + 1)  # Set y-axis limit for better visualization
                    st.pyplot(fig)
                else:
                    st.warning("No sentiment analysis available (all sentiments are zero).")

            else:
                st.warning("No comments found for this video.")
        except Exception as e:
            st.error(f"Error occurred: {e}")
    else:
        if not st.session_state.api_key:
            st.error("Please enter a valid YouTube API Key.")
        if not video_id:
            st.error("Please enter a valid YouTube video ID.")
