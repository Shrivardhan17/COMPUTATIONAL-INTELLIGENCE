import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# INPUT
# -----------------------------
file_name = input("Enter CSV file name: ")
df = pd.read_csv(file_name)

# Automatically remove 'Date' as requested
if 'Date' in df.columns:
    df = df.drop(columns=['Date'])
    print("\n'Date' column removed.")

print("Columns available:", list(df.columns))
target_col = input("Enter target column name: ")

# -----------------------------
# PREPROCESSING (Categorical to Numeric)
# -----------------------------
# RandomForest requires numeric data. This converts text columns to numbers.
le = LabelEncoder()
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = le.fit_transform(df[col].astype(str))

X = df.drop(columns=[target_col])
y = df[target_col]

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
train_percent = float(input("Enter training percentage (e.g. 80): "))
test_size = 1 - (train_percent / 100)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

# -----------------------------
# MODEL TRAINING
# -----------------------------
n_estimators = int(input("Enter number of trees (n_estimators): "))
criterion = input("Enter criterion (gini/entropy): ").lower()

model = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# EVALUATION & OUTPUT
# -----------------------------
y_pred = model.predict(X_test)

# Confusion Matrix & Counts
cm = confusion_matrix(y_test, y_pred)
is_binary = len(y.unique()) == 2

print("\n--- DATASET INFO ---")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
print("\n--- RESULTS ---")
print("Accuracy :", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1_score(y_test, y_pred, average='weighted') * 100, 2), "%")

print("\n--- CONFUSION MATRIX ---")
print(cm)

if is_binary:
    tn, fp, fn, tp = cm.ravel()
    print(f"\nTP: {tp} | TN: {tn} | FP: {fp} | FN: {fn}")
