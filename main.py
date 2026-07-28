import pandas as pd


# reading the letterboxd data
films_df = pd.read_csv('films.csv', on_bad_lines='skip')
ratings_df = pd.read_csv('ratings.csv', on_bad_lines='skip')




# reading and cleaning user data
films_df = films_df.dropna(subset=['year'])
films_df['year'] = films_df['year'].astype(int)

input_ratings = pd.read_csv("userRatings.csv")

input_ratings = input_ratings.drop(["Letterboxd URI" , "Date"] , axis=1)

input_ratings = input_ratings.rename(columns={"Name" :"film_name" ,"Rating" :"rating"})


input_watched = pd.read_csv("watched.csv")

input_watched  = input_watched.drop(["Date" , "Letterboxd URI"], axis=1)

input_watched = input_watched.rename(columns={"Name":"film_name", "Year":"year"})

input_ratings = pd.merge(input_ratings , input_watched, on="film_name", how="inner")

input_ratings = pd.merge(input_ratings,films_df, on=["year","film_name"],how="inner")

# calculating the similarities
similar_ratings = ratings_df[ratings_df['film_id'].isin(input_ratings['film_id'].tolist())]
groups = similar_ratings.groupby("user_name")

similarities = {}

for username, group in groups:

    common = input_ratings.merge(
        group,
        on="film_id",
        suffixes=("_target", "_other")
    )

    # Skip users with very few common movies
    if len(common) < 3:
        continue
    if common["rating_target"].std() == 0:
        continue

    if common["rating_other"].std() == 0:
        continue

    similarity = common["rating_target"].corr(common["rating_other"])

    if pd.isna(similarity):
        continue

    similarities[username] = similarity

similarities = pd.DataFrame(
    similarities.items(),
    columns=["user_name", "similarity"]
)
similarities = similarities[similarities['similarity'] > 0.1]

similarities = similarities.sort_values(by=["similarity"],ascending=False)

neighbors = similarities.head(60)

watched = set(input_ratings["film_id"])

neighbors_ratings = pd.merge(ratings_df , neighbors, on='user_name' , how= 'inner')

neighbors_ratings = neighbors_ratings[~neighbors_ratings['film_id'].isin(watched)]

neighbors_ratings = neighbors_ratings[neighbors_ratings['similarity'] > 0]

neighbors_ratings['weighted_ratings'] = neighbors_ratings['rating'] * neighbors_ratings['similarity']

target_films = neighbors_ratings.groupby('film_id').agg(
    similarity=('similarity', 'sum'),
    weighted_ratings=('weighted_ratings', 'sum'),
    n_neighbors=('similarity', 'count')
)
target_films = target_films[target_films['n_neighbors'] >= 3]

target_films['weighted_average'] = target_films['weighted_ratings'] / target_films['similarity']


target_films = target_films.sort_values(['weighted_average' , 'similarity'], ascending=False)

target_films = target_films.reset_index()
target_films = pd.merge(target_films, films_df , on="film_id" , how="inner")

target_films = target_films[~target_films['film_name'].isin(input_watched['film_name'].tolist())]

print(target_films[['film_name', 'year', 'weighted_average' , 'similarity']].head(50))

