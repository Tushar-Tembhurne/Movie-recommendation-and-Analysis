import streamlit as st


# CLASSES -- Movie , Rating, Movie Analysis


class Movie:
    def __init__(self, movie_id, title, genre):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre

class Rating:
    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

class MovieAnalysis:
    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings

    def clean_data(self):
        """Remove ratings with missing/None values"""
        return [r for r in self.ratings if r.rating is not None]

    def compute_movie_stats(self, clean_ratings):
        """Calculate average rating and count for each movie with clean column names"""
        stats = {}
        for r in clean_ratings:
            if r.movie_id not in stats:
                stats[r.movie_id] = []
            stats[r.movie_id].append(r.rating)
            
        movie_lookup = {m.movie_id: m for m in self.movies}
        results = []
        
        for movie_id, rating_list in stats.items():
            if movie_id in movie_lookup:
                movie = movie_lookup[movie_id]
                avg_rating = sum(rating_list) / len(rating_list)
                results.append({
                    "Movie ID": movie_id,
                    "Title": movie.title,
                    "Genre": movie.genre,
                    "Average Rating": round(avg_rating, 2),
                    "Rating Count": len(rating_list)
                })
        return results

    def compute_genre_stats(self, movie_stats):
        """Calculate average rating per genre with professional column names"""
        genre_data = {}
        for item in movie_stats:
            genre = item['Genre']
            if genre not in genre_data:
                genre_data[genre] = []
            genre_data[genre].append(item['Average Rating'])
            
        genre_summary = []
        for genre, ratings in genre_data.items():
            avg = sum(ratings) / len(ratings)
            genre_summary.append({
                "Genre": genre,
                "Average Rating": round(avg, 2),
                "Total Movies": len(ratings)
            })
        return sorted(genre_summary, key=lambda x: x['Average Rating'], reverse=True)

    def recommend_movies(self, movie_stats, genre, min_rating):
        """Filter movies by genre and minimum rating threshold"""
        recommendations = [
            m for m in movie_stats 
            if m['Genre'] == genre and m['Average Rating'] >= min_rating
        ]
        return sorted(recommendations, key=lambda x: x['Average Rating'], reverse=True)


 
# DATASET (5 GENRES, 5 MOVIES)


def movie_data():
    movies = [
        # Genre 1: Action 
        Movie(1, "RRR", "Action"),
        Movie(2, "K.G.F: Chapter 2", "Action"),
        Movie(3, "Jawan", "Action"),
        Movie(4, "Top Gun: Maverick", "Action"),
        Movie(5, "Baahubali 2: The Conclusion", "Action"),

        # Genre 2: Sci-Fi 
        Movie(6, "Interstellar", "Sci-Fi"),
        Movie(7, "Kalki 2898 AD", "Sci-Fi"),
        Movie(8, "Dune: Part Two", "Sci-Fi"),
        Movie(9, "Avatar: The Way of Water", "Sci-Fi"),
        Movie(10, "Robot 2.0", "Sci-Fi"),

        # Genre 3: Drama 
        Movie(11, "12th Fail", "Drama"),
        Movie(12, "Oppenheimer", "Drama"),
        Movie(13, "Dangal", "Drama"),
        Movie(14, "The Whale", "Drama"),
        Movie(15, "Jatadhara", "Drama"),

        # Genre 4: Comedy 
        Movie(16, "3 Idiots", "Comedy"),
        Movie(17, "Stree 2", "Comedy"),
        Movie(18, "Barbie", "Comedy"),
        Movie(19, "Hera Pheri", "Comedy"),
        Movie(20, "Housefull 4", "Comedy"),

        # Genre 5: Thriller 
        Movie(21, "Drishyam 2", "Thriller"),
        Movie(22, "Parasite", "Thriller"),
        Movie(23, "Kantara", "Thriller"),
        Movie(24, "Get Out", "Thriller"),
        Movie(25, "Cuttputlli", "Thriller")
    ]
    

    ratings = [
        # Action
        Rating(101, 1, 4.8), Rating(102, 1, 4.9), 
        Rating(101, 2, 4.5), Rating(103, 2, 4.3), 
        Rating(102, 3, 3.8), Rating(104, 3, 3.6), 
        Rating(103, 4, 4.7), Rating(105, 4, 4.8), 
        Rating(101, 5, 4.6), Rating(104, 5, 4.7), 

        # Sci-Fi
        Rating(102, 6, 4.9), Rating(105, 6, 4.8), 
        Rating(101, 7, 4.2), Rating(103, 7, 4.0), 
        Rating(103, 8, 4.6), Rating(104, 8, 4.7), 
        Rating(102, 9, 3.9), Rating(105, 9, 4.1), 
        Rating(104, 10, 2.8), Rating(101, 10, 3.0),

        # Drama
        Rating(101, 11, 4.9), Rating(103, 11, 5.0), 
        Rating(102, 12, 4.8), Rating(104, 12, 4.7), 
        Rating(101, 13, 4.6), Rating(105, 13, 4.7), 
        Rating(103, 14, 3.7), Rating(104, 14, 3.5), 
        Rating(102, 15, 2.5), Rating(105, 15, 2.7), 

        # Comedy
        Rating(101, 16, 4.9), Rating(102, 16, 4.8), 
        Rating(103, 17, 4.3), Rating(104, 17, 4.1), 
        Rating(102, 18, 3.9), Rating(105, 18, 4.0), 
        Rating(101, 19, 4.7), Rating(103, 19, 4.6), 
        Rating(104, 20, 2.6), Rating(105, 20, 2.8),

        # Thriller
        Rating(101, 21, 4.6), Rating(102, 21, 4.5), 
        Rating(103, 22, 4.8), Rating(104, 22, 4.7), 
        Rating(101, 23, 4.4), Rating(105, 23, 4.5), 
        Rating(102, 24, 4.2), Rating(104, 24, 4.1), 
        Rating(103, 25, 3.0), Rating(105, 25, 2.8),
        Rating(106, 25, None)                       
    ]
    return movies, ratings



