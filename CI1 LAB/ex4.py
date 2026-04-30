import pandas as pd
import numpy as np
from collections import Counter
import math

def entropy(y):
    counts = Counter(y)
    total = len(y)
    ent = 0
    for c in counts.values():
        p = c / total
        ent -= p * math.log2(p)
    print(f"Entopy:{ent}")
    return ent

def gini(y):
    counts = Counter(y)
    total = len(y)
    g = 1
    for c in counts.values():
        p = c / total
        g -= p * p
    print(f"Gini:{g}")
    return g

def information_gain(df, feature, target):
    total_entropy = entropy(df[target])
    values = df[feature].unique()
    weighted_entropy = 0
    for v in values:
        subset = df[df[feature] == v]
        weighted_entropy += (len(subset) / len(df)) * entropy(subset[target])
    print(f"Weighted entropy({feature}):{weighted_entropy}")
    return total_entropy - weighted_entropy

def gini_gain(df, feature, target):
    total_gini = gini(df[target])
    values = df[feature].unique()
    weighted_gini = 0
    for v in values:
        subset = df[df[feature] == v]
        weighted_gini += (len(subset) / len(df)) * gini(subset[target])
    print(f"Weighted gini:{weighted_gini}")
    return total_gini - weighted_gini

def predict(tree, sample):
    if not isinstance(tree, dict):
        return tree
    feature = list(tree.keys())[0]
    value = str(sample.get(feature))
    if value in tree[feature]:
        return predict(tree[feature][value], sample)
    else:
        return "Unknown"

def calculate_metrics(y_true, y_pred):
    classes = list(set(y_true))
    accuracy = sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true)

    precision_list = []
    recall_list = []

    for c in classes:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == c and p == c)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != c and p == c)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == c and p != c)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        precision_list.append(prec)
        recall_list.append(rec)

    avg_precision = sum(precision_list) / len(precision_list)
    avg_recall = sum(recall_list) / len(recall_list)
    f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"Precision: {avg_precision:.4f}")
    print(f"Recall: {avg_recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

def build_tree(df, target, features, method):
    if len(df[target].unique()) == 1:
        return df[target].iloc[0]
    if not features:
        return Counter(df[target]).most_common(1)[0][0]
    scores = {}
    for f in features:
        if method == 1:
            scores[f] = information_gain(df, f, target)
        else:
            scores[f] = gini_gain(df, f, target)
    best = max(scores, key=scores.get)
    tree = {best: {}}
    for v in df[best].unique():
        subset = df[df[best] == v]
        remaining = [f for f in features if f != best]
        tree[best][v] = build_tree(subset, target, remaining, method)
    return tree

def decision_tree_manual():
    n = int(input("Enter number of samples: "))
    m = int(input("Enter number of attributes (excluding class): "))
    cols = []
    for i in range(m):
        cols.append(input(f"Enter attribute {i+1} name: "))
    target = input("Enter class label name: ")
    cols.append(target)
    data = []
    print("\nEnter data row-wise:")
    for i in range(n):
        row = input(f"Row {i+1}: ").split()
        data.append(row)
    df = pd.DataFrame(data, columns=cols)
    print("\nSplit method: 1-Entropy 2-Gini")
    method = int(input())
    print("\n--- Intermediate Values ---")
    scores = {}
    for feature in cols[:-1]:
        if method == 1:
            val = information_gain(df, feature, target)
            print(f"Information Gain({feature}) = {val:.4f}")
        else:
            val = gini_gain(df, feature, target)
            print(f"Gini Gain({feature}) = {val:.4f}")
        scores[feature] = val
    root = max(scores, key=scores.get)
    print("\nRoot Node Selected:", root)

def decision_tree_csv():
    file = input("Enter CSV file name: ")
    df = pd.read_csv(file).astype(str)
    target = input("Enter class label column: ")
    features = [c for c in df.columns if c != target]
    print("Split method: 1-Entropy 2-Gini")
    method = int(input())
    tree = build_tree(df, target, features, method)
    print("\nDecision Tree:\n", tree)

    y_true = df[target].tolist()
    y_pred = [predict(tree, row) for _, row in df.iterrows()]
    calculate_metrics(y_true, y_pred)

    print("\n--- Predict New Observation ---")
    new_obs = {}
    for f in features:
        new_obs[f] = input(f"Enter value for {f}: ")
    print(f"Predicted Class: {predict(tree, new_obs)}")

print("\n1. Manual Decision Tree (Root Only)")
print("2. CSV Decision Tree (Full Tree)")
choice = int(input("Enter choice: "))
if choice == 1:
    decision_tree_manual()
else:
    decision_tree_csv()