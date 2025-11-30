import streamlit as st
import pandas as pd
import requests
import pickle

# Streamlit Page Config

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Load processed movie data

@st.cache_data(show_spinner=False)
def load_data():
    with open('movie_data.pkl', 'rb') as file:
        movies, cosine_sim = pickle.load(file)
    return movies, cosine_sim

movies, cosine_sim = load_data()

# Recommendation Logic

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = movies[movies['title'] == title].index[0]
    except IndexError:
        return pd.DataFrame(columns=['title', 'movie_id'])

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # top 10 similar
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]


# TMDB Helper (light + cached)

TMDB_API_KEY = "7b995d3c6fd91a2284b4ad8cb390c7b8"

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id: int):
    """
    Fetch only what we need: poster, title, overview, rating, year.
    Cached so same movie_id is never re-fetched again.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        poster_path = data.get("poster_path")
        poster_url = (
            f"https://image.tmdb.org/t/p/w500{poster_path}"
            if poster_path
            else "https://via.placeholder.com/500x750?text=No+Image"
        )

        title = data.get("title") or "Unknown Title"
        overview = data.get("overview") or "No overview available."
        vote_average = data.get("vote_average") or 0
        release_date = data.get("release_date") or ""
        year = release_date.split("-")[0] if release_date else "N/A"

        if len(overview) > 190:
            overview = overview[:187] + "..."

        return {
            "poster_url": poster_url,
            "title": title,
            "overview": overview,
            "rating": round(vote_average, 1) if isinstance(vote_average, (int, float)) else vote_average,
            "year": year,
        }

    except Exception as e:
        print("TMDB fetch error:", e)
        return {
            "poster_url": "https://via.placeholder.com/500x750?text=Error",
            "title": "Unknown Title",
            "overview": "Could not fetch details.",
            "rating": "N/A",
            "year": "N/A",
        }



# Global Styling 

st.markdown("""
    <style>
        /* Uniform neon night background */
        html, body, .stApp, [class*="stApp"], .block-container {
            background: radial-gradient(circle at top, #020617 0, #020617 40%, #020617 100%) !important;
            color: #e5f2ff;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
            max-width: 1200px;
        }

        /* Subtle grid / scanline vibe (overlay) */
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(rgba(15,23,42,0.5) 1px, transparent 1px),
                linear-gradient(90deg, rgba(15,23,42,0.6) 1px, transparent 1px);
            background-size: 0.5px 12px, 12px 0.5px;
            opacity: 0.18;
            z-index: -1;
        }

        /* Title + Subtitle */
        .app-title {
            text-align: center;
            font-size: 40px;
            font-weight: 800;
            color: #38bdf8;
            margin-top: 5px;
            letter-spacing: 1.6px;
            text-shadow: 0 0 16px rgba(56,189,248,0.8);
        }
        .app-subtitle {
            text-align: center;
            font-size: 16px;
            color: #a5b4fc;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        /* Movie cards – glassy neon */
        .movie-card {
            background: radial-gradient(circle at top left, rgba(56,189,248,0.16), rgba(15,23,42,0.96));
            border-radius: 18px;
            padding: 12px;
            margin-bottom: 18px;
            box-shadow: 0 12px 30px rgba(15,23,42,0.9);
            border: 1px solid rgba(56,189,248,0.35);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            backdrop-filter: blur(8px);
            transition: all 0.16s ease-in-out;
        }
        .movie-card:hover {
            transform: translateY(-5px) scale(1.015);
            box-shadow: 0 18px 40px rgba(15,23,42,1);
            border-color: rgba(125,211,252,0.85);
        }

        .poster-img {
            width: 100%;
            border-radius: 14px;
            margin-bottom: 10px;
            box-shadow: 0 10px 20px rgba(15,23,42,1);
            transition: transform 0.16s ease-in-out, box-shadow 0.16s ease-in-out;
        }
        .movie-card:hover .poster-img {
            transform: scale(1.03);
            box-shadow: 0 14px 30px rgba(15,23,42,1);
        }

        .movie-title {
            font-size: 15px;
            font-weight: 700;
            color: #e5f2ff;
            margin-bottom: 4px;
        }

        .movie-meta {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            margin-bottom: 6px;
            color: #bae6fd;
        }

        .movie-year {
            opacity: 0.85;
        }

        .movie-rating {
            background: radial-gradient(circle, #22d3ee 0%, #0ea5e9 60%, #0369a1 100%);
            padding: 2px 9px;
            border-radius: 999px;
            font-size: 11px;
            border: 1px solid #7dd3fc;
            color: #0b1120;
        }

        .movie-overview {
            font-size: 12px;
            color: #e0f2fe;
            opacity: 0.94;
            line-height: 1.35;
        }

        /* Main button */
        .stButton>button {
            border-radius: 999px;
            background: linear-gradient(90deg, #0ea5e9, #22d3ee);
            color: #020617;
            font-weight: 700;
            border: none;
            padding: 0.6rem 1.9rem;
            cursor: pointer;
            box-shadow: 0 10px 24px rgba(15,23,42,1);
        }
        .stButton>button:hover {
            filter: brightness(1.06);
            box-shadow: 0 14px 30px rgba(15,23,42,1);
        }

        /* Selectbox label */
        label[data-baseweb="typography"] {
            font-weight: 600;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# Main UI

st.markdown('<div class="app-title">Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Futuristic ML-powered movie recommendations with TMDB data</div>', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "Choose a movie to get similar recommendations",
    sorted(movies['title'].values)
)

if st.button("⚡ Get Recommendations"):
    with st.spinner("Scanning the grid for similar vibes..."):
        rec_df = get_recommendations(selected_movie)

        if rec_df.empty:
            st.error("No recommendations found for this movie.")
        else:
            st.markdown("### 🔷 Top 10 Recommendations")
            st.write("")

            # Show in rows of 5 (2 rows)
            for start in range(0, len(rec_df), 5):
                cols = st.columns(5)
                for col, (_, row) in zip(cols, rec_df.iloc[start:start+5].iterrows()):
                    movie_id = int(row["movie_id"])
                    details = fetch_movie_details(movie_id)

                    with col:
                        card_html = f"""
                            <div class="movie-card">
                                <img src="{details['poster_url']}" class="poster-img" />
                                <div class="movie-title">{details['title']}</div>
                                <div class="movie-meta">
                                    <span class="movie-year">{details['year']}</span>
                                    <span class="movie-rating">⭐ {details['rating']}</span>
                                </div>
                                <div class="movie-overview">{details['overview']}</div>
                            </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)