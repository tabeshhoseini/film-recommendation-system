# User-Based Movie Recommendation System

A simple movie recommendation system built with **Python** and **Pandas** using a user-based collaborative filtering approach.

## Overview

This project recommends movies to a target user by finding other users with similar movie preferences. Similarity is calculated using the **Pearson Correlation Coefficient**, and recommendations are generated from highly rated movies of the most similar users.

## Features

* Load and process movie rating data
* Compute user-to-user similarity using Pearson correlation
* Find the most similar users (nearest neighbors)
* Predict ratings for unseen movies using weighted averages
* Recommend the highest-ranked movies to the target user

## Technologies

* Python
* Pandas
* NumPy

## How It Works

1. Load the movie ratings dataset(letterboxd dataset).
2. Compare the target user with every other user based on commonly rated movies.
3. Calculate similarity scores using Pearson correlation.
4. Select the most similar users.
5. Predict ratings for movies the target user hasn't watched.
6. Recommend the highest-scoring movies.

## Future Improvements

* Item-based collaborative filtering
* Matrix factorization (SVD)

## License

This project is intended for educational purposes.

You can make it even more professional by adding a **Sample Output** section with a screenshot of your recommendations once the project is finished. That makes GitHub projects much more appealing to recruiters.

