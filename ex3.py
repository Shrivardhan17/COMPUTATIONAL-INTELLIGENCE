import math
from collections import Counter

# -------------------------------
# TRAINING DATA (Features + Labels)
# -------------------------------
X_train = [
    [1, 2],
    [2, 3],
    [3, 3],
    [6, 5],
    [7, 7],
    [8, 6]
]

y_train = ['A', 'A', 'A', 'B', 'B', 'B']

# -------------------------------
# EUCLIDEAN DISTANCE FUNCTION
# -------------------------------
def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

# -------------------------------
# KNN FUNCTION
# -------------------------------
def knn_predict(X_train, y_train, test_point, k):
    distances = []

    # Step 1: Calculate distance from all training points
    for i in range(len(X_train)):
        dist = euclidean_distance(test_point, X_train[i])
        distances.append((dist, y_train[i]))

    # Step 2: Sort by distance
    distances.sort(key=lambda x: x[0])

    # Step 3: Take k nearest neighbors
    k_neighbors = distances[:k]

    # Step 4: Majority voting
    labels = [label for _, label in k_neighbors]
    prediction = Counter(labels).most_common(1)[0][0]

    return prediction

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    test_point = [5, 5]
    k = 3

    result = knn_predict(X_train, y_train, test_point, k)

    print("Test Point:", test_point)
    print("Predicted Class:", result)