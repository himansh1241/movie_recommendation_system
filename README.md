🎬 Movie Recommendation System

A simple and smart Content-Based Movie Recommendation System built using Python, scikit-learn, and Streamlit.
The system recommends similar movies based on metadata like genres, keywords, cast, and crew, using TF-IDF Vectorization and Cosine Similarity.

The web app is powered by Streamlit and fetches real movie posters using the TMDB API, making recommendations interactive and visually appealing.

⸻

🚀 Features
	•	🔍 Content-based recommendation (no user data required)
	•	🧠 TF-IDF vectorization on movie tags
	•	📐 Cosine Similarity for movie matching
	•	🧾 Displays top 10 similar movies
	•	🎭 Shows real movie posters using TMDB API
	•	💻 Simple and clean Streamlit interface
	•	🪶 Lightweight and beginner-friendly

⸻

🛠️ Tech Stack
	•	Python
	•	Pandas, NumPy
	•	scikit-learn
	•	Streamlit
	•	TMDB API

📁 Project Structure
├── Movie_Recommendation_System.ipynb    # Model building + Data processing
├── app.py                               # Streamlit web app
├── movie_data.pkl                       # Saved movie data + similarity matrix
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
└── README.md
  
