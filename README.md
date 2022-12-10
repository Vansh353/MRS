# Movie Recomendation System

## Deployment link : https://vansh3503-mrs-app-vg2add.streamlit.app/

This project uses Content based filtering algorithm for measuring similarity between 2 data points, in this case it's 2 movies.
Bag of words approach is used here and are preprocessed into vectors by Count Vectorizer.


A Content-Based Recommender works by the data that we take from the user, either explicitly (rating) or implicitly (clicking on a link). By the data we create a user profile, which is then used to suggest to the user, as the user provides more input or take more actions on the recommendation, the engine becomes more accurate.

![image](https://user-images.githubusercontent.com/110348311/206867654-ec4ee27b-b2cf-43a3-bf87-f6de8df7ba1f.png)

# User Profile:
In the User Profile, we create vectors that describe the user’s preference. In the creation of a user profile, we use the utility matrix which describes the relationship between user and item. With this information, the best estimate we can make regarding which item user likes, is some aggregation of the profiles of those items.
Item Profile:
In Content-Based Recommender, we must build a profile for each item, which will represent the important characteristics of that item.
For example, if we make a movie as an item then its actors, director, release year and genre are the most significant features of the movie. We can also add its rating from the IMDB (Internet Movie Database) in the Item Profile.
Utility Matrix:
Utility Matrix signifies the user’s preference with certain items. In the data gathered from the user, we have to find some relation between the items which are liked by the user and those which are disliked, for this purpose we use the utility matrix. In it we assign a particular value to each user-item pair, this value is known as the degree of preference. Then we draw a matrix of a user with the respective items to identify their preference relationship.

![image](https://user-images.githubusercontent.com/110348311/206867719-a12dd5c9-cca9-42af-b4b6-efbfb79c7382.png)
Some of the columns are blank in the matrix that is because we don’t get the whole input from the user every time, and the goal of a recommendation system is not to fill all the columns but to recommend a movie to the user which he/she will prefer. Through this table, our recommender system won’t suggest Movie 3 to User 2, because in Movie 1 they have given approximately the same ratings, and in Movie 3 User 1 has given the low rating, so it is highly possible that User 2 also won’t like it.

## Recommending Items to User Based on Content:

# Method 1:
We can use the cosine distance between the vectors of the item and the user to determine its preference to the user. For explaining this, let us consider an example:
We observe that the vector for a user will have a positive number for actors that tend to appear in movies the user likes and negative numbers for actors user doesn’t like, Consider a movie with actors which user likes and only a few actors which user doesn’t like, then the cosine angle between the user’s and movie’s vectors will be a large positive fraction. Thus, the angle will be close to 0, therefore a small cosine distance between the vectors.
It represents that the user tends to like the movie, if the cosine distance is large, then we tend to avoid the item from the recommendation.
# Method 2:
We can use a classification approach in the recommendation systems too, like we can use the Decision Tree for finding out whether a user wants to watch a movie or not, like at each level we can apply a certain condition to refine our recommendation. For example:


![image](https://user-images.githubusercontent.com/110348311/206867661-8c749059-dfe8-446f-8b85-f86ee260f114.png)



# Refrences :
[1] GFG : https://www.geeksforgeeks.org/ml-content-based-recommender-system/
