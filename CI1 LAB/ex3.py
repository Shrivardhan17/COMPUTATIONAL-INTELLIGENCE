import numpy as np
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
import math

# ---------------- DISTANCE FUNCTIONS ---------------- #

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

def chebyshev(a, b):
    return max(abs(x - y) for x, y in zip(a, b))

# ---------------- KNN PREDICTION ---------------- #

def knn_predict(X_train, y_train, x_test, k, dist_func, weighted, verbose=False):
    distances = []

    # Compute distance from each training point
    for i in range(len(X_train)):
        d = dist_func(X_train[i], x_test)
        distances.append((d, y_train[i], X_train[i]))

    # Sort by distance
    distances.sort(key=lambda x: x[0])

    # Take k nearest neighbors
    neighbors = distances[:k]

    # PRINT TABLE ONLY FOR MANUAL MODE
    if verbose:
        print("\nInput Test Point:", x_test)
        print(f"\n{'Rank':<4} | {'Training Point':<20} | {'Distance':<10} | {'Class':<6} | {'1/d^2' if weighted else ''}")
        print("-" * 75)

        for idx, (d, label, point) in enumerate(neighbors, start=1):
            if weighted:
                w = 1 / (d**2 + 1e-9)
                print(f"{idx:<4} | {str(point):<20} | {d:10.4f} | {label:<6} | {w:.6f}")
            else:
                print(f"{idx:<4} | {str(point):<20} | {d:10.4f} | {label:<6}")

    # Voting
    if weighted:
        votes = {}
        for d, label, _ in neighbors:
            w = 1 / (d**2 + 1e-9)
            votes[label] = votes.get(label, 0) + w
        return max(votes, key=votes.get)
    else:
        labels = [label for _, label, _ in neighbors]
        return Counter(labels).most_common(1)[0][0]

# ---------------- EVALUATION METRICS ---------------- #

def evaluate(y_true, y_pred):
    classes = np.unique(y_true)
    TP = FP = FN = 0

    # Calculating metrics globally (Micro-averaging logic)
    for c in classes:
        TP += np.sum((y_true == c) & (y_pred == c))
        FP += np.sum((y_true != c) & (y_pred == c))
        FN += np.sum((y_true == c) & (y_pred != c))

    accuracy = np.mean(y_true == y_pred)
    precision = TP / (TP + FP + 1e-9)
    recall = TP / (TP + FN + 1e-9)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-9)

    return accuracy, precision, recall, f1

# ---------------- MANUAL MODE ---------------- #

def knn_manual():
    n = int(input("Enter number of training samples: "))
    m = int(input("Enter number of attributes: "))

    X_train = []
    y_train = []

    print("\nEnter training data:")
    for i in range(n):
        row = list(map(float, input(f"Features {i+1} (space separated): ").split()))
        label = input("Class: ")
        X_train.append(row)
        y_train.append(label)

    x_test = list(map(float, input("\nEnter new data point to predict: ").split()))
    k = int(input("Enter k value: "))

    print("\nDistance metric: 1-Euclidean 2-Manhattan 3-Chebyshev")
    d_choice = int(input("Choice: "))
    dist_func = euclidean if d_choice == 1 else manhattan if d_choice == 2 else chebyshev

    weighted = input("Weighted KNN? (y/n): ").lower() == 'y'

    result = knn_predict(
        np.array(X_train),
        np.array(y_train),
        x_test,
        k,
        dist_func,
        weighted,
        verbose=True
    )

    print("\n>>> Predicted Class:", result)

# ---------------- CSV MODE ---------------- #

def knn_from_csv():
    file = input("Enter CSV file name (e.g., data.csv): ")
    df = pd.read_csv(file)

    class_col = input("Enter the target (class label) column name: ")

    # Optional: Filter columns if needed
    if input("Use all columns? (y/n): ").lower() == 'n':
        cols = input("Enter feature column names (comma separated): ").split(',')
        cols = [c.strip() for c in cols]
        X = df[cols].values
    else:
        X = df.drop(columns=[class_col]).values

    y = df[class_col].values

    train_percent = int(input("Enter training percentage (e.g., 80): "))

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=(100 - train_percent) / 100,
        shuffle=True,
        random_state=42
    )

    # Calculate k
    k = int(0.1 * len(X_train))
    k = max(1, k if k % 2 != 0 else k + 1)

    # Distance Selection
    print("\nDistance metric: 1-Euclidean 2-Manhattan 3-Chebyshev")
    d_choice = int(input("Choice: "))
    dist_func = euclidean if d_choice == 1 else manhattan if d_choice == 2 else chebyshev
    weighted = input("Weighted KNN? (y/n): ").lower() == 'y'

    # DISPLAY RECORD COUNTS
    print("\n" + "="*30)
    print(f"Dataset Summary:")
    print(f"Total Records    : {len(df)}")
    print(f"Training Records : {len(X_train)}")
    print(f"Test Records     : {len(X_test)}")
    print(f"Value of K       : {k}")
    print("="*30)

    print("\nProcessing predictions... Please wait.")
    y_pred = []
    for x in X_test:
        # verbose=False ensures we don't print every single distance calculation
        y_pred.append(knn_predict(X_train, y_train, x, k, dist_func, weighted, verbose=False))

    return evaluate(y_test, np.array(y_pred))


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    print("--- KNN Classifier Tool ---")
    print("1. Manual Entry Mode")
    print("2. CSV File Mode")

    try:
        choice = int(input("Enter choice (1/2): "))
        if choice == 1:
            knn_manual()
        elif choice == 2:
            acc, prec, rec, f1 = knn_from_csv()
            print("\n--- Model Evaluation ---")
            print(f"Accuracy  : {acc:.4f}")
            print(f"Precision : {prec:.4f}")
            print(f"Recall    : {rec:.4f}")
            print(f"F1 Score  : {f1:.4f}")
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"An error occurred: {e}")