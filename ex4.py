import math
from collections import Counter

# -------------------------------
# DATASET (Outlook, Temp, Humidity, Wind -> Play)
# -------------------------------
data = [
    ['Sunny', 'Hot', 'High', 'Weak', 'No'],
    ['Sunny', 'Hot', 'High', 'Strong', 'No'],
    ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
    ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
    ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
]

features = ['Outlook', 'Temp', 'Humidity', 'Wind']

# -------------------------------
# ENTROPY FUNCTION
# -------------------------------
def entropy(data):
    labels = [row[-1] for row in data]
    total = len(labels)
    count = Counter(labels)

    ent = 0
    for c in count.values():
        p = c / total
        ent -= p * math.log2(p)
    return ent

# -------------------------------
# SPLIT DATA
# -------------------------------
def split_data(data, col, value):
    return [row for row in data if row[col] == value]

# -------------------------------
# INFORMATION GAIN
# -------------------------------
def information_gain(data, col):
    total_entropy = entropy(data)
    values = set(row[col] for row in data)

    weighted_entropy = 0
    for v in values:
        subset = split_data(data, col, v)
        weighted_entropy += (len(subset) / len(data)) * entropy(subset)

    return total_entropy - weighted_entropy

# -------------------------------
# BUILD TREE (ID3)
# -------------------------------
def build_tree(data, features):
    labels = [row[-1] for row in data]

    # If all same → leaf node
    if len(set(labels)) == 1:
        return labels[0]

    # If no features left
    if not features:
        return Counter(labels).most_common(1)[0][0]

    # Find best feature
    gains = [information_gain(data, i) for i in range(len(features))]
    best_index = gains.index(max(gains))
    best_feature = features[best_index]

    tree = {best_feature: {}}

    values = set(row[best_index] for row in data)

    for v in values:
        subset = split_data(data, best_index, v)
        new_features = features[:best_index] + features[best_index+1:]

        # Remove column
        new_subset = [row[:best_index] + row[best_index+1:] for row in subset]

        tree[best_feature][v] = build_tree(new_subset, new_features)

    return tree

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    tree = build_tree(data, features)
    print("Decision Tree:")
    print(tree)