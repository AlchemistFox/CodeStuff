import streamlit as st
from sheets_service import read_all_records
import sessions

st.set_page_config(page_title="Group Results", layout="centered")

st.title("🍿 Group Results")

# Check login/session
if "user" not in st.session_state or "session_code" not in st.session_state:
    st.warning("You must be logged in and in a session to view results.")
    st.stop()

user = st.session_state["user"]
session_code = st.session_state["session_code"]
users = sessions.get_users_in_session(session_code)

# Fetch all response rows
data = read_all_records()

# Sanity check headers
required_keys = {"user_id", "movie_id", "movie_title", "response", "session_code"}
valid_data = [
    row for row in data
    if required_keys.issubset(row.keys())
]

# Filter by session and response
filtered = [
    row for row in valid_data
    if row["session_code"] == session_code and row["user_id"] in users and row["response"] == "Yes"
]

# Aggregate results
from collections import defaultdict
vote_counts = defaultdict(int)
movie_titles = {}

for row in filtered:
    mid = row["movie_id"]
    vote_counts[mid] += 1
    movie_titles[mid] = row["movie_title"]

# Sort by most likes
sorted_movies = sorted(vote_counts.items(), key=lambda x: x[1], reverse=True)

if not sorted_movies:
    st.info("No movies have been liked yet in this session.")
else:
    st.subheader("🎬 Most Liked Movies in This Session")
    for movie_id, count in sorted_movies:
        title = movie_titles[movie_id]
        st.markdown(f"**{title}** – 👍 {count} votes")
