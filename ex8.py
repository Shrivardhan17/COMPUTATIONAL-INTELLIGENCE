# ------------------------------------------
# BAYES RULE, CONDITIONAL & MARGINAL PROBABILITY
# WITHOUT USING SHORTCUT BUILT-INS
# ------------------------------------------

# Step 1: Define probabilities manually
# ------------------------------------------

# Probability of Disease
P_D = 0.01

# Probability of No Disease
P_not_D = 1.0 - P_D

# Probability of Positive test given Disease
P_pos_given_D = 0.99

# Probability of Positive test given No Disease
P_pos_given_not_D = 0.05


# ------------------------------------------
# Step 2: Function to multiply two numbers
# (manual step for clarity)
# ------------------------------------------
def multiply(a, b):
    result = a * b
    return result


# ------------------------------------------
# Step 3: Function to add two numbers
# ------------------------------------------
def add(a, b):
    result = a + b
    return result


# ------------------------------------------
# Step 4: Conditional Probability Function
# P(A|B) = P(A ∩ B) / P(B)
# ------------------------------------------
def conditional_probability(intersection, prob_B):
    if prob_B == 0:
        return 0
    result = intersection / prob_B
    return result


# ------------------------------------------
# Step 5: Compute Joint Probabilities
# ------------------------------------------

# P(D AND +)
joint_D_pos = multiply(P_D, P_pos_given_D)

# P(not D AND +)
joint_notD_pos = multiply(P_not_D, P_pos_given_not_D)


# ------------------------------------------
# Step 6: Compute Marginal Probability P(+)
# P(+) = P(D AND +) + P(not D AND +)
# ------------------------------------------
P_pos = add(joint_D_pos, joint_notD_pos)


# ------------------------------------------
# Step 7: Apply Bayes Rule
# P(D | +) = P(D AND +) / P(+)
# ------------------------------------------
P_D_given_pos = conditional_probability(joint_D_pos, P_pos)


# ------------------------------------------
# Step 8: Display Results Step by Step
# ------------------------------------------

print("----- GIVEN PROBABILITIES -----")
print("P(Disease) =", P_D)
print("P(No Disease) =", P_not_D)
print("P(+ | Disease) =", P_pos_given_D)
print("P(+ | No Disease) =", P_pos_given_not_D)

print("\n----- JOINT PROBABILITIES -----")
print("P(D AND +) =", joint_D_pos)
print("P(not D AND +) =", joint_notD_pos)

print("\n----- MARGINAL PROBABILITY -----")
print("P(+) =", P_pos)

print("\n----- BAYES RESULT -----")
print("P(D | +) =", P_D_given_pos)


# ------------------------------------------
# Step 9: Extra Explanation Output
# ------------------------------------------
print("\n----- INTERPRETATION -----")

if P_D_given_pos < 0.5:
    print("Even if test is positive, probability of disease is LOW")
else:
    print("High probability of disease if test is positive")


# ------------------------------------------
# Step 10: Manual Loop Demonstration
# (to extend logic for multiple cases)
# ------------------------------------------

print("\n----- LOOP DEMONSTRATION -----")

# Simulate checking multiple hypothetical probabilities
test_values = [0.01, 0.05, 0.1]

i = 0
while i < len(test_values):
    temp_PD = test_values[i]
    temp_not_PD = 1 - temp_PD

    # Compute joint values
    temp_joint1 = multiply(temp_PD, P_pos_given_D)
    temp_joint2 = multiply(temp_not_PD, P_pos_given_not_D)

    # Compute marginal
    temp_Ppos = add(temp_joint1, temp_joint2)

    # Compute Bayes
    temp_result = conditional_probability(temp_joint1, temp_Ppos)

    print("For P(D) =", temp_PD, "→ P(D|+) =", temp_result)

    i = i + 1


# ------------------------------------------
# END OF PROGRAM
# ------------------------------------------