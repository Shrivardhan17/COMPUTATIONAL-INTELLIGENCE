import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# -------------------------------
# LOAD DATA
# -------------------------------
data = load_iris()
X = data.data
y = data.target

# -------------------------------
# SPLIT DATA
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# -------------------------------
# DEFINE MODELS
# -------------------------------
model1 = LogisticRegression(max_iter=200)
model2 = DecisionTreeClassifier()
model3 = KNeighborsClassifier(n_neighbors=5)

# -------------------------------
# ENSEMBLE MODEL (VOTING)
# -------------------------------
ensemble = VotingClassifier(
    estimators=[
        ('lr', model1),
        ('dt', model2),
        ('knn', model3)
    ],
    voting='hard'   # majority voting
)

# -------------------------------
# TRAIN
# -------------------------------
ensemble.fit(X_train, y_train)

# -------------------------------
# PREDICT
# -------------------------------
y_pred = ensemble.predict(X_test)

# -------------------------------
# ACCURACY
# -------------------------------
print("Ensemble Accuracy:", accuracy_score(y_test, y_pred))