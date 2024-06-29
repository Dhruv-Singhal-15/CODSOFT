import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('task4/movie-dataset/movies.csv')  
ratings = pd.read_csv('task4/movie-dataset/ratings.csv')  

user_movie_ratings = ratings.pivot(index='userId', columns='movieId', values='rating')

user_movie_ratings.fillna(0, inplace=True)

user_similarity = cosine_similarity(user_movie_ratings)

user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_ratings.index, columns=user_movie_ratings.index)

def get_user_recommendations(user_id, num_recommendations=5):

    if user_id not in user_movie_ratings.index:
        print("User ID not found!")
        return None
    
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    similar_users = similar_users[similar_users.index != user_id]

    similar_users_ratings = user_movie_ratings.loc[similar_users.index]

    weighted_ratings = similar_users_ratings.T.dot(similar_users).div(similar_users.sum())

    user_ratings = user_movie_ratings.loc[user_id]
    recommendations = weighted_ratings[user_ratings[user_ratings == 0].index]

    return recommendations.sort_values(ascending=False).head(num_recommendations)

def add_new_user(user_id, movie_ratings):
    global user_movie_ratings, user_similarity_df
    
    user_movie_ratings.loc[user_id] = 0  
    for movie_id, rating in movie_ratings.items():
        user_movie_ratings.at[user_id, movie_id] = rating
    
    user_similarity = cosine_similarity(user_movie_ratings)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_ratings.index, columns=user_movie_ratings.index)


def main():
    choice = input("Do you want to (1) Enter an existing user ID or (2) Create a new user? Enter 1 or 2: ")
    
    if choice == '1':
        user_id = int(input("Enter your user ID: "))
        num_recommendations = int(input("Enter the number of recommendations you want: "))

        recommendations = get_user_recommendations(user_id, num_recommendations)
        
        if recommendations is not None:
            print(f"Top {num_recommendations} recommendations for user {user_id}:")
            for movie_id in recommendations.index:
                print(movies[movies['movieId'] == movie_id]['title'].values[0])
    
    elif choice == '2':
        new_user_id = int(input("Enter a new user ID: "))
        movie_ratings = {}
        
        print("Enter movie names and ratings (enter 'stop' to finish):")
        while True:
            movie_name = str(input("Enter movie name: "))
            if movie_name.lower() == 'stop':
                break
            rating = float(input("Enter your rating for the movie (0.5 to 5): "))

            movie_id = movies[movies['title'].str.contains(movie_name, case=False, regex=False)]
            if not movie_id.empty:
                movie_id = movie_id.iloc[0]['movieId']
                movie_ratings[movie_id] = rating
            else:
                print(f"Movie '{movie_name}' not found!")
        
        add_new_user(new_user_id, movie_ratings)
        
        num_recommendations = int(input("Enter the number of recommendations you want: "))
        
        recommendations = get_user_recommendations(new_user_id, num_recommendations)
        
        if recommendations is not None:
            print(f"Top {num_recommendations} recommendations for user {new_user_id}:")
            for movie_id in recommendations.index:
                print(movies[movies['movieId'] == movie_id]['title'].values[0])
    
    else:
        print("Invalid choice! Please enter 1 or 2.")

if __name__ == "__main__":
    main()