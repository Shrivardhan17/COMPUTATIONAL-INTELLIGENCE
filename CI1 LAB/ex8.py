import numpy as np

def sigmoid(yin):
    return 1 / (1 + np.exp(-yin))

def tanh(yin):
    return np.tanh(yin)

def activation(activation_type, yin, theta, off_state):
    if activation_type == 1:  # Threshold
        return 1 if yin >= theta else off_state
    elif activation_type == 2:  # Sigmoid
        return 1 if sigmoid(yin) >= theta else off_state
    elif activation_type == 3:  # Tanh
        return 1 if tanh(yin) >= theta else off_state


def train(data, n, w, b, alpha, activation_type, theta, max_epochs=10):
    dataset = np.array(data)
    X = dataset[:, :-1]
    T = dataset[:, -1]

    # Determine off_state automatically (0 or -1 dataset)
    off_state = -1 if -1 in np.unique(T) else 0

    for epoch in range(1, max_epochs + 1):
        print(f"\n===== Epoch {epoch} =====")
        print(f"{'Inputs':<12} {'t':<3} {'yin':<7} {'y':<4} {'chg_W':<18} {'chg_b':<6} {'W':<18} {'b':<5}")
        print("-" * 90)

        error_count = 0   #  Better stopping check

        for i in range(len(X)):
            x_i = X[i]
            t_i = T[i]

            yin = np.dot(x_i, w) + b
            y = activation(activation_type, yin, theta, off_state)

            ch_w = np.zeros(n)
            ch_b = 0.0

            if y != t_i:
                ch_w = alpha * t_i * x_i
                w = w + ch_w
                ch_b = alpha * t_i
                b = b + ch_b
                error_count += 1

            print(f"{str(x_i):<12} {t_i:<3} {yin:<7.2f} {y:<4} {str(ch_w):<18} {ch_b:<6.1f} {str(w):<18} {b:<5.1f}")

        #  STOP immediately when no errors in epoch
        if error_count == 0:
            print(f"\n CONVERGED at Epoch {epoch}")
            return w, b

    print("\nStopped due to max epochs.")
    return w, b


# ----------- MAIN PROGRAM -----------
try:
    data = np.loadtxt("data.txt", dtype=int)

    n = int(input("Enter number of inputs (n): "))

    print("Enter initial weights:")
    w = np.array([float(input(f"w{i+1}: ")) for i in range(n)])

    b = float(input("Enter bias (b): "))
    alpha = float(input("Enter learning rate (alpha): "))

    print("\nSelect Activation Function:")
    print("1. Threshold")
    print("2. Sigmoid")
    print("3. Tanh")
    activation_type = int(input("Enter choice (1-3): "))

    theta = float(input("Enter threshold: "))

    final_w, final_b = train(data, n, w, b, alpha, activation_type, theta)

    print("\nFinal Answer:")
    print("Weights:", final_w)
    print("Bias:", final_b)

except Exception as e:
    print("Error:", e)

