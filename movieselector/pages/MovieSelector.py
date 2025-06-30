import streamlit as st
from tmdb_fetch import get_popular_movies
from responses import log_response

st.set_page_config(page_title="MovieSelector", layout="centered")

# Custom styling
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        div.stButton > button {
            width: 180px !important;
            height: 50px !important;
            font-size: 20px !important;
            cursor: pointer !important;
        }
    </style>
""", unsafe_allow_html=True)

# Check if user is logged in
if "user" not in st.session_state:
    st.warning("Please log in to continue.")
    st.stop()

# Load movies
movies = get_popular_movies()

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "yes_list" not in st.session_state:
    st.session_state.yes_list = []
if "no_list" not in st.session_state:
    st.session_state.no_list = []
if "confirm_exit" not in st.session_state:
    st.session_state.confirm_exit = False
if "choice_made" not in st.session_state:
    st.session_state.choice_made = False

def move_next(choice):
    # Prevent double-submit
    if st.session_state.choice_made:
        return

    st.session_state.choice_made = True
    movie = movies[st.session_state.index]
    user = st.session_state.get("user", "anonymous")

    log_response(user, movie["id"], movie["title"], "Yes" if choice == "yes" else "No")

    if choice == "yes":
        st.session_state.yes_list.append(movie)
    else:
        st.session_state.no_list.append(movie)

    st.session_state.index += 1

    # Reset choice_made after rerun
    st.rerun()

# Show current movie
if st.session_state.index < len(movies) and not st.session_state.confirm_exit:
    movie = movies[st.session_state.index]

    # Reset choice_made on new movie
    st.session_state.choice_made = False

    st.markdown(f'''
    <div style="text-align: center;">
        <img src="https://image.tmdb.org/t/p/w342{movie['poster_path']}" width="300" />
        <h3 style="margin-bottom: 0.5rem;">{movie["title"]}</h3>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Yes"):
            move_next("yes")
    with col2:
        if st.button("❌ No"):
            move_next("no")
    with col3:
        if st.button("🛑 End Early"):
            st.session_state.confirm_exit = True

    st.write("#### Synopsis")
    st.write(movie["overview"])

elif st.session_state.confirm_exit:
    st.warning("Are you sure you want to stop?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ No, continue"):
            st.session_state.confirm_exit = False
    with col2:
        if st.button("✅ Yes, stop"):
            st.session_state.index = len(movies)  # Mark as finished
            st.switch_page("pages/GroupResults.py")

else:
    st.success("You've gone through all the movies!")
    st.subheader("✅ Movies You Liked:")
    for m in st.session_state.yes_list:
        st.markdown(f"- **{m['title']}** ({m['release_date']})")
