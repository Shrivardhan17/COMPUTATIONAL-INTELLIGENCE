import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# -------------------------------
# SAMPLE DATA (features + labels)
# -------------------------------
X = np.array([
    [50, 60, 2],
    [80, 90, 5],
    [30, 40, 1],
    [70, 75, 4],
    [90, 95, 6],
    [20, 30, 1]
])

y = np.array([0, 1, 0, 1, 1, 0])  # 0 = Fail, 1 = Pass

# -------------------------------
# PREPROCESSING
# -------------------------------
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# -------------------------------
# BUILD MODEL
# -------------------------------
model = Sequential()

# Input + Hidden Layers
model.add(Dense(5, activation='relu', input_dim=3))
model.add(Dense(3, activation='relu'))

# Output Layer
model.add(Dense(1, activation='sigmoid'))

# -------------------------------
# COMPILE MODEL
# -------------------------------
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# -------------------------------
# TRAIN MODEL
# -------------------------------
model.fit(X_train, y_train, epochs=50, verbose=1)

# -------------------------------
# EVALUATE
# -------------------------------
loss, accuracy = model.evaluate(X_test, y_test)
print("Accuracy:", accuracy)