# ------------- WAVE 1 --------------------

def create_movie(title, genre, rating):
    new_movie = {}

    if title and genre and rating:
        new_movie["title"] = title
        new_movie["genre"] = genre
        new_movie["rating"] = rating
        return new_movie
    return None

def add_to_watched(user_data, movie):
    user_data["watched"].append(movie)
    return user_data

def add_to_watchlist(user_data, movie):
    user_data["watchlist"].append(movie)
    return user_data

def watch_movie(user_data, title):
    for movie in user_data["watchlist"]:
        if title == movie["title"]:
            add_to_watched(user_data, movie)
            user_data["watchlist"].remove(movie)
    return user_data

# -----------------------------------------
# ------------- WAVE 2 --------------------
# -----------------------------------------
def get_watched_avg_rating(user_data):
    avg_rating = 0.0
    summed_ratings = 0
    collected_ratings = []

    if len(user_data["watched"]) >= 1:
        collected_ratings = [movie["rating"] for movie in user_data["watched"]]
    else:
        return avg_rating

    for rating in collected_ratings:
        summed_ratings += rating

    avg_rating = (summed_ratings / len(collected_ratings))
    return avg_rating

def get_most_watched_genre(user_data):
    genre_count = {}
    top_genre = (0, 0)

    if len(user_data["watched"]) < 1:
        return None

    for movie in user_data["watched"]:
        if not movie["genre"] in genre_count:
            genre_count[movie["genre"]] = 1
        else:
            genre_count[movie["genre"]] += 1

    for genre_pair in genre_count.items():
        if genre_pair[1] > top_genre[1]:
            top_genre = genre_pair

    return top_genre[0]

# -----------------------------------------
# ------------- WAVE 3 --------------------
# -----------------------------------------
def get_unique_watched(user_data):
    friends_watched = [movie for friend in user_data["friends"] 
        for movie in friend["watched"]]

    unique_watched = [movie for movie in user_data["watched"] 
        if not movie in friends_watched]

    return unique_watched

def get_friends_unique_watched(user_data):
    unique_watched = []

    friends_watched = [movie for friend in user_data["friends"] 
        for movie in friend["watched"]]

    friends_watched_dict = {movie["title"]:movie for movie in friends_watched}

    user_titles_watched = [movie["title"] for movie in user_data["watched"]]

    unique_watched = [friends_watched_dict[movie_title] for movie_title in friends_watched_dict.keys() 
        if not movie_title in user_titles_watched]

    return unique_watched
        
# -----------------------------------------
# ------------- WAVE 4 --------------------
# -----------------------------------------
def get_available_recs(user_data):
    friends_unique_watched = get_friends_unique_watched(user_data)

    recommended_movies = [movie for movie in friends_unique_watched 
        if movie["host"] in user_data["subscriptions"]]

    return recommended_movies

# -----------------------------------------
# ------------- WAVE 5 --------------------
# -----------------------------------------
def get_new_rec_by_genre(user_data):
    recommendations = []

    if len(user_data["watched"]) < 1:
        return recommendations

    if len(user_data["friends"]) < 1:
        return recommendations

    friend_recommendations = get_available_recs(user_data)
    user_top_genre = get_most_watched_genre(user_data)        

    recommendations = [movie for movie in friend_recommendations 
        if movie["genre"] == user_top_genre]

    return recommendations

def get_rec_from_favorites(user_data):
    recommendations = []
    user_unique_watched = get_unique_watched(user_data)

    if len(user_data["favorites"]) < 1:
        return recommendations

    if len(user_data["friends"]) < 1:
        return user_data["favorites"]

    recommendations = [movie for movie in user_data["favorites"] 
        if movie in user_unique_watched]

    return recommendations