# STREAMLIT APP INTERFACE


st.set_page_config(page_title="Movie Recommendation & Analysis", layout="wide")

st.title("🎬 Movie Recommendation & Analysis Dashboard")
st.write("An interactive analytics system to explore top-rated movies, genre insights, and customized recommendations.")

# Process Data
movies, ratings = movie_data()
analysis = MovieAnalysis(movies, ratings)

clean_ratings = analysis.clean_data()
movie_stats = analysis.compute_movie_stats(clean_ratings)
genre_stats = analysis.compute_genre_stats(movie_stats)

# --- TOP METRIC CARDS ---
overall_avg = sum(m["Average Rating"] for m in movie_stats) / len(movie_stats)
top_genre = genre_stats[0]["Genre"]

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Total Movies Cataloged", f"{len(movie_stats)} Movies")
col_m2.metric("Overall Average Rating", f"{overall_avg:.2f} / 5.0")
col_m3.metric("Top Performing Genre", top_genre)

st.divider()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎯 Recommendation Engine Settings")
genres = sorted(list(set(m['Genre'] for m in movie_stats)))
selected_genre = st.sidebar.selectbox("Select Target Genre", genres)
min_rating = st.sidebar.slider("Minimum Rating Threshold", 2.0, 5.0, 3.5, 0.1)

# --- TABBED LAYOUT ---
tab1, tab2, tab3 = st.tabs(["📊 Performance & Visualizations", "⭐ Top Recommendations", "💾 Export Data"])

with tab1:
    st.subheader("Data & Visual Analytics")
    
    # Section 1: Genre Ratings Chart
    st.write("### 📈 Average Rating by Genre")
    genre_chart_data = {g["Genre"]: g["Average Rating"] for g in genre_stats}
    st.bar_chart(genre_chart_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 📜 Movie Performance Data")
        st.dataframe(movie_stats, use_container_width=True)
        
    with col2:
        st.write("### 🎭 Genre Popularity Breakdown")
        st.dataframe(genre_stats, use_container_width=True)

with tab2:
    st.subheader(f"Recommendations for Genre: '{selected_genre}'")
    recs = analysis.recommend_movies(movie_stats, selected_genre, min_rating)
    
    if recs:
        for item in recs:
            st.success(f"🎥 **{item['Title']}**  \n⭐ **Average Rating:** {item['Average Rating']}/5.0 | 👥 **Total Reviews:** {item['Rating Count']}")
    else:
        st.warning(f"No movies found in '{selected_genre}' with a rating of {min_rating} or higher. Try adjusting the slider on the left!")

with tab3:
    st.subheader("Download Analysis Summary")
    st.write("Generate a formatted CSV report directly from the live application dataset.")
    
    # Text-based CSV generation
    csv_lines = ["Movie ID,Title,Genre,Average Rating,Rating Count"]
    for row in movie_stats:
        csv_lines.append(f"{row['Movie ID']},{row['Title']},{row['Genre']},{row['Average Rating']},{row['Rating Count']}")
    
    csv_string = "\n".join(csv_lines)

    st.download_button(
        label="📥 Download Movie Analysis Report (CSV)",
        data=csv_string,
        file_name="movie_analysis_report.csv",
        mime="text/csv"
    )
    